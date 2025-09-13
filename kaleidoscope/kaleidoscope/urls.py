from django.contrib import admin
from django.urls import path
from journal import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('password/', views.PasswordView.as_view(), name='password'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),

    path('create_entry/', views.create_entry, name='create_entry'),
    path('get_entry/<int:entry_id>', views.get_entry, name='get_entry'),
    path('update_entry/<int:entry_id>', views.update_entry, name='update_entry'),
    path('delete_entry/<int:entry_id>', views.delete_entry, name='delete_entry'),
    path('toggle_bookmark/<int:entry_id>', views.toggle_bookmark, name='toggle_bookmark'),
    path('single_download/',views.SingleDownloadView.as_view(),name='single_download'),
    path('landing/',views.landing,name="landing"),
    path('templates/',views.templates, name='templates'),

    path('create_entry_from_template/', views.create_entry_from_template, name='create_entry_from_template'),
    path('update_template/', views.UpdateTemplateView.as_view(), name='update_template'),
    path('create_template/', views.CreateTemplateView.as_view(), name='create_template'),
    path('templates/delete/<int:entry_id>/', views.delete_template, name='delete_template'),

    path('tests/help_button_test', views.JSTestViews.help_button_test, name='help_button_test'),
    path('tests/daily_popup_test', views.JSTestViews.daily_popup_test, name='daily_popup_test'),
    path('tests/sidebar_test', views.JSTestViews.sidebar_test, name='sidebar_test'),
    path('tests/chart_test', views.JSTestViews.chart_test, name='chart_test'),
    path('tests/css_test', views.JSTestViews.css_test, name='css_test'),
    path('tests/journal_test', views.JSTestViews.journal_test, name='journal_test'),

    path('create_a_new_template/', views.create_template_view, name='create_a_new_template'),
    path('edit_template/<int:template_id>', views.edit_template_view, name='edit_template'),
    path('delete_reminder/',views.delete_reminder,name='delete_reminder'),

    path('multiple_download/',views.MultipleDownloadsView.as_view(),name='multiple_download'),
    # path('dashboard/email/', views.EmailView.as_view(), name='email'),
    path('archives/', views.ArchivesView.as_view(), name='archives'),
    path('achievements/', views.AchievementView.as_view(), name='achievements'),
    path('generate_inspiring_question/', views.generate_inspiring_question, name='generate_inspiring_question'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
