<?php
// services/Checkout.php
$secret = getenv('STRIPE_SECRET_KEY');
if (!$secret) {
    throw new RuntimeException('STRIPE_SECRET_KEY is required');
}
$stripe = new StripeClient($secret);

function create_checkout($priceId) {
    global $stripe;
    return $stripe->checkout([
        'price' => $priceId,
        'success_url' => 'https://app.example.com/success'
    ]);
}
?>
