// Initialize Lucide icons
lucide.createIcons();

window.onload

// Function to load experiences for a city
async function loadExperiences(cityId) {
    try {
        const response = await fetch(`/api/experiences/${cityId}`);
        const data = await response.json();
        
        // Populate Events
        const eventsList = document.getElementById('eventsList');
        eventsList.innerHTML = data.events.map(event => `
            <li class="list-item">
                <span>${event.name}</span>
                <span class="text-sm text-gray-500">${event.time}</span>
            </li>
        `).join('');

        // Populate Gems
        const gemsList = document.getElementById('gemsList');
        gemsList.innerHTML = data.gems.map(gem => `
            <li class="list-item">
                <span>${gem.name}</span>
                <span class="text-sm text-gray-500">${gem.type}</span>
            </li>
        `).join('');

        // Populate Tours
        const toursList = document.getElementById('toursList');
        toursList.innerHTML = data.tours.map(tour => `
            <li class="list-item">
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
    const searchTerm = searchInput.value.trim();
    const cityId = locationSelect.value;

    if (searchTerm === '') {
        loadExperiences(cityId);
        return;
    }

    try {
        const response = await fetch(`/api/search?q= ${searchTerm} &city_id = ${cityId}`);
        const results = await response.json();
        
        // Hide all items initially
        document.querySelectorAll('.list-item').forEach(item => {
            item.classList.add('hidden');
        });

        // Show matching items
        results.forEach(result => {
            const items = document.querySelectorAll('.list-item');
            items.forEach(item => {
                if (item.querySelector('span:first-child').textContent === result.name) {
                    item.classList.remove('hidden');
                }
            });
        });
    } catch (error) {
        console.error('Error searching experiences:', error);
    }
}

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    const locationSelect = document.getElementById('locationSelect');
    
    // Load initial experiences
    loadExperiences(locationSelect.value);
    
    // Add event listeners
    document.getElementById('searchInput').addEventListener('input', handleSearch);
    locationSelect.addEventListener('change', (e) => loadExperiences(e.target.value));
});