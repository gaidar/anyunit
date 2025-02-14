// static/js/category.js
class CategoryPage {
    constructor() {
        this.filterButtons = document.querySelectorAll('[data-filter]');
        this.conversionRows = document.querySelectorAll('.conversion-table tbody tr');
        this.searchInput = null;

        this.initializeSearch();
        this.initializeFilters();
        this.initializeTableSorting();
        this.initializeResponsiveTable();
    }

    initializeSearch() {
        // Create search input
        this.searchInput = document.createElement('input');
        this.searchInput.type = 'text';
        this.searchInput.className = 'form-control conversion-search';
        this.searchInput.placeholder = 'Search conversions...';
        this.searchInput.setAttribute('aria-label', 'Search conversions');

        const filtersContainer = document.querySelector('.conversion-filters');
        if (filtersContainer) {
            filtersContainer.appendChild(this.searchInput);

            // Add search functionality with debounce
            let debounceTimeout;
            this.searchInput.addEventListener('input', (e) => {
                clearTimeout(debounceTimeout);
                debounceTimeout = setTimeout(() => {
                    this.handleSearch(e.target.value);
                }, 300);
            });
        }
    }

    initializeFilters() {
        this.filterButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                this.handleFilter(e.target);
            });
        });
    }

    initializeTableSorting() {
        const tableHeaders = document.querySelectorAll('.conversion-table th');
        tableHeaders.forEach((header, index) => {
            if (header.textContent.trim() !== 'Convert') {
                header.style.cursor = 'pointer';
                header.setAttribute('role', 'button');
                header.setAttribute('aria-sort', 'none');
                header.addEventListener('click', () => this.sortTable(index));
            }
        });
    }

    initializeResponsiveTable() {
        // Add horizontal scroll hint for mobile
        const tableWrapper = document.querySelector('.table-responsive');
        if (tableWrapper && window.innerWidth < 768) {
            const scrollHint = document.createElement('div');
            scrollHint.className = 'scroll-hint';
            scrollHint.textContent = 'Scroll horizontally to see more →';
            tableWrapper.parentNode.insertBefore(scrollHint, tableWrapper);

            // Remove hint after user has scrolled
            tableWrapper.addEventListener('scroll', () => {
                scrollHint.style.display = 'none';
            }, { once: true });
        }
    }

    handleSearch(searchTerm) {
        searchTerm = searchTerm.toLowerCase();
        let visibleCount = 0;

        this.conversionRows.forEach(row => {
            const fromUnit = row.querySelector('td:first-child').textContent.toLowerCase();
            const toUnit = row.querySelector('td:nth-child(2)').textContent.toLowerCase();

            const isVisible = fromUnit.includes(searchTerm) || toUnit.includes(searchTerm);
            row.style.display = isVisible ? '' : 'none';
            if (isVisible) visibleCount++;
        });

        this.updateNoResultsMessage(visibleCount, searchTerm);
    }

    handleFilter(button) {
        // Update active state
        this.filterButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');

        const filterValue = button.dataset.filter;
        let visibleCount = 0;

        this.conversionRows.forEach(row => {
            const fromType = row.dataset.fromType;
            const toType = row.dataset.toType;

            const isVisible = filterValue === 'all' ||
                fromType === filterValue ||
                toType === filterValue;

            row.style.display = isVisible ? '' : 'none';
            if (isVisible) visibleCount++;
        });

        // Clear search when filtering
        if (this.searchInput) {
            this.searchInput.value = '';
        }
    }

    sortTable(columnIndex) {
        const table = document.querySelector('.conversion-table');
        const tbody = table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        const header = table.querySelectorAll('th')[columnIndex];

        // Toggle sort direction
        const isAscending = header.getAttribute('aria-sort') !== 'ascending';

        // Update aria-sort attributes
        table.querySelectorAll('th').forEach(th => th.setAttribute('aria-sort', 'none'));
        header.setAttribute('aria-sort', isAscending ? 'ascending' : 'descending');

        // Sort rows
        rows.sort((a, b) => {
            const aValue = a.querySelectorAll('td')[columnIndex].textContent;
            const bValue = b.querySelectorAll('td')[columnIndex].textContent;
            return isAscending ?
                aValue.localeCompare(bValue) :
                bValue.localeCompare(aValue);
        });

        // Reorder rows
        rows.forEach(row => tbody.appendChild(row));
    }

    updateNoResultsMessage(visibleCount, searchTerm) {
        let noResultsMsg = document.getElementById('noResults');

        if (visibleCount === 0) {
            if (!noResultsMsg) {
                noResultsMsg = document.createElement('div');
                noResultsMsg.id = 'noResults';
                noResultsMsg.className = 'alert alert-info mt-3';
                noResultsMsg.setAttribute('role', 'alert');

                const table = document.querySelector('.conversion-table');
                table.parentNode.insertBefore(noResultsMsg, table.nextSibling);
            }

            noResultsMsg.innerHTML = `
                <p class="mb-0">No matching conversions found for "${searchTerm}"</p>
                <small>Try different keywords or <a href="#" class="alert-link reset-search">clear search</a></small>
            `;

            // Add reset search functionality
            noResultsMsg.querySelector('.reset-search').addEventListener('click', (e) => {
                e.preventDefault();
                if (this.searchInput) {
                    this.searchInput.value = '';
                    this.handleSearch('');
                }
            });
        } else if (noResultsMsg) {
            noResultsMsg.remove();
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new CategoryPage();
});