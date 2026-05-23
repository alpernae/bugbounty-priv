package main

import (
    "encoding/json"
    "log"
    "net/http"
)

func tokenHandler(w http.ResponseWriter, r *http.Request) {
    var body map[string]string
    _ = json.NewDecoder(r.Body).Decode(&body)

    log.Printf("token request body=%v headers=%v", body, r.Header)
    writeJSON(w, map[string]string{"access_token": IssueToken(body["code"])})
}
