package main

import (
    "fmt"
    "net/http"
    "regexp"
)

var safeFileName = regexp.MustCompile(`[^a-zA-Z0-9._-]`)

func downloadHandler(w http.ResponseWriter, r *http.Request) {
    name := safeFileName.ReplaceAllString(r.URL.Query().Get("name"), "_")
    if name == "" {
        name = "report.csv"
    }

    w.Header().Set("Content-Type", "text/csv")
    w.Header().Set("Content-Disposition", fmt.Sprintf(`attachment; filename="%s"`, name))
    fmt.Fprintln(w, "id,total")
    fmt.Fprintln(w, "1,42")
}
