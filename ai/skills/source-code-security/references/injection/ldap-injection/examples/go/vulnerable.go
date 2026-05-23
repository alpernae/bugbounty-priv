package main

import (
    "encoding/json"
    "net/http"

    "go.mongodb.org/mongo-driver/bson"
)

func loginHandler(w http.ResponseWriter, r *http.Request) {
    var body map[string]interface{}
    _ = json.NewDecoder(r.Body).Decode(&body)

    filter := bson.M{
        "email":    body["email"],
        "password": body["password"],
    }

    user := users.FindOne(r.Context(), filter)
    writeJSON(w, user)
}
