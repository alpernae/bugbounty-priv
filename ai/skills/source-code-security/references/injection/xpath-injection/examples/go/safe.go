package main

import (
    "encoding/json"
    "net/http"

    "go.mongodb.org/mongo-driver/bson"
)

func loginHandler(w http.ResponseWriter, r *http.Request) {
    var body struct {
        Email    string `json:"email"`
        Password string `json:"password"`
    }
    _ = json.NewDecoder(r.Body).Decode(&body)

    var user User
    err := users.FindOne(r.Context(), bson.M{"email": body.Email}).Decode(&user)
    if err != nil || !CheckPasswordHash(body.Password, user.PasswordHash) {
        http.Error(w, "invalid login", http.StatusUnauthorized)
        return
    }

    writeJSON(w, PublicUser{ID: user.ID, Email: user.Email})
}
