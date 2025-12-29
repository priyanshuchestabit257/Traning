const productGrid = document.getElementById('product-grid');
const searchInput = document.getElementById('search-input');
const sortSelect = document.getElementById('sort-select');

let allProducts = []; // To store fetched data locally

// 1. Fetch Products from API
async function fetchProducts() {
    try {
        const response = await fetch('https://dummyjson.com/products');
        const data = await response.json();
        allProducts = data.products; // Save to global variable
        renderProducts(allProducts); // Initial render
    } catch (error) {
        console.error("Error fetching products:", error);
        productGrid.innerHTML = "<p>Failed to load products. Please try again.</p>";
    }
}

// 2. Render Products to HTML
function renderProducts(products) {
    productGrid.innerHTML = ""; // Clear existing content

    if (products.length === 0) {
        productGrid.innerHTML = "<p>No products found.</p>";
        return;
    }

    products.forEach(product => {
        // Create Card HTML
        const card = document.createElement('div');
        card.classList.add('card');
        
        card.innerHTML = `
            <img src="${product.thumbnail}" alt="${product.title}">
            <h3>${product.title}</h3>
            <p>Category: ${product.category}</p>
            <p class="price">$${product.price}</p>
        `;
        
        productGrid.appendChild(card);
    });
}

// 3. Search Functionality
searchInput.addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    
    const filteredProducts = allProducts.filter(product => 
        product.title.toLowerCase().includes(searchTerm)
    );
    
    renderProducts(filteredProducts);
});

// 4. Sort Functionality
sortSelect.addEventListener('change', (e) => {
    const sortValue = e.target.value;
    let sortedProducts = [...allProducts]; // Copy array to avoid mutating original

    if (sortValue === 'low-high') {
        sortedProducts.sort((a, b) => a.price - b.price);
    } else if (sortValue === 'high-low') {
        sortedProducts.sort((a, b) => b.price - a.price);
    }
    
    // If search is also active, we should strictly sort the currently visible items,
    // but for this simple version, sorting the 'allProducts' copy is acceptable 
    // or re-applying search filter. 
    // Ideally: Filter first, then Sort.
    
    // Quick Fix: Re-run search logic on sorted list
    const searchTerm = searchInput.value.toLowerCase();
    const finalProducts = sortedProducts.filter(product => 
        product.title.toLowerCase().includes(searchTerm)
    );

    renderProducts(finalProducts);
});

// Initialize
fetchProducts();