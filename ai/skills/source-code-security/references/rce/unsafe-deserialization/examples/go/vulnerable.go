package main

import (
    "encoding/base64"
    "encoding/gob"
    "net/http"
    "bytes"
)

func restoreSession(w http.ResponseWriter, r *http.Request) {
    raw, _ := base64.StdEncoding.DecodeString(r.URL.Query().Get("state"))

    var session map[string]interface{}
    decoder := gob.NewDecoder(bytes.NewReader(raw))
    _ = decoder.Decode(&session)

    writeJSON(w, session)
}
