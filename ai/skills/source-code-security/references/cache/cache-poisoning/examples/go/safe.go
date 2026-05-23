package main

import (
    "html/template"
    "net/http"
)

var profileTemplate = template.Must(template.New("profile").Parse(
    "<link rel='canonical' href='https://app.example.com/profile'><h1>{{ .Email }}</h1>",
))

func profileHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Cache-Control", "private, no-store")
    _ = profileTemplate.Execute(w, CurrentUser(r))
}
