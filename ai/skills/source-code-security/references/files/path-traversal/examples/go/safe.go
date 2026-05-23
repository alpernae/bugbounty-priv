package main

import (
    "net/http"
    "path/filepath"
    "strings"
)

var uploadRoot, _ = filepath.Abs("uploads")

func downloadHandler(w http.ResponseWriter, r *http.Request) {
    name := filepath.Base(r.URL.Query().Get("file"))
    path, _ := filepath.Abs(filepath.Join(uploadRoot, name))
    if !strings.HasPrefix(path, uploadRoot + string(filepath.Separator)) {
        http.Error(w, "invalid file", http.StatusBadRequest)
        return
    }
    http.ServeFile(w, r, path)
}
