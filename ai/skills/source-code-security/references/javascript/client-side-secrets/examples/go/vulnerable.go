package main

type CheckoutService struct {
    stripe *StripeClient
}

func NewCheckoutService() *CheckoutService {
    return &CheckoutService{
        stripe: NewStripeClient("sk_live_REDACTED_BUT_REAL_LOOKING_SECRET"),
    }
}

func (s *CheckoutService) CreateCheckout(priceID string) (*CheckoutSession, error) {
    return s.stripe.Checkout(priceID, "https://app.example.com/success")
}
