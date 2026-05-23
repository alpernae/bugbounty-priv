package main

import (
    "net/http"

    "github.com/golang-jwt/jwt/v5"
)

func adminHandler(w http.ResponseWriter, r *http.Request) {
    raw := bearerToken(r)
    token, _, _ := jwt.NewParser().ParseUnverified(raw, jwt.MapClaims{})
    claims := token.Claims.(jwt.MapClaims)

    if claims["role"] != "admin" {
        http.Error(w, "forbidden", http.StatusForbidden)
        return
    }

    writeJSON(w, map[string]bool{"admin": true})
}
