package examples;

public class ClientSideSecretsExample {
    private final StripeClient stripe;

    public ClientSideSecretsExample() {
        String key = System.getenv("STRIPE_SECRET_KEY");
        if (key == null || key.isBlank()) throw new IllegalStateException("missing key");
        this.stripe = new StripeClient(key);
    }

    public CheckoutSession createCheckout(String priceId) {
        return stripe.checkout(priceId, "https://app.example.com/success");
    }
}
