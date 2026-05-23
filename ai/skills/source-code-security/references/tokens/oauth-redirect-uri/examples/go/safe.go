package main

import "net/http"

var allowedRedirects = map[string]bool{
    "/dashboard": true,
    "/settings":  true,
    "/billing":   true,
}

func callbackHandler(w http.ResponseWriter, r *http.Request) {
    next := r.URL.Query().Get("next")
    if !allowedRedirects[next] {
        next = "/dashboard"
    }
    http.Redirect(w, r, next, http.StatusFound)
}
