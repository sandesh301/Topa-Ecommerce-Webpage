document.addEventListener("DOMContentLoaded", function () {

  // Fetch sizes from the backend
  const fetchSizes = () => {
    return fetch('http://127.0.0.1:8000/get_sizes/')
      .then(response => response.json())
      .then(data => data.sizes)
      .catch(error => {
        console.error('Error fetching sizes:', error);
        return [];
      });
  };

  // Populate size dropdown
  const sizeDropdown = document.getElementById('size');
  fetchSizes().then(sizes => {
    sizeDropdown.innerHTML = sizes.map(size => `<option value="${size.id}">${size.name}</option>`).join('');
  });

  // Add event listener to size dropdown
  sizeDropdown.addEventListener('change', () => {
    const selectedSizeId = sizeDropdown.value;
    if (selectedSizeId) {
      // Fetch and display products based on the selected size
      fetch(`http://127.0.0.1:8000/get_products_by_size/${selectedSizeId}/`)
        .then(response => response.json())
        .then(data => {
          // Clear the existing content in the product container
          const productContainer = document.querySelector('.container');
          productContainer.innerHTML = '';

          // Loop through the fetched products and create HTML elements for each product
          data.products.forEach(product => {
            const productElement = document.createElement('div');
            productElement.classList.add('items'); // Add appropriate class

            productElement.innerHTML = `
            <div class="img"><img src="${product.Product_image.url}" alt="${product.Product_name}"></div>
            <div class="name">${product.Product_name}</div>
            <div class="price">$${product.original_price}</div>
            <div class="info">${product.Product_desc}</div>
            <button class="button">
              <span>Add to cart</span>
            </button>
            <button class="button">
              <span>Add to wishlist</span>
            </button>
          `;
            productContainer.appendChild(productElement);
          });
        })
        .catch(error => {
          console.error('Error fetching products by size:', error);
        });
    } else {
      // Reset the product display to show all products
      // Example: Remove or update the existing product display as needed
    }
  });
});
