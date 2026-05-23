package main

import (
    "archive/zip"
    "io"
    "os"
    "path/filepath"
    "strings"
)

func importZip(archive string) error {
    dest, _ := filepath.Abs("var/imports")
    reader, err := zip.OpenReader(archive)
    if err != nil { return err }
    defer reader.Close()

    for _, file := range reader.File {
        target, _ := filepath.Abs(filepath.Join(dest, file.Name))
        if target == dest || !strings.HasPrefix(target, dest + string(filepath.Separator)) { continue }
        rc, _ := file.Open()
        os.MkdirAll(filepath.Dir(target), 0750)
        out, _ := os.OpenFile(target, os.O_WRONLY|os.O_CREATE|os.O_EXCL, 0600)
        io.Copy(out, rc)
        out.Close()
        rc.Close()
    }
    return nil
}
