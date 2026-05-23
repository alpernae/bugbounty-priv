package main

import (
    "fmt"
    "net/http"
)

func searchHandler(w http.ResponseWriter, r *http.Request) {
    query := r.URL.Query().Get("q")
    w.Header().Set("Content-Type", "text/html; charset=utf-8")
    fmt.Fprintf(w, "<html><body>")
    fmt.Fprintf(w, "<h1>Search</h1>")
    fmt.Fprintf(w, "<p>Results for: %s</p>", query)
    fmt.Fprintf(w, "</body></html>")
}

func main() {
    http.HandleFunc("/search", searchHandler)
    http.ListenAndServe(":8080", nil)
}
