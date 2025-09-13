from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import JsonResponse, FileResponse, HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from journal.models import User, Entry, Achievement, Reminder
from django.http import JsonResponse, HttpResponse, FileResponse
from journal.forms import LogInForm, PasswordForm, UserForm, SignUpForm, EntryForm, EmailForm, ReminderForm
from journal.helpers import login_prohibited
from django.utils import timezone
import json
import io
import zipfile
import reportlab
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from .ai_journal import generate_ai_question
from datetime import datetime
from io import BytesIO
import bs4
from bs4 import BeautifulSoup
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.templatetags.static import static
from PIL import Image as PILImage
import base64
import logging

logger = logging.getLogger(__name__)

@login_required
def dashboard(request):
    """Display the current user's dashboard."""
    current_user = request.user
    entries = Entry.objects.filter(user=request.user).order_by('-date_created')
    current_date = datetime.now().date()
    templates = Entry.objects.filter(user=request.user, is_template=True)

    # Parse the given date string
    given_date = datetime.strptime(str(current_user.last_login), "%Y-%m-%d %H:%M:%S.%f%z")

    # Get the current date
    current_date = datetime.now(given_date.tzinfo)

    # Calculate the absolute difference in days
    days_difference = abs((current_date - given_date).days)
    isDaily = False
    # Check if the difference is greater than or equal to 1 day

    given_time = given_date.time()
    current_time = datetime.now().time()
    if current_time < given_time and current_date.day - given_date.day == 1:
        days_difference += 1

    if(days_difference >= 1):
        # Update the last login date
        current_user.last_login = current_date
        current_user.save()
        isDaily = True
    else:
        isDaily = False
    
    context = {
        'current_date': current_date,
        'user': current_user,
        'entries': entries,
        'templates': templates,
        'isDaily': isDaily
        }
    return render(request, 'dashboard.html', context)
    
@login_required
def create_entry(request):
    """Create a new entry."""

    if request.method == 'POST':
        entry = Entry(user=request.user, title="New Title", text='<div>New Entry</div>', bookmarked=False)
        entry.save()
        return redirect('dashboard')
    else:
        return JsonResponse({'status': 'error', 'message': 'Cannot get create_entry'}, status=302)

@login_required
def get_entry(request, entry_id):
    """Get the selected new entry."""

    try:
        entry = Entry.objects.get(id=entry_id, user=request.user)
        return JsonResponse({'title':entry.title,'text': entry.text, 'mood': entry.mood})
    except Entry.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Entry not found'}, status=404)

@login_required
def update_entry(request, entry_id):
    """Update and save changes made to an entry."""

    try:
        data = json.loads(request.body)
        entry = Entry.objects.get(id=entry_id, user=request.user)
        entry.text = data['text']
        entry.title = data['title']
        if 'mood' in data:
            entry.mood = data['mood']
        entry.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
def delete_entry(request, entry_id):
    """Delete an entry."""

    Entry.objects.filter(id=entry_id, user=request.user).delete()
    return JsonResponse({'status': 'success'})

@login_required
def toggle_bookmark(request, entry_id):
    """Switch an entry between bookmarked and unbookmarked."""

    try:
        entry = Entry.objects.get(id=entry_id, user=request.user)
        entry.bookmarked = not entry.bookmarked
        entry.save()
        return JsonResponse({'status': 'success', 'bookmarked': entry.bookmarked})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@login_prohibited
def home(request):
    """Display the application's start/home screen."""
    
    return render(request, 'home.html')


class LoginProhibitedMixin:
    """Mixin that redirects when a user is logged in."""

    redirect_when_logged_in_url = None

    def dispatch(self, *args, **kwargs):
        """Redirect when logged in, or dispatch as normal otherwise."""
        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        return super().dispatch(*args, **kwargs)

    def handle_already_logged_in(self, *args, **kwargs):
        url = self.get_redirect_when_logged_in_url()
        return redirect(url)

    def get_redirect_when_logged_in_url(self):
        """Returns the url to redirect to when not logged in."""
        if self.redirect_when_logged_in_url is None:
            raise ImproperlyConfigured(
                "LoginProhibitedMixin requires either a value for "
                "'redirect_when_logged_in_url', or an implementation for "
                "'get_redirect_when_logged_in_url()'."
            )
        else:
            return self.redirect_when_logged_in_url


class LogInView(LoginProhibitedMixin, View):
    """Display login screen and handle user login."""

    http_method_names = ['get', 'post']
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def get(self, request):
        """Display log in template."""

        self.next = request.GET.get('next') or ''
        return self.render()

    def post(self, request):
        """Handle log in attempt."""

        form = LogInForm(request.POST)
        self.next = request.POST.get('next') or settings.REDIRECT_URL_WHEN_LOGGED_IN
        user = form.get_user()
        if user is not None:
            login(request, user)
            return redirect(self.next)
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
        return self.render()

    def render(self):
        """Render log in template with blank log in form."""

        form = LogInForm()
        return render(self.request, 'log_in.html', {'form': form, 'next': self.next})


def log_out(request):
    """Log out the current user"""

    logout(request)
    return redirect('home')


class PasswordView(LoginRequiredMixin, FormView):
    """Display password change screen and handle password change requests."""

    template_name = 'password.html'
    form_class = PasswordForm

    def get_form_kwargs(self, **kwargs):
        """Pass the current user to the password change form."""

        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """Handle valid form by saving the new password."""

        form.save()
        login(self.request, self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the user after successful password change."""

        messages.add_message(self.request, messages.SUCCESS, "Password updated!")
        return reverse('dashboard')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Display user profile editing screen, and handle profile modifications."""

    model = UserForm
    template_name = "profile.html"
    form_class = UserForm

    def get_object(self):
        """Return the object (user) to be updated."""
        user = self.request.user
        return user

    def get_success_url(self):
        """Return redirect URL after successful update."""
        messages.add_message(self.request, messages.SUCCESS, "Profile updated!")
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


class SignUpView(LoginProhibitedMixin, FormView):
    """Display the sign up screen and handle sign ups."""

    form_class = SignUpForm
    template_name = "sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        # Get the user's email from the form
        email = form.cleaned_data['email']
        
        # Send a welcome email
        subject = 'Welcome to our journaling website'
        message = 'Thank you for signing up!'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)

@login_required
def create_entry_from_template(request):
    if request.method == 'POST':
        template_id = request.POST.get('template_id')
        if not template_id:
            return HttpResponse('No template selected', status=400)
        
        template = Entry.objects.get(id=template_id, user=request.user)  

        new_entry = Entry.objects.create(
            user=request.user,
            title=template.title,
            text=template.text,
        )
        return redirect('dashboard')  
    else:
        return HttpResponse('Invalid request', status=405)
        
class UpdateTemplateView(LoginRequiredMixin, View):
    """Display the templates screen."""

    def post(self, request, *args, **kwargs):
        new_title = request.POST.get('template_title')
        template_id = request.POST.get('template_id')
        new_text = request.POST.get('template_text')
        
        template_entry = get_object_or_404(Entry, id=template_id, user=request.user, is_template=True)
        template_entry.text = new_text
        template_entry.title = new_title
        template_entry.save()

        return redirect('templates')

class CreateTemplateView(LoginRequiredMixin, View):
    """Creation of the templates screen."""

    def post(self, request, *args, **kwargs):
        template_title = request.POST.get('template_title')
        template_text = request.POST.get('template_text')
        Entry.objects.create(user=request.user, text=template_text, is_template=True, title=template_title)
        return redirect('templates')

@login_required
def delete_template(request, entry_id):
    Entry.objects.filter(id=entry_id, user=request.user).delete()
    return redirect('templates')

@login_required
def create_template_view(request):
    if request.method == 'POST':
        return redirect('templates')
    else:
        return render(request, 'new_template.html')

@login_required
def edit_template_view(request, template_id):
    template = get_object_or_404(Entry, pk=template_id)
    if request.method == 'POST':
        return redirect('templates')
    else:
        context = {
            'template_id': template.id,
            'template_text': template.text,
            'template_title': template.title
        }
        return render(request, 'edit_template.html', context)

class SingleDownloadView(LoginRequiredMixin, View):
    def post(self, request):
        raw_data = request.body
        try:
            json_data = json.loads(raw_data.decode('utf-8'))
   
            # Create a BytesIO buffer to hold the PDF content
            buffer = io.BytesIO()

            # Create a PDF document
            document = SimpleDocTemplate(buffer, pagesize=A4)
            entry_title = json_data.get('entryTitle', '')
            entry_text = json_data.get('entryText', '')
            
            # Combine entry title and text for HTML parsing
            combined_html = f"<h1>{entry_title}</h1>\n{entry_text}"
           
            # Parse HTML content with BeautifulSoup
            soup = BeautifulSoup(combined_html, 'html.parser')

            plain_text = soup.get_text(separator='!;;!', strip=True)
            text = plain_text.split("!;;!")
            heading = entry_title
            styles = getSampleStyleSheet()

            # Prepare separate lists to hold paragraphs, headers, divs, and images
            content = [                
                Paragraph(heading, styles['Heading1'])
            ]

            # Extract only <div> elements
            divs = soup.find_all('div')
            for div in divs:
                content.append(str(div))

            # Extract images and add them to the content
            images = soup.find_all('img')
            for img_tag in images:
                img_url = img_tag.get('src')
                img = Image(img_url)
                content.append(str(img))  # Convert Image instance to string
                content.append('')  # Add an empty string as a placeholder for spacing

            # Generate PDF from HTML content
            pdf = generate_pdf(''.join(filter(lambda x: not isinstance(x, Spacer), map(lambda x: str(x.text) if isinstance(x, Paragraph) else str(x), content))))  # Convert Paragraph objects to strings


            # Create a FileResponse with the PDF content
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="entry.pdf"'

            return response

        except json.JSONDecodeError as e:
            # Handle JSON decoding error
            return HttpResponse(f'Error decoding JSON: {e}', status=400, content_type='text/plain')


def generate_pdf(html_content):
    # Create a BytesIO buffer to hold the PDF content
    buffer = io.BytesIO()

    # Generate PDF using xhtml2pdf
    pisa.CreatePDF(html_content, dest=buffer)

    # Get the value of the buffer
    pdf = buffer.getvalue()
    buffer.close()

    return pdf

class MultipleDownloadsView(LoginRequiredMixin,View):
    """Display the multiple PDF downloads screen."""
    
    def post(self,request):
        try:
            # entry_ids = (str(request.body.decode('utf-8')).split(','))
            json_data = json.loads(request.body.decode('utf-8'))
            entry_ids = json_data.get('entries')
            
            zip_buffer = io.BytesIO()
            

            with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                for entry_id in entry_ids:
                    int_id = int(entry_id)
                    entry= Entry.objects.get(user=request.user, id=int_id)
                    data = entry.text
                    soup = BeautifulSoup(data, 'html.parser')
                    plain_text = soup.get_text(separator='!;;!', strip=True)
                    text = plain_text.split("!;;!")
                    heading = entry.title
                    pdf_buffer = io.BytesIO()
                    document = SimpleDocTemplate(pdf_buffer, pagesize=A4)
                    styles = getSampleStyleSheet()
                    content = [
                        Paragraph(heading, styles['Heading1'])
                    ]
                    
                    for txt in text:
                        content.append(Paragraph(txt,styles['Normal']))
                        content.append(Spacer(1, 12))
                    document.build(content)
                    pdf_buffer.seek(0)
                    zip_file.writestr(f'{heading}.pdf', pdf_buffer.getvalue())

            zip_buffer.seek(0)
            response = HttpResponse(zip_buffer, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="multiple_entries.zip"'
            return response
        except json.JSONDecodeError as e:
                return HttpResponse(f'Error decoding JSON: {e}', status=400, content_type='text/plain')

@login_required
def landing(request):
    # Landing page of the app

    if request.method == "GET":
        current_user = request.user
        # Parse the given date string
        given_date = datetime.strptime(str(current_user.last_login), "%Y-%m-%d %H:%M:%S.%f%z")

        # Get the current date
        current_date = datetime.now(given_date.tzinfo)

        # Calculate the absolute difference in days
        days_difference = abs((current_date - given_date).days)
        isDaily = False
        # Check if the difference is greater than or equal to 1 day

        given_time = given_date.time()
        current_time = datetime.now().time()
        if current_time < given_time and current_date.day - given_date.day == 1:
            days_difference += 1

        if(days_difference >= 1):
            # Update the last login date
            current_user.last_login = current_date
            current_user.save()
            # Set the flag to True
            isDaily = True
        else:
            # Set the flag to False
            isDaily = False
    
        context = {
            'isDaily': isDaily
        }
    return render(request,"landing.html", context)

@require_POST
@login_required
def generate_inspiring_question(request):
    # Generate an entry prompt based on user input

    if request.method == 'POST':
        data = json.loads(request.body)
        user_input = data.get('user_input', '')
        try:
            question = generate_ai_question(user_input) # Call the AI function
            return JsonResponse({'question': question})
        except Exception as e:
            return JsonResponse({'status':'no API key'},status=404)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def templates(request):
    if request.method == "GET":
        template_entries = Entry.objects.filter(user=request.user, is_template=True)
        context = {
            'entries': template_entries
        }
        return render(request,"templates.html", context)

class AchievementView(LoginRequiredMixin, View):
    """Display the achievements and rewards screen."""

    def get(self, request):

        user = request.user

        #the achievements calculations
        achievementIDs = user.achievements.all()
        achievements = Achievement.objects.filter(id__in=achievementIDs)
        entries = Entry.objects.filter(user = request.user, is_template=False)

        #filter out the template entries
        valid_entries = []
        for entry in entries:
            if not entry.is_template:
                valid_entries.append(entry)
        
        achievements_completed = [int(len(valid_entries)) for i in range(len(achievements))]
        achievements_total = [achievement.value for achievement in achievements]
        achievements_current = [int((achievements_completed[i]/achievements_total[i])*100) for i in range(len(achievements))]

        for i in range(len(achievements)):
            achievements[i].completed = achievements_completed[i]
            achievements[i].percentage_completed = int((achievements_completed[i]/achievements_total[i])*100)
            achievements[i].save()
            achievements[i].update_is_achieved()
            achievements[i].save()
        entry_list = [entry for entry in entries]
        
        #longest streak calculation
        longest_streak = 0
        current_streak = 0
        
        for i in range(len(entry_list) -1 ):
            while i+1 < len(entry_list) and ((entry_list[i+1].date_created.date() - entry_list[i].date_created.date()).days == 1 ):
                current_streak += 1
                i=i+1
            if current_streak > longest_streak:
                longest_streak = current_streak
            current_streak = 0
        

        current_streak = 0
        #current streak calculation
        for i in range(len(entry_list)-1,0,-1 ):
            while i >= 1 and ((entry_list[i].date_created.date() - entry_list[i-1].date_created.date()).days == 1 ):
                current_streak += 1
                i=i-1
            i = 0

        
        #word count calculation
        dates =  [entry.date_created.date().year for entry in entries]
        entry_word_count = [len(entry.text.split(' ')) for entry in entries]   
        

        #mood calculation
        moods = [entry.mood for entry in entries ]

        #reminder calculation
        reminders = Reminder.objects.filter(user=request.user)
        for reminder in reminders:
            reminder_date = reminder.date_created.replace(tzinfo=None)
            current_date = datetime.now()
            days_passed = abs((reminder_date - current_date).days)
            if days_passed > reminder.value:
                subject = f"Hey! \U0001F44B {request.user.username}, remember? You wanted yourself to journal by now "
                message =f"Hi {request.user.username} \nWe hope everything is going okay ... No pressure on you but you did tell us to remind you to journal \U0001F60A \n Here's what you said to yourself :\n {reminder.description} \n Have a great day! \n Regards,\nThe Kaleidoscope Team"
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [request.user.email]
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        # Parse the given date string
        given_date = datetime.strptime(str(user.last_login), "%Y-%m-%d %H:%M:%S.%f%z")

        # Get the current date
        current_date = datetime.now(given_date.tzinfo)

        # Calculate the absolute difference in days
        days_difference = abs((current_date - given_date).days)
        isDaily = False
        # Check if the difference is greater than or equal to 1 day

        given_time = given_date.time()
        current_time = datetime.now().time()
        if current_time < given_time and current_date.day - given_date.day == 0:
            days_difference += 1

        if(days_difference >= 1):
            # Update the last login date
            user.last_login = current_date
            user.save()
            # Set the flag to True
            isDaily = True
        else:
            # Set the flag to False
            isDaily = False
        form = ReminderForm()
        context = {'form':form,
                   'reminders':reminders,
                   'entries':entries,
                    'moods':moods,
                    'year_dates':dates, 
                    'word_count':entry_word_count,
                    'current_streak':current_streak,
                    'longest_streak':longest_streak,
                    'achievements': achievements, 
                    'isDaily': isDaily}
        return render(request, 'achievements.html',context )
    
    def post(self,request):
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.save()
            messages.success(request,"Reminder created successfully!")  
        else:
            form = ReminderForm()
        return redirect('achievements')


class ArchivesView(LoginRequiredMixin,View):
    """Display the archives of all entries screen."""

    def get(self,request):
        user = request.user
        entries = Entry.objects.filter(user = request.user, is_template=False)
        temp = set([str(entry.date_created.date().strftime('%B'))   +" "+str(entry.date_created.date().year) for entry in entries])
        #months = [month for month in temp]
        months = {}
        for entry in entries:
            if str(entry.date_created.date().strftime('%B'))+" "+str(entry.date_created.date().year) in months:
                months[str(entry.date_created.date().strftime('%B'))+" "+str(entry.date_created.date().year)].append(entry)
            else:
                months[str(entry.date_created.date().strftime('%B'))+" "+str(entry.date_created.date().year)] = []
                months[str(entry.date_created.date().strftime('%B'))+" "+str(entry.date_created.date().year)].append(entry)

        return render(request,"archives.html",{"months":months})


def delete_reminder(request):
    if request.method == "POST":
        data = json.loads(request.body)
        reminder_id = data.get('id')
        reminder = Reminder.objects.filter(user=request.user, id=reminder_id)
        if reminder.exists():
            reminder.delete()
            messages.success(request, f"Reminder no.{reminder_id} has been deleted successfully!")
            return JsonResponse({'success': True},status=302)
        else:
            return JsonResponse({'error': 'Reminder not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

class JSTestViews:
    """JavaScript tests screen."""
    
    def help_button_test(request):
        return render(request, 'tests/help_button_tests.html')

    def daily_popup_test(request):
        return render(request, 'tests/daily_popup_tests.html')

    def sidebar_test(request):
        current_user = request.user
        entries = Entry.objects.filter(user=request.user).order_by('-date_created')
        current_date = datetime.now().date()
        templates = Entry.objects.filter(user=request.user, is_template=True)
        context = {
            'current_date': current_date,
            'user': current_user,
            'entries': entries,
            'templates': templates,
        }
        return render(request, 'tests/sidebar_tests.html', context)
    
    def chart_test(request):
        entries = Entry.objects.filter(user = request.user, is_template=False)
        dates =  [entry.date_created.date().year for entry in entries]
        entry_word_count = [len(entry.text.split(' ')) for entry in entries]
        moods = [entry.mood for entry in entries ]

        context = {
            'moods':moods,
            'year_dates':dates, 
            'word_count':entry_word_count,
        }
        return render(request, 'tests/charts_tests.html', context)
    
    def css_test(request):
        user = request.user
        #the achievements calculations
        achievementIDs = user.achievements.all()
        achievements = Achievement.objects.filter(id__in=achievementIDs)
        entries = Entry.objects.filter(user = request.user, is_template=False)

        #filter out the template entries
        valid_entries = []
        for entry in entries:
            if not entry.is_template:
                valid_entries.append(entry)
        
        achievements_completed = [int(len(valid_entries)) for i in range(len(achievements))]
        achievements_total = [achievement.value for achievement in achievements]
        achievements_current = [int((achievements_completed[i]/achievements_total[i])*100) for i in range(len(achievements))]

        for i in range(len(achievements)):
            achievements[i].completed = achievements_completed[i]
            achievements[i].percentage_completed = int((achievements_completed[i]/achievements_total[i])*100)
            achievements[i].save()
            achievements[i].update_is_achieved()
            achievements[i].save()
        context = {
            'achievements': achievements,
        }
        return render(request, 'tests/css_switch_tests.html', context)
    
    def journal_test(request):
        return render(request, 'tests/journal_tests.html')