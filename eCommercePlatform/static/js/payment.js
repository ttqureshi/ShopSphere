let stripe;
let elements;
let cardElement;

function setupStripe() {
    stripe = Stripe('pk_test_51PpSeMRr8aD3gsItRb7cl2fri6Nvm7GkxtY7nbM8mqv4Ln6ES8DSwvc6sPE4z5kagvEyp8UDFao1yBiV8KN3HSfn00Zxevwk7p');
    elements = stripe.elements();
    cardElement = elements.create('card');
    cardElement.mount('#card-element');
}

function processPayment(clientSecret) {
    const result = stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: cardElement,
        },
    });

    if (result.error) {
        const errorElement = document.getElementById('card-errors');
        errorElement.textContent = result.error.message;
    } else {
        window.location.href = '/products/';
    }
}
