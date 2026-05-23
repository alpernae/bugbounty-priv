package main

import (
    "net/http"
    "path/filepath"
)

func downloadHandler(w http.ResponseWriter, r *http.Request) {
    name := r.URL.Query().Get("file")
    path := filepath.Join("uploads", name)
    http.ServeFile(w, r, path)
}
