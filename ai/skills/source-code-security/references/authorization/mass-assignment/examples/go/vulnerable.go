package main

import (
    "encoding/json"
    "net/http"
)

func updateProfile(w http.ResponseWriter, r *http.Request) {
    user := CurrentUser(r)
    _ = json.NewDecoder(r.Body).Decode(&user)

    saved, _ := users.Save(r.Context(), user)
    writeJSON(w, saved)
}
