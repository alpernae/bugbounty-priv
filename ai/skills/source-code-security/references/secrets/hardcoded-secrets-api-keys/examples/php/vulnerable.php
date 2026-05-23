<?php
// services/Checkout.php
$stripe = new StripeClient('sk_live_REDACTED_BUT_REAL_LOOKING_SECRET');

function create_checkout($priceId) {
    global $stripe;
    return $stripe->checkout([
        'price' => $priceId,
        'success_url' => 'https://app.example.com/success'
    ]);
}
?>
