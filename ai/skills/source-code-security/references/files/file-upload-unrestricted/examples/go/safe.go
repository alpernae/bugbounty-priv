package main

import (
    "crypto/rand"
    "encoding/hex"
    "io"
    "net/http"
    "os"
    "path/filepath"
)

func avatarHandler(w http.ResponseWriter, r *http.Request) {
    file, header, _ := r.FormFile("file")
    defer file.Close()

    if header.Header.Get("Content-Type") != "image/png" && header.Header.Get("Content-Type") != "image/jpeg" {
        http.Error(w, "bad file type", http.StatusBadRequest)
        return
    }

    buf := make([]byte, 16)
    rand.Read(buf)
    name := hex.EncodeToString(buf) + ".bin"
    out, _ := os.Create(filepath.Join("var", "uploads", name))
    defer out.Close()
    io.Copy(out, file)

    writeJSON(w, map[string]string{"fileId": name})
}
