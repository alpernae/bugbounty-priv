package main

import "net/http"

var allowedOrigins = map[string]bool{
    "https://app.example.com":   true,
    "https://admin.example.com": true,
}

func cors(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        origin := r.Header.Get("Origin")
        if allowedOrigins[origin] {
            w.Header().Set("Access-Control-Allow-Origin", origin)
            w.Header().Set("Access-Control-Allow-Credentials", "true")
            w.Header().Set("Vary", "Origin")
        }
        next.ServeHTTP(w, r)
    })
}
