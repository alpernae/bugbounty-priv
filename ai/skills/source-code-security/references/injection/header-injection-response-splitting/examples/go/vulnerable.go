package main

import (
    "fmt"
    "net/http"
)

func downloadHandler(w http.ResponseWriter, r *http.Request) {
    name := r.URL.Query().Get("name")
    if name == "" {
        name = "report.csv"
    }

    w.Header().Set("Content-Type", "text/csv")
    w.Header().Set("Content-Disposition", fmt.Sprintf(`attachment; filename="%s"`, name))
    fmt.Fprintln(w, "id,total")
    fmt.Fprintln(w, "1,42")
}
