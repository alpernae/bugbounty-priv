package main

import (
    "database/sql"
    "fmt"
    "net/http"
)

var db *sql.DB

func invoicesHandler(w http.ResponseWriter, r *http.Request) {
    status := r.URL.Query().Get("status")
    if status == "" {
        status = "open"
    }

    query := fmt.Sprintf("SELECT id,total,status FROM invoices WHERE status = '%s'", status)
    rows, err := db.Query(query)
    if err != nil {
        http.Error(w, err.Error(), 500)
        return
    }
    writeRowsAsJSON(w, rows)
}
