package main

import (
    "encoding/json"
    "html/template"
    "net/http"
)

func previewEmail(w http.ResponseWriter, r *http.Request) {
    var body map[string]string
    _ = json.NewDecoder(r.Body).Decode(&body)

    tmpl := template.Must(template.New("email").Parse(body["template"]))
    _ = tmpl.Execute(w, map[string]string{
        "Name": body["name"],
    })
}
