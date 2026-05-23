package main

import (
    "archive/zip"
    "io"
    "os"
    "path/filepath"
)

func importZip(archive string) error {
    reader, err := zip.OpenReader(archive)
    if err != nil { return err }
    defer reader.Close()

    for _, file := range reader.File {
        target := filepath.Join("var/imports", file.Name)
        rc, _ := file.Open()
        out, _ := os.Create(target)
        io.Copy(out, rc)
        out.Close()
        rc.Close()
    }
    return nil
}
