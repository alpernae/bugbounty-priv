package main

import (
    "io"
    "net/http"
)

func fetchPreview(w http.ResponseWriter, r *http.Request) {
    url := r.URL.Query().Get("url")
    resp, err := http.Get(url)
    if err != nil {
        http.Error(w, err.Error(), 500)
        return
    }
    defer resp.Body.Close()

    sample, _ := io.ReadAll(io.LimitReader(resp.Body, 200))
    writeJSON(w, map[string]interface{}{"status": resp.StatusCode, "sample": string(sample)})
}
