/**
 * Main JavaScript file for the Drug Tariff Master web interface
 */

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');
    const recordTypeFilter = document.getElementById('recordTypeFilter');
    const resultsSection = document.getElementById('resultsSection');
    const noResultsSection = document.getElementById('noResultsSection');
    const statisticsSection = document.getElementById('statisticsSection');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const resultsCount = document.getElementById('resultsCount');
    const resultsTableBody = document.getElementById('resultsTableBody');
    const resultsPagination = document.getElementById('resultsPagination');
    const statsLink = document.getElementById('statsLink');
    const statsContent = document.getElementById('statsContent');
    const exportCsvBtn = document.getElementById('exportCsvBtn');
    const printResultsBtn = document.getElementById('printResultsBtn');
    
    // State
    let currentSearch = '';
    let currentPage = 1;
    let resultsPerPage = 50;
    let currentRecordType = '';
    let searchResults = [];
    let totalResults = 0;
    
    // Event Listeners
    searchButton.addEventListener('click', performSearch);
    searchInput.addEventListener('keyup', function(event) {
        if (event.key === 'Enter') {
            performSearch();
        }
    });
    recordTypeFilter.addEventListener('change', function() {
        if (currentSearch) {
            performSearch();
        }
    });
    statsLink.addEventListener('click', function(e) {
        e.preventDefault();
        showStatistics();
    });
    exportCsvBtn.addEventListener('click', exportResultsAsCsv);
    printResultsBtn.addEventListener('click', printResults);
    
    // Initialize
    checkForUrlParams();
    
    /**
     * Check URL parameters for search term and filter
     */
    function checkForUrlParams() {
        const urlParams = new URLSearchParams(window.location.search);
        
        if (urlParams.has('q')) {
            const q = urlParams.get('q');
            searchInput.value = q;
            
            if (urlParams.has('type')) {
                recordTypeFilter.value = urlParams.get('type');
            }
            
            performSearch();
        }
    }
    
    /**
     * Perform search with current parameters
     */
    function performSearch() {
        const searchTerm = searchInput.value.trim();
        const recordType = recordTypeFilter.value;
        
        if (!searchTerm) {
            alert('Please enter a search term');
            searchInput.focus();
            return;
        }
        
        // Update state
        currentSearch = searchTerm;
        currentPage = 1;
        currentRecordType = recordType;
        
        // Update URL without reloading the page
        updateUrlParams();
        
        // Show loading indicator
        showLoading();
        
        // Hide sections
        hideAllSections();
        
        // Fetch results
        fetchSearchResults(searchTerm, recordType, resultsPerPage, currentPage);
    }
    
    /**
     * Update URL parameters to reflect current search
     */
    function updateUrlParams() {
        const url = new URL(window.location);
        url.searchParams.set('q', currentSearch);
        
        if (currentRecordType) {
            url.searchParams.set('type', currentRecordType);
        } else {
            url.searchParams.delete('type');
        }
        
        window.history.pushState({}, '', url);
    }
    
    /**
     * Fetch search results from API
     */
    function fetchSearchResults(searchTerm, recordType, limit, page) {
        // Build query URL
        let url = `/api/search?q=${encodeURIComponent(searchTerm)}&limit=${limit}&page=${page}`;
        
        if (recordType) {
            url += `&type=${recordType}`;
        }
        
        // Fetch results
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                hideLoading();
                
                if (data.success) {
                    searchResults = data.results;
                    totalResults = data.total;
                    
                    if (searchResults.length > 0) {
                        displayResults(searchResults, data.total, data.page, data.limit);
                    } else {
                        showNoResults();
                    }
                } else {
                    showNoResults();
                    console.error('Error:', data.message);
                }
            })
            .catch(error => {
                hideLoading();
                showNoResults();
                console.error('Error fetching search results:', error);
            });
    }
    
    /**
     * Display search results in the table
     */
    function displayResults(results, total, page, limit) {
        // Show results section
        resultsSection.classList.remove('d-none');
        
        // Update results count
        resultsCount.textContent = `${total} results found for "${currentSearch}"`;
        
        // Clear previous results
        resultsTableBody.innerHTML = '';
        
        // Add results to table
        results.forEach(result => {
            const row = document.createElement('tr');
            
            // Format price as currency if available
            let priceDisplay = '';
            if (result.price) {
                // Price is stored in pence, convert to pounds
                const pounds = (result.price / 100).toFixed(2);
                priceDisplay = `£${pounds}`;
            } else {
                priceDisplay = '-';
            }
            
            // Create type badge with appropriate color
            const typeLower = result.type.toLowerCase();
            const typeBadge = `<span class="badge bg-${typeLower}">${result.type}</span>`;
            
            row.innerHTML = `
                <td>${typeBadge}</td>
                <td>${highlightSearchTerm(result.name, currentSearch)}</td>
                <td>${result.supplier || '-'}</td>
                <td class="price">${priceDisplay}</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary view-details" 
                            data-type="${result.type}" 
                            data-id="${result.id}">
                        <i class="fas fa-info-circle"></i> Details
                    </button>
                </td>
            `;
            
            resultsTableBody.appendChild(row);
        });
        
        // Add event listeners to detail buttons
        document.querySelectorAll('.view-details').forEach(button => {
            button.addEventListener('click', function() {
                const type = this.getAttribute('data-type');
                const id = this.getAttribute('data-id');
                showProductDetails(type, id);
            });
        });
        
        // Create pagination
        createPagination(total, page, limit);
    }
    
    /**
     * Create pagination controls
     */
    function createPagination(total, currentPage, limit) {
        resultsPagination.innerHTML = '';
        
        const totalPages = Math.ceil(total / limit);
        
        if (totalPages <= 1) {
            return;
        }
        
        // Add previous button
        const prevLi = document.createElement('li');
        prevLi.className = `page-item ${currentPage === 1 ? 'disabled' : ''}`;
        prevLi.innerHTML = `
            <a class="page-link" href="#" aria-label="Previous">
                <span aria-hidden="true">&laquo;</span>
            </a>
        `;
        if (currentPage > 1) {
            prevLi.querySelector('a').addEventListener('click', function(e) {
                e.preventDefault();
                goToPage(currentPage - 1);
            });
        }
        resultsPagination.appendChild(prevLi);
        
        // Determine which page numbers to show
        let startPage = Math.max(1, currentPage - 2);
        let endPage = Math.min(totalPages, startPage + 4);
        
        // Adjust startPage if endPage is maxed out
        if (endPage === totalPages) {
            startPage = Math.max(1, endPage - 4);
        }
        
        // Add page numbers
        for (let i = startPage; i <= endPage; i++) {
            const pageLi = document.createElement('li');
            pageLi.className = `page-item ${i === currentPage ? 'active' : ''}`;
            pageLi.innerHTML = `<a class="page-link" href="#">${i}</a>`;
            
            if (i !== currentPage) {
                pageLi.querySelector('a').addEventListener('click', function(e) {
                    e.preventDefault();
                    goToPage(i);
                });
            }
            
            resultsPagination.appendChild(pageLi);
        }
        
        // Add next button
        const nextLi = document.createElement('li');
        nextLi.className = `page-item ${currentPage === totalPages ? 'disabled' : ''}`;
        nextLi.innerHTML = `
            <a class="page-link" href="#" aria-label="Next">
                <span aria-hidden="true">&raquo;</span>
            </a>
        `;
        if (currentPage < totalPages) {
            nextLi.querySelector('a').addEventListener('click', function(e) {
                e.preventDefault();
                goToPage(currentPage + 1);
            });
        }
        resultsPagination.appendChild(nextLi);
    }
    
    /**
     * Go to a specific page of results
     */
    function goToPage(page) {
        currentPage = page;
        showLoading();
        fetchSearchResults(currentSearch, currentRecordType, resultsPerPage, page);
        window.scrollTo(0, 0);
    }
    
    /**
     * Show product details in modal
     */
    function showProductDetails(type, id) {
        const modal = new bootstrap.Modal(document.getElementById('productDetailModal'));
        const modalTitle = document.getElementById('productDetailTitle');
        const modalBody = document.getElementById('productDetailBody');
        
        // Reset modal content and show loading spinner
        modalTitle.textContent = `${type} Details`;
        modalBody.innerHTML = `
            <div class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p>Loading product details...</p>
            </div>
        `;
        
        // Show modal
        modal.show();
        
        // Fetch product details
        fetch(`/api/product/${type}/${id}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    displayProductDetails(data.product, data.additional_info, type);
                } else {
                    modalBody.innerHTML = `<div class="alert alert-danger">${data.message}</div>`;
                }
            })
            .catch(error => {
                modalBody.innerHTML = `<div class="alert alert-danger">Error loading product details: ${error.message}</div>`;
                console.error('Error fetching product details:', error);
            });
    }
    
    /**
     * Display product details in modal
     */
    function displayProductDetails(product, additionalInfo, type) {
        const modalBody = document.getElementById('productDetailBody');
        
        // Format product details based on type
        let detailsHtml = '';
        
        // Main product info section
        detailsHtml += `<div class="product-detail-section">`;
        detailsHtml += `<h6><span class="badge bg-${type.toLowerCase()}">${type}</span> Information</h6>`;
        detailsHtml += `<div class="row">`;
        
        // Add all fields from product object
        Object.keys(product).forEach(key => {
            let value = product[key];
            
            // Format value for display
            if (key === 'PRICE' && value) {
                value = `£${(value / 100).toFixed(2)}`;
            } else if (value === null || value === '') {
                value = '-';
            }
            
            // Skip internal or redundant fields
            if (['ID', 'rowid'].includes(key)) {
                return;
            }
            
            detailsHtml += `
                <div class="col-md-6 mb-2">
                    <div class="detail-label">${formatFieldName(key)}</div>
                    <div class="detail-value">${value}</div>
                </div>
            `;
        });
        
        detailsHtml += `</div></div>`;
        
        // Add additional info sections
        if (additionalInfo) {
            Object.keys(additionalInfo).forEach(infoType => {
                const info = additionalInfo[infoType];
                
                if (Array.isArray(info)) {
                    // Array of related items
                    detailsHtml += `<div class="product-detail-section">`;
                    detailsHtml += `<h6>Related ${infoType.toUpperCase()} (${info.length})</h6>`;
                    
                    if (info.length > 0) {
                        detailsHtml += `<div class="table-responsive">`;
                        detailsHtml += `<table class="table table-sm table-striped">`;
                        detailsHtml += `<thead><tr>`;
                        
                        // Get column headers from first item
                        const headerKeys = Object.keys(info[0]).filter(key => !['rowid', 'ID'].includes(key));
                        headerKeys.forEach(key => {
                            detailsHtml += `<th>${formatFieldName(key)}</th>`;
                        });
                        
                        detailsHtml += `</tr></thead>`;
                        detailsHtml += `<tbody>`;
                        
                        // Add rows
                        info.forEach(item => {
                            detailsHtml += `<tr>`;
                            headerKeys.forEach(key => {
                                let value = item[key];
                                
                                // Format value for display
                                if (key === 'PRICE' && value) {
                                    value = `£${(value / 100).toFixed(2)}`;
                                } else if (value === null || value === '') {
                                    value = '-';
                                }
                                
                                detailsHtml += `<td>${value}</td>`;
                            });
                            detailsHtml += `</tr>`;
                        });
                        
                        detailsHtml += `</tbody></table></div>`;
                    } else {
                        detailsHtml += `<p>No related ${infoType} found.</p>`;
                    }
                    
                    detailsHtml += `</div>`;
                } else {
                    // Single related item
                    detailsHtml += `<div class="product-detail-section">`;
                    detailsHtml += `<h6>Related ${infoType.toUpperCase()} Information</h6>`;
                    detailsHtml += `<div class="row">`;
                    
                    // Add all fields from info object
                    Object.keys(info).forEach(key => {
                        let value = info[key];
                        
                        // Format value for display
                        if (key === 'PRICE' && value) {
                            value = `£${(value / 100).toFixed(2)}`;
                        } else if (value === null || value === '') {
                            value = '-';
                        }
                        
                        // Skip internal or redundant fields
                        if (['ID', 'rowid'].includes(key)) {
                            return;
                        }
                        
                        detailsHtml += `
                            <div class="col-md-6 mb-2">
                                <div class="detail-label">${formatFieldName(key)}</div>
                                <div class="detail-value">${value}</div>
                            </div>
                        `;
                    });
                    
                    detailsHtml += `</div></div>`;
                }
            });
        }
        
        modalBody.innerHTML = detailsHtml;
    }
    
    /**
     * Format database field names for display
     */
    function formatFieldName(fieldName) {
        // Special cases
        const specialFields = {
            'VPID': 'VMP ID',
            'VPPID': 'VMPP ID',
            'APID': 'AMP ID',
            'APPID': 'AMPP ID',
            'GTIN': 'GTIN Code',
            'AMP_ID': 'AMP ID'
        };
        
        if (specialFields[fieldName]) {
            return specialFields[fieldName];
        }
        
        // Convert from snake_case or UPPER_CASE to Title Case
        return fieldName
            .replace(/_/g, ' ')
            .split(' ')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
            .join(' ');
    }
    
    /**
     * Show statistics section
     */
    function showStatistics() {
        hideAllSections();
        statisticsSection.classList.remove('d-none');
        showLoading();
        
        fetch('/api/stats')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                hideLoading();
                
                if (data.success) {
                    displayStatistics(data.stats);
                } else {
                    statsContent.innerHTML = `<div class="alert alert-danger">${data.message}</div>`;
                }
            })
            .catch(error => {
                hideLoading();
                statsContent.innerHTML = `<div class="alert alert-danger">Error loading statistics: ${error.message}</div>`;
                console.error('Error fetching statistics:', error);
            });
    }
    
    /**
     * Display database statistics
     */
    function displayStatistics(stats) {
        let statsHtml = '';
        
        // Overview cards
        statsHtml += `<div class="row mb-4">`;
        
        // VMP card
        statsHtml += `
            <div class="col-md-3 col-sm-6">
                <div class="stat-card">
                    <div class="stat-number">${stats.vmp?.toLocaleString() || 0}</div>
                    <div class="stat-label">Virtual Medicinal Products</div>
                </div>
            </div>
        `;
        
        // VMPP card
        statsHtml += `
            <div class="col-md-3 col-sm-6">
                <div class="stat-card">
                    <div class="stat-number">${stats.vmpp?.toLocaleString() || 0}</div>
                    <div class="stat-label">Virtual Medicinal Product Packs</div>
                </div>
            </div>
        `;
        
        // AMP card
        statsHtml += `
            <div class="col-md-3 col-sm-6">
                <div class="stat-card">
                    <div class="stat-number">${stats.amp?.toLocaleString() || 0}</div>
                    <div class="stat-label">Actual Medicinal Products</div>
                </div>
            </div>
        `;
        
        // AMPP card
        statsHtml += `
            <div class="col-md-3 col-sm-6">
                <div class="stat-card">
                    <div class="stat-number">${stats.ampp?.toLocaleString() || 0}</div>
                    <div class="stat-label">Actual Medicinal Product Packs</div>
                </div>
            </div>
        `;
        
        statsHtml += `</div>`;
        
        // Additional stats
        statsHtml += `<div class="row">`;
        
        // GTIN card
        statsHtml += `
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body">
                        <h6 class="card-title">GTIN Information</h6>
                        <p class="mb-0">Total GTINs: <strong>${stats.gtin?.toLocaleString() || 0}</strong></p>
                    </div>
                </div>
            </div>
        `;
        
        // Pricing info card
        statsHtml += `
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body">
                        <h6 class="card-title">Pricing Information</h6>
                        <p class="mb-0">AMPPs with price: <strong>${stats.ampp_with_price?.toLocaleString() || 0}</strong></p>
                    </div>
                </div>
            </div>
        `;
        
        // Search data card
        statsHtml += `
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body">
                        <h6 class="card-title">Search Information</h6>
                        <p class="mb-0">Search index entries: <strong>${stats.search_data?.toLocaleString() || 0}</strong></p>
                    </div>
                </div>
            </div>
        `;
        
        statsHtml += `</div>`;
        
        // Price sources breakdown
        if (stats.ampp_price_sources && Object.keys(stats.ampp_price_sources).length > 0) {
            statsHtml += `
                <div class="row mt-4">
                    <div class="col-12">
                        <div class="card">
                            <div class="card-body">
                                <h6 class="card-title">Price Sources</h6>
                                <div class="table-responsive">
                                    <table class="table table-sm">
                                        <thead>
                                            <tr>
                                                <th>Source</th>
                                                <th>Count</th>
                                            </tr>
                                        </thead>
                                        <tbody>
            `;
            
            Object.keys(stats.ampp_price_sources).forEach(source => {
                statsHtml += `
                    <tr>
                        <td>${source || 'Unknown'}</td>
                        <td>${stats.ampp_price_sources[source].toLocaleString()}</td>
                    </tr>
                `;
            });
            
            statsHtml += `
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }
        
        statsContent.innerHTML = statsHtml;
    }
    
    /**
     * Export search results as CSV
     */
    function exportResultsAsCsv() {
        if (!searchResults || searchResults.length === 0) {
            alert('No results to export');
            return;
        }
        
        // Create CSV content
        const headers = ['ID', 'Type', 'Name', 'Supplier', 'Price'];
        
        let csvContent = headers.join(',') + '\n';
        
        searchResults.forEach(result => {
            // Format price as currency if available
            let priceDisplay = '';
            if (result.price) {
                // Price is stored in pence, convert to pounds
                priceDisplay = (result.price / 100).toFixed(2);
            }
            
            // Properly escape fields with commas
            const row = [
                result.id,
                result.type,
                `"${result.name.replace(/"/g, '""')}"`,  // Escape quotes
                `"${(result.supplier || '').replace(/"/g, '""')}"`,
                priceDisplay
            ];
            
            csvContent += row.join(',') + '\n';
        });
        
        // Create and download file
        const encodedUri = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csvContent);
        const link = document.createElement('a');
        link.setAttribute('href', encodedUri);
        link.setAttribute('download', `drug-tariff-search-${currentSearch}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
    
    /**
     * Print search results
     */
    function printResults() {
        if (!searchResults || searchResults.length === 0) {
            alert('No results to print');
            return;
        }
        
        // Create a printable version of the results
        const printWindow = window.open('', '_blank');
        
        printWindow.document.write(`
            <!DOCTYPE html>
            <html>
            <head>
                <title>Drug Tariff Search Results: ${currentSearch}</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    h1 { font-size: 18px; margin-bottom: 10px; }
                    .info { margin-bottom: 20px; }
                    table { border-collapse: collapse; width: 100%; }
                    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                    th { background-color: #f2f2f2; }
                    .no-print { display: none; }
                    @media print {
                        button { display: none; }
                        .header { margin-bottom: 20px; }
                    }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Drug Tariff Search Results</h1>
                    <div class="info">
                        <p>Search term: <strong>${currentSearch}</strong></p>
                        <p>Total results: <strong>${totalResults}</strong></p>
                        <p>Date: <strong>${new Date().toLocaleDateString()}</strong></p>
                    </div>
                    <button class="no-print" onclick="window.print()">Print</button>
                    <button class="no-print" onclick="window.close()">Close</button>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>Type</th>
                            <th>Name</th>
                            <th>Supplier</th>
                            <th>Price</th>
                        </tr>
                    </thead>
                    <tbody>
        `);
        
        searchResults.forEach(result => {
            // Format price as currency if available
            let priceDisplay = '';
            if (result.price) {
                // Price is stored in pence, convert to pounds
                const pounds = (result.price / 100).toFixed(2);
                priceDisplay = `£${pounds}`;
            } else {
                priceDisplay = '-';
            }
            
            printWindow.document.write(`
                <tr>
                    <td>${result.type}</td>
                    <td>${result.name}</td>
                    <td>${result.supplier || '-'}</td>
                    <td>${priceDisplay}</td>
                </tr>
            `);
        });
        
        printWindow.document.write(`
                    </tbody>
                </table>
            </body>
            </html>
        `);
        
        printWindow.document.close();
        
        // Trigger print after the content is loaded
        printWindow.addEventListener('load', function() {
            printWindow.focus();
            printWindow.print();
        });
    }
    
    /**
     * Highlight search term in a string
     */
    function highlightSearchTerm(text, searchTerm) {
        if (!text || !searchTerm) {
            return text;
        }
        
        // Escape special regex characters in the search term
        const escapeRegExp = (string) => {
            return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        };
        
        const searchWords = searchTerm.split(' ').map(word => escapeRegExp(word));
        let highlightedText = text;
        
        // Highlight each word from the search term
        searchWords.forEach(word => {
            if (word.length > 2) {  // Only highlight words with more than 2 characters
                const regex = new RegExp(word, 'gi');
                highlightedText = highlightedText.replace(regex, match => `<span class="highlight">${match}</span>`);
            }
        });
        
        return highlightedText;
    }
    
    /**
     * Show loading indicator
     */
    function showLoading() {
        loadingIndicator.classList.remove('d-none');
    }
    
    /**
     * Hide loading indicator
     */
    function hideLoading() {
        loadingIndicator.classList.add('d-none');
    }
    
    /**
     * Show no results section
     */
    function showNoResults() {
        noResultsSection.classList.remove('d-none');
        resultsSection.classList.add('d-none');
        statisticsSection.classList.add('d-none');
    }
    
    /**
     * Hide all sections
     */
    function hideAllSections() {
        resultsSection.classList.add('d-none');
        noResultsSection.classList.add('d-none');
        statisticsSection.classList.add('d-none');
    }
}); 