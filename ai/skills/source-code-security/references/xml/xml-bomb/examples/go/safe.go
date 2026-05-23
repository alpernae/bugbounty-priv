package main

import (
    "encoding/xml"
    "io"
    "net/http"
    "strings"
)

type SAMLResponse struct {
    NameID string `xml:"Assertion>NameID"`
}

func consumeSAML(w http.ResponseWriter, r *http.Request) {
    limited := http.MaxBytesReader(w, r.Body, 64*1024)
    body, _ := io.ReadAll(limited)
    if strings.Contains(strings.ToUpper(string(body)), "<!DOCTYPE") {
        http.Error(w, "doctype not allowed", http.StatusBadRequest)
        return
    }

    var response SAMLResponse
    _ = xml.Unmarshal(body, &response)
    writeJSON(w, map[string]string{"user": response.NameID})
}
