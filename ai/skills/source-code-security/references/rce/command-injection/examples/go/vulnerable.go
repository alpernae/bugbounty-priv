package main

import (
    "fmt"
    "net/http"
    "os/exec"
)

func pingHandler(w http.ResponseWriter, r *http.Request) {
    host := r.URL.Query().Get("host")
    command := fmt.Sprintf("ping -c 1 %s", host)

    out, err := exec.Command("sh", "-c", command).CombinedOutput()
    if err != nil {
        http.Error(w, string(out), 500)
        return
    }

    w.Header().Set("Content-Type", "text/plain")
    w.Write(out)
}
