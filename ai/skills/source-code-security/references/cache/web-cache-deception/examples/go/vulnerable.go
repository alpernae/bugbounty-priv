package main

import (
    "fmt"
    "net/http"
)

func profileHandler(w http.ResponseWriter, r *http.Request) {
    host := r.Header.Get("X-Forwarded-Host")
    w.Header().Set("Cache-Control", "public, max-age=600")
    fmt.Fprintf(w, "<link rel='canonical' href='https://%s/profile'>", host)
    fmt.Fprintf(w, "<h1>%s</h1>", CurrentUser(r).Email)
}
