document.addEventListener('DOMContentLoaded', function() {
    const stripe = Stripe('{{ stripe_public_key }}'); // Use the public key from your Django context
    const cardButton = document.getElementById('card-button');

    cardButton.addEventListener('click', function() {
        const checkoutSessionId = '{{ checkout_session_id }}'; // Use the session ID from your Django context
        stripe.redirectToCheckout({ sessionId: checkoutSessionId })
            .then(function(result) {
                if (result.error) {
                    alert(result.error.message);
                }
            });
    });
}); 