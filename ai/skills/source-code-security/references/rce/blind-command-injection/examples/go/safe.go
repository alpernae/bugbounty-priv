package main

import (
    "net"
    "net/http"
    "os/exec"
)

func pingHandler(w http.ResponseWriter, r *http.Request) {
    host := r.URL.Query().Get("host")
    if net.ParseIP(host) == nil {
        http.Error(w, "invalid host", http.StatusBadRequest)
        return
    }

    out, err := exec.Command("ping", "-c", "1", host).CombinedOutput()
    if err != nil {
        http.Error(w, string(out), 500)
        return
    }

    w.Header().Set("Content-Type", "text/plain")
    w.Write(out)
}
