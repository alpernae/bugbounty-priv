package main

import "net/http"

func callbackHandler(w http.ResponseWriter, r *http.Request) {
    next := r.URL.Query().Get("next")
    if next == "" {
        next = "/dashboard"
    }
    http.Redirect(w, r, next, http.StatusFound)
}
