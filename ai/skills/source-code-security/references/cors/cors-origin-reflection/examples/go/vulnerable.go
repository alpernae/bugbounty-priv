package main

import "net/http"

func cors(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Access-Control-Allow-Origin", r.Header.Get("Origin"))
        w.Header().Set("Access-Control-Allow-Credentials", "true")
        next.ServeHTTP(w, r)
    })
}
