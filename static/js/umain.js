// Initialize Lucide icons
lucide.createIcons();

// Function to load experiences for a city
async function loadExperiences(cityId) {
    try {
        const response = await fetch(`/api/experiences/${cityId}`);
        const data = await response.json();
        
        // Populate Events
        const eventsList = document.getElementById('eventsList');
        eventsList.innerHTML = data.events.map(event => `
            <li class="list-item" data-type="event">
                <span>${event.name}</span>
                <span class="text-sm text-gray-500">${event.time}</span>
            </li>
        `).join('');

        // Populate Gems
        const gemsList = document.getElementById('gemsList');
        gemsList.innerHTML = data.gems.map(gem => `
            <li class="list-item" data-type="gem">
                <span>${gem.name}</span>
                <span class="text-sm text-gray-500">${gem.type}</span>
            </li>
        `).join('');

        // Populate Tours
        const toursList = document.getElementById('toursList');
        toursList.innerHTML = data.tours.map(tour => `
            <li class="list-item" data-type="tour">
                <span>${tour.name}</span>
                <span class="text-sm text-gray-500">${tour.duration}</span>
            </li>
        `).join('');

        // Reinitialize Lucide icons
        lucide.createIcons();
    } catch (error) {
        console.error('Error loading experiences:', error);
    }
}

// Search functionality
async function handleSearch() {
    const searchInput = document.getElementById('searchInput');
    const locationSelect = document.getElementById('locationSelect');
    const searchTerm = searchInput.value.trim().toLowerCase();
    const cityId = locationSelect.value;

    if (searchTerm === '') {
        // If search is empty, load all experiences
        loadExperiences(cityId);
        return;
    }

    try {
        const response = await fetch(`/api/search?q=${encodeURIComponent(searchTerm)}&city_id=${cityId}`);
        const results = await response.json();
        
        // Show all items initially
        document.querySelectorAll('.list-item').forEach(item => {
            item.style.display = 'none';
        });

        // Process search results and show matching items
        results.forEach(result => {
            let listContainer;
            switch (result.type) {
                case 'local_event':
                    listContainer = document.getElementById('eventsList');
                    break;
                case 'hidden_gem':
                    listContainer = document.getElementById('gemsList');
                    break;
                case 'walking_tour':
                    listContainer = document.getElementById('toursList');
                    break;
            }

            if (listContainer) {
                const items = listContainer.querySelectorAll('.list-item');
                items.forEach(item => {
                    const itemName = item.querySelector('span:first-child').textContent.toLowerCase();
                    if (itemName.includes(searchTerm)) {
                        item.style.display = 'flex';
                    }
                });
            }
        });

        // If no results found in a category, display "No results found"
        ['eventsList', 'gemsList', 'toursList'].forEach(listId => {
            const container = document.getElementById(listId);
            const visibleItems = container.querySelectorAll('.list-item[style="display: flex;"]');
            if (visibleItems.length === 0) {
                container.innerHTML = '<li class="list-item no-results">No results found</li>';
            }
        });

    } catch (error) {
        console.error('Error searching experiences:', error);
    }
}

// Debounce function to limit API calls
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    const locationSelect = document.getElementById('locationSelect');
    const searchInput = document.getElementById('searchInput');
    
    // Load initial experiences
    loadExperiences(locationSelect.value);
    
    // Add event listeners with debounced search
    const debouncedSearch = debounce(handleSearch, 300);
    searchInput.addEventListener('input', debouncedSearch);
    locationSelect.addEventListener('change', (e) => {
        searchInput.value = ''; // Clear search on location change
        loadExperiences(e.target.value);
    });
});