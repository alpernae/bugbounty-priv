package main

import (
    "database/sql"
    "net/http"
)

var db *sql.DB

func invoicesHandler(w http.ResponseWriter, r *http.Request) {
    status := r.URL.Query().Get("status")
    if status == "" {
        status = "open"
    }

    rows, err := db.Query(
        "SELECT id,total,status FROM invoices WHERE status = ?",
        status,
    )
    if err != nil {
        http.Error(w, err.Error(), 500)
        return
    }
    writeRowsAsJSON(w, rows)
}
