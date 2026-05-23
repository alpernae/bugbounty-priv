package examples;

public class ClientSideSecretsExample {
    private static final String STRIPE_KEY = "sk_live_REDACTED_BUT_REAL_LOOKING_SECRET";

    public CheckoutSession createCheckout(String priceId) {
        StripeClient stripe = new StripeClient(STRIPE_KEY);
        return stripe.checkout(priceId, "https://app.example.com/success");
    }
}
