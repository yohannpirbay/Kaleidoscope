document.addEventListener('DOMContentLoaded', function () {
    setupJournalSidebarFeatures();
    setupSearchFeature();
    setupFilterBookmarksFeature();
});

// Add event listeners for entry creation, deletion, and bookmarking on the sidebar
function setupJournalSidebarFeatures() {
    document.querySelector('.entries').addEventListener('click', function (event) {
        // Entry selection
        if (event.target.classList.contains('entry') || event.target.closest('.entry')) {
            const entryId = event.target.closest('.entry').getAttribute('data-entry-id');
            loadEntryContent(entryId);
        }

        // Entry deletion
        if (event.target.closest('.delete-entry-btn')) {
            const entryId = event.target.closest('.delete-entry-btn').getAttribute('data-entry-id');
            deleteEntry(entryId);
        }

        // Bookmark entry
        if (event.target.closest('.bookmark-entry-btn')) {
            const entryId = event.target.closest('.bookmark-entry-btn').getAttribute('data-entry-id');
            toggleBookmark(entryId);
        }
    });
}

// Add event listener to the search box
function setupSearchFeature() {
    const searchInput = document.querySelector('.entry-search');
    searchInput.addEventListener('input', handleSearchInput);
}

// Add event listener to the bookmarked entres button
function setupFilterBookmarksFeature() {
    document.querySelector('.bookmarked-entries').addEventListener('click', function () {
        filterBookmarkedEntries();
    });
}

// Filter sidebar entries by search
function filterEntries(searchTerm) {
    const entries = document.querySelectorAll('.entry');

    entries.forEach(entry => {
        const content = entry.querySelector('.entry-preview').textContent.toLowerCase();
        if (content.includes(searchTerm) || searchTerm === '') {
            entry.style.display = '';
        } else {
            entry.style.display = 'none';
        }
    });
}

// Filtering the entries according to the user search
function handleSearchInput() {
    const searchTerm = this.value.toLowerCase();
    filterEntries(searchTerm);
}

// Create a new entry and add it to the sidebar
function createNewEntry() {
    var form = document.createElement("form");
    form.setAttribute("method", "post");
    form.setAttribute("action", "/create_entry/");

    // CSRF Token is needed for POST requests
    var csrfInput = document.createElement("input");
    csrfInput.setAttribute("type", "hidden");
    csrfInput.setAttribute("name", "csrfmiddlewaretoken");
    csrfInput.setAttribute("value", getCookie('csrftoken'));
    form.appendChild(csrfInput);

    document.body.appendChild(form);
    form.submit();
}

// Create a new entry only for testing purposes
function createNewEntryTest() {
    var form = document.createElement("form");
    form.setAttribute("id", "create-entry-form-test");
    form.setAttribute("method", "post");
    form.setAttribute("action", "/create_entry/");

    // CSRF Token is needed for POST requests
    var csrfInput = document.createElement("input");
    csrfInput.setAttribute("id", "csrf-input-test");
    csrfInput.setAttribute("type", "hidden");
    csrfInput.setAttribute("name", "csrfmiddlewaretoken");
    csrfInput.setAttribute("value", getCookie('csrftoken'));
    form.appendChild(csrfInput);

    document.body.appendChild(form);
}

// Load the selected entry
function loadEntryContent(entryId) {
    const entryContent = document.querySelector('.entry-content');
    entryContent.setAttribute('data-current-entry-id', entryId);

    fetch(`/get_entry/${entryId}`)
        .then(response => response.json())
        .then(data => {
            const entryTitle = document.getElementById("entry-title-edit");
            entryTitle.innerHTML = "<h1>" + data.title + "</h1>";
            entryContent.innerHTML = data.text.replace(/\n/g, '<br>');

            // Logs the current mood
            document.getElementById('mood-value').value = data.mood;

            // Handle save button click
            const saveButton = document.getElementById('save-entry-btn');
            saveButton.onclick = function() {
                saveEntry(entryId);
            };

            highlightSelectedEntry(entryId);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


// Highlight the selected entry on the sidebar
function highlightSelectedEntry(entryId){
    // Prevously selected entry is unselected
    document.querySelectorAll('.entry').forEach(function(en) {
        en.classList.remove('selected');
    });

    // Selected class makes selected entry highlighted
    const selectedEntry = document.querySelector(`.entry[data-entry-id="${entryId}"]`);
    if (selectedEntry) {
        selectedEntry.classList.add('selected');
    }
}

// Delete an entry
function deleteEntry(entryId) {
    const csrftoken = getCookie('csrftoken');

    fetch(`/delete_entry/${entryId}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ entry_id: entryId })
    })
        .then(response => {
            if (response.ok) {
                document.querySelector(`.entry[data-entry-id="${entryId}"]`).remove();

                // Get the ID of the currently loaded entry
                const currentLoadedEntryId = document.querySelector('.entry-content').getAttribute('data-current-entry-id');

                // Check if the deleted entry is the one currently loaded
                if (entryId === currentLoadedEntryId) {
                    const remainingEntries = document.querySelectorAll('.entry');
                    if (remainingEntries.length > 0) {
                        // If there are remaining entries, load the first one
                        const firstEntryId = remainingEntries[0].getAttribute('data-entry-id');
                        loadEntryContent(firstEntryId);
                    } else {
                        // Otherwise redirect to the dashboard
                        window.location.href = "/dashboard/";
                    }
                }
            } else {
                console.error("Failed to delete entry");
            }
        })
        .catch(error => {
            console.error(error);
        });
}

// Modified delete entry function for testing purposes
function deleteEntryTest(entryId) {

    document.querySelector(`.entry[data-entry-id="${entryId}"]`).remove();
    // Get the ID of the currently loaded entry
}


// Toggle between bookmarking and unbookmarking an entry
function toggleBookmark(entryId) {
    const csrftoken = getCookie('csrftoken');
    const bookmarkBtn = document.querySelector(`.bookmark-entry-btn[data-entry-id="${entryId}"] i`);

    // Toggle the icon before the fetch request
    const isBookmarked = bookmarkBtn.classList.contains('bi-bookmark-fill');
    bookmarkBtn.className = isBookmarked ? 'bi bi-bookmark' : 'bi bi-bookmark-fill';

    fetch(`/toggle_bookmark/${entryId}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ entry_id: entryId })
    })
        .then(response => response.json())
        .then(data => {
            // Correctly updates the icon based on actual server response if needed
            if (data.status !== 'success') {
                // If the toggle failed, revert the icon change
                bookmarkBtn.className = isBookmarked ? 'bi bi-bookmark-fill' : 'bi bi-bookmark';
                console.error("Failed to toggle bookmark", data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            // Revert the icon change if there's an error
            bookmarkBtn.className = isBookmarked ? 'bi bi-bookmark-fill' : 'bi bi-bookmark';
        });
}

// Show only the bookmarked entries
function filterBookmarkedEntries() {
    const bookmarkedButton = document.querySelector('.bookmarked-entries button');
    const showBookmarks = bookmarkedButton.getAttribute('data-show-bookmarks') === 'true';

    // Toggle the data-showing-bookmarked attribute
    bookmarkedButton.setAttribute('data-show-bookmarks', !showBookmarks);

    if (!showBookmarks) {
        // Show only bookmarked entries
        [...document.querySelectorAll('.entry')].forEach(entry => {
            const isBookmarked = entry.querySelector('.bookmark-entry-btn i').classList.contains('bi-bookmark-fill'); // Adjust based on your actual bookmark icon class
            if (!isBookmarked) {
                entry.style.display = 'none';
            } else {
                entry.style.display = '';
            }
        });
    } else {
        // Show all entries
        [...document.querySelectorAll('.entry')].forEach(entry => {
            entry.style.display = '';
        });
    }
}

// Updates the entry's title on the sidebar after it is updated
function updateSideBar(updatedTitle, updatedText, entryId) {
    const title = updatedTitle;
    const sidebarEntry = document.querySelector(`.entry[data-entry-id="${entryId}"]`);
    if (sidebarEntry) {

        const entryPreview = sidebarEntry.querySelector('.entry-preview');
        const entryDate = sidebarEntry.querySelector('.entry-date').outerHTML;

        if (entryPreview) {
            entryPreview.innerHTML = `${title} ${entryDate}`;
        }
    }
}