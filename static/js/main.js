// Initialize Lucide icons
lucide.createIcons();

// Function to load experiences for a city
async function loadExperiences(cityId) {
    try {
        const response = await fetch(`/api/experiences/${cityId}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        
        // Populate Events
        const eventsList = document.getElementById('eventsList');
        eventsList.innerHTML = data.events.length > 0 
            ? data.events.map(event => `
                <li class="list-item" data-type="event">
                    <span>${event.name}</span>
                    <span class="text-sm text-gray-500">${event.time}</span>
                </li>
            `).join('')
            : '<li class="list-item">No events found</li>';

        // Populate Gems
        const gemsList = document.getElementById('gemsList');
        gemsList.innerHTML = data.gems.length > 0
            ? data.gems.map(gem => `
                <li class="list-item" data-type="gem">
                    <span>${gem.name}</span>
                    <span class="text-sm text-gray-500">${gem.type}</span>
                </li>
            `).join('')
            : '<li class="list-item">No hidden gems found</li>';

        // Populate Tours
        const toursList = document.getElementById('toursList');
        toursList.innerHTML = data.tours.length > 0
            ? data.tours.map(tour => `
                <li class="list-item" data-type="tour">
                    <span>${tour.name}</span>
                    <span class="text-sm text-gray-500">${tour.duration}</span>
                </li>
            `).join('')
            : '<li class="list-item">No walking tours found</li>';

        // Reinitialize Lucide icons
        lucide.createIcons();
    } catch (error) {
        console.error('Error loading experiences:', error);
        document.querySelectorAll('.card-list').forEach(list => {
            list.innerHTML = '<li class="list-item error-state">Failed to load data</li>';
        });
    }
}

// Search functionality
async function handleSearch() {
    const searchInput = document.getElementById('searchInput');
    const locationSelect = document.getElementById('locationSelect');
    const searchTerm = searchInput.value.trim();
    const cityId = locationSelect.value;

    if (searchTerm === '') {
        loadExperiences(cityId);
        return;
    }

    try {
        const response = await fetch(`/api/search?q=${encodeURIComponent(searchTerm)}&city_id=${cityId}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const results = await response.json();
        
        // Reset all lists first
        document.getElementById('eventsList').innerHTML = '';
        document.getElementById('gemsList').innerHTML = '';
        document.getElementById('toursList').innerHTML = '';
        
        const eventItems = [];
        const gemItems = [];
        const tourItems = [];
        
        // Sort results by type
        results.forEach(result => {
            if (result.type === 'local_event') {
                eventItems.push(`
                    <li class="list-item">
                        <span>${result.name}</span>
                        <span class="text-sm text-gray-500">${result.details.time || 'TBD'}</span>
                    </li>
                `);
            } else if (result.type === 'hidden_gem') {
                gemItems.push(`
                    <li class="list-item">
                        <span>${result.name}</span>
                        <span class="text-sm text-gray-500">${result.details.type || 'Unknown'}</span>
                    </li>
                `);
            } else if (result.type === 'walking_tour') {
                tourItems.push(`
                    <li class="list-item">
                        <span>${result.name}</span>
                        <span class="text-sm text-gray-500">${result.details.distance || 'Unknown'}</span>
                    </li>
                `);
            }
        });
        
        // Update lists with search results or no results message
        document.getElementById('eventsList').innerHTML = 
            eventItems.length > 0 ? eventItems.join('') : '<li class="list-item">No matching events</li>';
        document.getElementById('gemsList').innerHTML = 
            gemItems.length > 0 ? gemItems.join('') : '<li class="list-item">No matching gems</li>';
        document.getElementById('toursList').innerHTML = 
            tourItems.length > 0 ? tourItems.join('') : '<li class="list-item">No matching tours</li>';
            
        // Reinitialize icons
        lucide.createIcons();
    } catch (error) {
        console.error('Error searching experiences:', error);
    }
}

// Debounce function for search input
function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
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
