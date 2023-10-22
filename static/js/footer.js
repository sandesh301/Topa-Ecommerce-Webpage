const createFooter = () => {
    let footer = document.querySelector('footer');

    footer.innerHTML = `
    <div class="footer-content">
        <img src="img/Topa 1.png" class="logo" alt="">
        <div class="footer-ul-container">
            <ul class="category">
                <li class="category-title"> Women </li>
                <li><a href="#" class="footer-link">T-shirts</a></li>
                <li><a href="#" class="footer-link">Tops</a></li>
                <li><a href="#" class="footer-link">Shirts</a></li>
                <li><a href="#" class="footer-link">Jeans</a></li>
                <li><a href="#" class="footer-link">Bottoms</a></li>
                <li><a href="#" class="footer-link">Casuals</a></li>
                <li><a href="#" class="footer-link">One-Piece</a></li>

            </ul>
        </div>
    </div>
    <p class="footer-title"> About TOPA </p>
    <p class="info" style="font-size:15px"><b>TOPA is a vertically integrated company, having its own sourcing, production, marketing, and sales unit, which allows us to take sustainable choices and ethical stands at every step of the supply chain. The exploitative problems of the industry can only be confronted when we are in complete control of our actions.</b></p>
    <p class="footer-title">Support Email:</pre>
    <p class="info"><b>topanewyork.com</b></p>
    <pre class="footer-title">Telephone:</pre>
     <p class="info"><b>+977 9860557647,
      180 00 00 002</b></p>
    <div class="footer-social-container">
        
            <a href="terms.html" class="social-link">Terms & Services</a>
            <a href="privacy.html" class="social-link">Privacy Page</a>
        
            <a href="#" class="social-link">Instagram</a>
            <a href="#" class="social-link">Facebook</a>
    
    </div>
                @ TOPA 2023 | designed and developed by Golden Duck Enterprises
              <p class="footer-credit"><b><i> @ TOPA 2023 | designed and developed by Golden Duck Enterprises</i></b></p>
    `;
}

createFooter();