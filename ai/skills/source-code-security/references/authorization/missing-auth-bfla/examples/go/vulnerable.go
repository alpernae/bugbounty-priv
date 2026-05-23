package main

import "net/http"

func invoiceHandler(w http.ResponseWriter, r *http.Request) {
    id := r.PathValue("id")
    invoice, err := invoices.FindByID(r.Context(), id)
    if err != nil {
        http.NotFound(w, r)
        return
    }

    writeJSON(w, invoice)
}
