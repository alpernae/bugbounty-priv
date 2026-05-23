package main

import (
    "net/http"

    "github.com/golang-jwt/jwt/v5"
)

func adminHandler(w http.ResponseWriter, r *http.Request) {
    raw := bearerToken(r)
    claims := jwt.MapClaims{}
    token, err := jwt.ParseWithClaims(raw, claims, func(token *jwt.Token) (interface{}, error) {
        if token.Method.Alg() != jwt.SigningMethodRS256.Alg() {
            return nil, ErrBadAlgorithm
        }
        return jwtPublicKey, nil
    }, jwt.WithIssuer("https://auth.example.com"), jwt.WithAudience("example-api"))

    if err != nil || !token.Valid || claims["role"] != "admin" {
        http.Error(w, "forbidden", http.StatusForbidden)
        return
    }

    writeJSON(w, map[string]bool{"admin": true})
}
