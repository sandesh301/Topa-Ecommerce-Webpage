document.addEventListener('DOMContentLoaded', function () {
    const step1 = document.getElementById('step1');
    const step2 = document.getElementById('step2');
    const step3 = document.getElementById('step3');

    const btnNextDelivery = document.getElementById('btn-next-delivery');
    const btnNextPayment = document.getElementById('btn-next-payment');
    const stripePaymentForm = document.getElementById('stripe-payment-form');

    // Fetch and populate countries in the country select dropdown
    const countrySelect = document.querySelector('#country');
    fetchCountries();

    async function fetchCountries() {
        try {
            const response = await fetch('https://restcountries.com/v2/all');
            if (response.ok) {
                const countries = await response.json();
                populateCountryDropdown(countries);
            } else {
                console.error('Error fetching countries:', response.statusText);
            }
        } catch (error) {
            console.error('Error fetching countries:', error);
        }
    }

    function populateCountryDropdown(countries) {
        countries.forEach(country => {
            const option = document.createElement('option');
            option.value = country.name;
            option.textContent = country.name;
            countrySelect.appendChild(option);
        });
    }

    // Display Step 2 after successful delivery form submission
    btnNextDelivery.addEventListener('click', function () {
        step1.style.display = 'none';
        step2.style.display = 'block';
    });

    // Display Step 3 (Stripe Payment) after payment option selection
    btnNextPayment.addEventListener('click', function () {
        step2.style.display = 'none';
        step3.style.display = 'block';
        initializeStripe();
    });

    // Helper function to get CSRF token
    function getCSRFToken() {
        const csrfTokenInput = document.querySelector('input[name=csrfmiddlewaretoken]');
        if (csrfTokenInput) {
            return csrfTokenInput.value;
        }
        return '';
    }

    // Handle delivery form submission
    const deliveryFormElement = document.querySelector('#delivery-form');
    deliveryFormElement.addEventListener('submit', async function (event) {
        event.preventDefault();

        // Collect form data
        const formData = new FormData(deliveryFormElement);

        // Send AJAX request to save data
        try {
            const response = await fetch('http://127.0.0.1:8000/Delivery_Address/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCSRFToken() // Get CSRF token if needed
                }
            });

            if (response.ok) {
                // Proceed to the next step
                step1.style.display = 'none';
                step2.style.display = 'block';
            } else {
                // Handle form submission error
                console.error('Error submitting delivery form');
            }
        } catch (error) {
            // Handle fetch error
            console.error('Error fetching data:', error);
        }
    });

    // Initialize Stripe
    function initializeStripe() {
        const stripe = Stripe('pk_test_51MxAqkGsYPii3aLi4ndRSW0MfmZehh8sQMbmDOVz79AxVzZobE578EzsFIqlYNLTusBO6mMVqzSowA9dSGGuccl800VipTuU04'); // Replace with your Stripe publishable key
        const elements = stripe.elements();
        const card = elements.create('card');

        // Mount the Stripe card element
        card.mount('#card-element');

        const cardErrors = document.getElementById('card-errors');

        stripePaymentForm.addEventListener('submit', async function (event) {
            event.preventDefault();


            const { token, error } = await stripe.createToken(card);

            if (error) {
                cardErrors.textContent = error.message;
            } else {
                // Send the token to your server
                sendTokenToServer(token);

            }
        });

    }

    // Send the token to your server
    function sendTokenToServer(token) {
        fetch('/process_payment/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCSRFToken() // Get CSRF token if needed
            },
            body: `token=${token.id}`
        })
            .then(response => response.text()) // Parse response as text
            .then(responseText => {
                console.log(responseText);
                try {
                    const data = JSON.parse(responseText); // Try to parse as JSON
                    if (data.status === 'success') {
                        // Payment successful
                        console.log('Payment successful');
                        // You can redirect the user to a success page or display a success message
                    } else if (data.status === 'failure') {
                        // Payment failed
                        console.log('Payment failed');
                        // You can redirect the user to a failure page or display a failure message
                    } else {
                        // Other error, handle accordingly
                        console.log('Other error:', data.message);
                        // You can display an error message to the user
                    }
                } catch (jsonError) {
                    console.error('Error parsing JSON:', jsonError);
                }
            })
            .catch(error => {
                console.error('Error sending token:', error);
            });
    }
});
