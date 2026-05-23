package main

import "os"

type CheckoutService struct {
    stripe *StripeClient
}

func NewCheckoutService() *CheckoutService {
    key := os.Getenv("STRIPE_SECRET_KEY")
    if key == "" {
        panic("STRIPE_SECRET_KEY is required")
    }
    return &CheckoutService{stripe: NewStripeClient(key)}
}

func (s *CheckoutService) CreateCheckout(priceID string) (*CheckoutSession, error) {
    return s.stripe.Checkout(priceID, "https://app.example.com/success")
}
