package main

import (
    "io"
    "net/http"
    "os"
    "path/filepath"
)

func avatarHandler(w http.ResponseWriter, r *http.Request) {
    file, header, _ := r.FormFile("file")
    defer file.Close()

    destination := filepath.Join("public", "uploads", header.Filename)
    out, _ := os.Create(destination)
    defer out.Close()
    io.Copy(out, file)

    writeJSON(w, map[string]string{"publicUrl": "/uploads/" + header.Filename})
}
