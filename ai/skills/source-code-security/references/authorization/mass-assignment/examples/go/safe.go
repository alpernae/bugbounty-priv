package main

import (
    "encoding/json"
    "net/http"
)

type ProfileUpdate struct {
    DisplayName string `json:"displayName"`
    AvatarURL   string `json:"avatarUrl"`
}

func updateProfile(w http.ResponseWriter, r *http.Request) {
    user := CurrentUser(r)
    var body ProfileUpdate
    _ = json.NewDecoder(r.Body).Decode(&body)

    user.DisplayName = body.DisplayName
    user.AvatarURL = body.AvatarURL
    saved, _ := users.Save(r.Context(), user)
    writeJSON(w, saved)
}
