// static/js/search.js
class UnitSearch {
    constructor() {
        this.searchInput = document.getElementById('unitSearch');
        this.searchResults = document.getElementById('searchResults');
        this.categoryGrid = document.getElementById('category-grid');
        this.debounceTimeout = null;
        this.searchCache = new Map();

        if (this.searchInput) {
            this.initializeSearch();
        }
    }

    initializeSearch() {
        // Add input event listener with debounce
        this.searchInput.addEventListener('input', (e) => {
            clearTimeout(this.debounceTimeout);
            this.debounceTimeout = setTimeout(() => {
                this.handleSearch(e.target.value);
            }, 300);
        });

        // Add clear search functionality
        this.searchInput.addEventListener('search', () => {
            this.handleSearch('');
        });
    }

    async handleSearch(searchTerm) {
        searchTerm = searchTerm.toLowerCase().trim();

        // Reset to default view if search is empty
        if (!searchTerm) {
            this.resetSearch();
            return;
        }

        // Check cache first
        if (this.searchCache.has(searchTerm)) {
            this.displayResults(this.searchCache.get(searchTerm), searchTerm);
            return;
        }

        try {
            const results = await this.performSearch(searchTerm);
            this.searchCache.set(searchTerm, results);
            this.displayResults(results, searchTerm);
        } catch (error) {
            console.error('Search error:', error);
            this.showError('An error occurred while searching. Please try again.');
        }
    }

    async performSearch(searchTerm) {
        // Search in categories
        const categoryCards = document.querySelectorAll('.category-item');
        const categories = [];
        categoryCards.forEach(card => {
            const category = {
                id: card.dataset.category,
                title: card.querySelector('.card-title').textContent,
                description: card.querySelector('.card-text').textContent,
                icon: card.querySelector('.category-icon').textContent
            };

            if (this.matchesSearch(category, searchTerm)) {
                categories.push(category);
            }
        });

        // Fetch additional unit data from the server
        try {
            const response = await fetch(`/api/search?q=${encodeURIComponent(searchTerm)}`);
            if (!response.ok) throw new Error('Search request failed');
            const data = await response.json();

            return {
                categories: categories,
                units: data.units || [],
                popularConversions: data.popularConversions || []
            };
        } catch (error) {
            console.error('API search error:', error);
            // Return just category results if API fails
            return {
                categories: categories,
                units: [],
                popularConversions: []
            };
        }
    }

    matchesSearch(item, searchTerm) {
        return item.title.toLowerCase().includes(searchTerm) ||
            item.description.toLowerCase().includes(searchTerm) ||
            item.id.toLowerCase().includes(searchTerm);
    }

    displayResults(results, searchTerm) {
        // Hide category grid and show search results
        if (this.categoryGrid) {
            this.categoryGrid.style.display = 'none';
        }

        // Create or clear search results container
        if (!this.searchResults) {
            this.searchResults = document.createElement('div');
            this.searchResults.id = 'searchResults';
            this.categoryGrid.parentNode.insertBefore(this.searchResults, this.categoryGrid);
        } else {
            this.searchResults.innerHTML = '';
        }

        const hasResults = results.categories.length > 0 ||
            results.units.length > 0 ||
            results.popularConversions.length > 0;

        if (!hasResults) {
            this.showNoResults(searchTerm);
            return;
        }

        // Build results HTML
        let resultsHTML = '';

        // Categories section
        if (results.categories.length > 0) {
            resultsHTML += this.buildCategoriesSection(results.categories);
        }

        // Units section
        if (results.units.length > 0) {
            resultsHTML += this.buildUnitsSection(results.units);
        }

        // Popular conversions section
        if (results.popularConversions.length > 0) {
            resultsHTML += this.buildPopularConversionsSection(results.popularConversions);
        }

        this.searchResults.innerHTML = resultsHTML;
    }

    buildCategoriesSection(categories) {
        return `
            <div class="search-section">
                <h2 class="h5 mb-3">Categories</h2>
                <div class="row g-3">
                    ${categories.map(category => `
                        <div class="col-12 col-md-6 col-lg-4">
                            <div class="card h-100">
                                <div class="card-body">
                                    <div class="category-icon mb-2">${category.icon}</div>
                                    <h3 class="h6 card-title">${category.title}</h3>
                                    <p class="card-text small">${category.description}</p>
                                    <a href="/convert/${category.id}" class="btn btn-primary btn-sm">View Conversions</a>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    buildUnitsSection(units) {
        return `
            <div class="search-section mt-4">
                <h2 class="h5 mb-3">Units</h2>
                <div class="row g-3">
                    ${units.map(unit => `
                        <div class="col-12 col-md-6 col-lg-4">
                            <div class="card h-100">
                                <div class="card-body">
                                    <h3 class="h6 card-title">${unit.name} (${unit.symbol})</h3>
                                    <p class="card-text small">Category: ${unit.category}</p>
                                    <a href="/convert/${unit.category_id}#${unit.id}" 
                                       class="btn btn-outline-primary btn-sm">Convert</a>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    buildPopularConversionsSection(conversions) {
        return `
            <div class="search-section mt-4">
                <h2 class="h5 mb-3">Popular Conversions</h2>
                <div class="row g-3">
                    ${conversions.map(conv => `
                        <div class="col-12 col-md-6 col-lg-4">
                            <div class="card h-100">
                                <div class="card-body">
                                    <h3 class="h6 card-title">${conv.title}</h3>
                                    <a href="${conv.url}" class="btn btn-outline-primary btn-sm">Convert Now</a>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    showNoResults(searchTerm) {
        this.searchResults.innerHTML = `
            <div class="no-results text-center py-5">
                <h2 class="h5 mb-3">No Results Found</h2>
                <p class="text-muted">No matches found for "${searchTerm}"</p>
                <button class="btn btn-outline-primary mt-3" onclick="this.resetSearch()">
                    Clear Search
                </button>
            </div>
        `;
    }

    showError(message) {
        this.searchResults.innerHTML = `
            <div class="alert alert-danger" role="alert">
                ${message}
            </div>
        `;
    }

    resetSearch() {
        // Clear search input
        if (this.searchInput) {
            this.searchInput.value = '';
        }

        // Hide search results
        if (this.searchResults) {
            this.searchResults.style.display = 'none';
        }

        // Show category grid
        if (this.categoryGrid) {
            this.categoryGrid.style.display = '';
        }
    }
}

// Initialize search when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new UnitSearch();
});