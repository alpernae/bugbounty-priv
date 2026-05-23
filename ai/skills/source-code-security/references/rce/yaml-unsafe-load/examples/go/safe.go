package main

import (
    "encoding/base64"
    "encoding/json"
    "net/http"
)

type SessionState struct {
    UserID string `json:"userId"`
    Theme  string `json:"theme"`
}

func restoreSession(w http.ResponseWriter, r *http.Request) {
    raw, _ := base64.StdEncoding.DecodeString(r.URL.Query().Get("state"))

    var session SessionState
    if err := json.Unmarshal(raw, &session); err != nil || session.UserID == "" {
        http.Error(w, "invalid session", http.StatusBadRequest)
        return
    }

    writeJSON(w, session)
}
