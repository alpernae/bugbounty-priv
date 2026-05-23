package main

import (
    "html/template"
    "net/http"
)

var searchTemplate = template.Must(template.New("search").Parse(`
<html><body>
  <h1>Search</h1>
  <p>Results for: {{ .Query }}</p>
</body></html>`))

func searchHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "text/html; charset=utf-8")
    _ = searchTemplate.Execute(w, struct{ Query string }{
        Query: r.URL.Query().Get("q"),
    })
}

func main() {
    http.HandleFunc("/search", searchHandler)
    http.ListenAndServe(":8080", nil)
}
