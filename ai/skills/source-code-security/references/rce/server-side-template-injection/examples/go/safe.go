package main

import (
    "encoding/json"
    "html/template"
    "net/http"
)

var templates = map[string]*template.Template{
    "welcome":  template.Must(template.New("welcome").Parse("Hello {{ .Name }}")),
    "reminder": template.Must(template.New("reminder").Parse("Reminder for {{ .Name }}")),
}

func previewEmail(w http.ResponseWriter, r *http.Request) {
    var body map[string]string
    _ = json.NewDecoder(r.Body).Decode(&body)

    tmpl := templates[body["templateKey"]]
    if tmpl == nil {
        tmpl = templates["welcome"]
    }
    _ = tmpl.Execute(w, map[string]string{"Name": body["name"]})
}
