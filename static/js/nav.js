const fetchCollections = () => {
    return fetch('http://127.0.0.1:8000/Collection/')
        .then(response => {
            console.log('Response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('Fetched data:', data);
            const collections = data; // Access the entire array as collections
            console.log('Fetched collections:', collections);
            return collections;
        })
        .catch(error => {
            console.error('Error fetching collections:', error);
            return [];
        });
};

const createNav = () => {
    let nav = document.querySelector('.navbar');
    fetch('/check_authentication/')
        .then(response => response.json())
        .then(async data => {
            const isAuthenticated = data && data.is_authenticated; // Check if data is defined

            let logoutButton = '';
            if (isAuthenticated) {
                logoutButton = '<a href="/logout"><img src="static/img/logout.png" alt="Logout"></a>';
            } else {
                logoutButton = '<a href="/login"><img src="static/img/login.png" alt="Login"></a>';
            }

            nav.innerHTML = `
      
          <div class="nav">
          <div class="nav-items">
          <a href=""><i style='font-size:24px'; class='fas'>&#xf002;</i></a>&nbsp;
          <a href="/register"><i style='font-size:24px' class='fas'>&#xf406;</i></a>
          </div>
          <a href="home"><img src="static/gif/Topa.gif" class="brand-logo" alt=""></a>
              <div class="nav-items a">
                  <a href="/wishlist_view"><i style='font-size:24px' class='fas'>&#xf290;</i></a>&nbsp;
                  
                  <a href="/cart_View"><i style='font-size:24px' class='fas'>	&#xf291;</i></a>
  
                  ${logoutButton}
              </div>
          </div>
          <ul class="links-container" style="margin-top:15px">
  
              <li class="link-item ">
              <a href="/shop" class="link" style="font-size:30px;"> Shop</a>
              <div class="dropdown-content space-x-24">
              <div class="row1 flex flex-col  w-1/3 space-y-3">
              <a href="#" class="dropdown-item">Shop All</a>
              <a href="#" class="dropdown-item">New Arrival</a>
              <a href="#" class="dropdown-item">Tops</a>
              <a href="#" class="dropdown-item">Bottoms</a>
              <a href="#" class="dropdown-item">One Piece</a>
              </div>
            </li>
            <li class="link-item ">
            <a href="/collection" class="link" style="font-size:30px;"> Collections </a>
            <div class="dropdown-content space-x-24 collections-dropdown">
                <!-- Collections will be dynamically populated here -->
            </div>
        </li>
          <li class="link-item ">
              <a class="link" style="font-size:30px;"> About </a>
              <div class="dropdown-content space-x-24">
              <div class="row1 flex flex-col  w-1/3 space-y-3">
              <a href="/about_us" class="dropdown-item">About Topa</a>
              <a href="/sustainability" class="dropdown-item">Sustainability & Ethical Values</a>
              </div>
            </li>
  
      </ul>
      `;

            const collections = await fetchCollections();
            const collectionsDropdown = document.querySelector('.collections-dropdown');
            if (collections && collectionsDropdown) {
                console.log('Collections data:', collections);
                collectionsDropdown.innerHTML = collections.map(collection => {
                    return `
                        <div class="row1 flex flex-col  w-1/2 space-y-3">
                            <a href="/collection/${collection.id}/" class="dropdown-item">${collection.name}</a>
                        </div>
                    `;
                }).join('');
            }
        })
        .catch(error => {
            console.error('Error fetching authentication status:', error);
            // Handle error gracefully
        });
}

createNav();

