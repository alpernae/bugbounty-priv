package main

import (
    "net"
    "net/http"
    "net/url"
)

var allowedHosts = map[string]bool{
    "api.partner.example":      true,
    "images.example-cdn.com":   true,
}

func fetchPreview(w http.ResponseWriter, r *http.Request) {
    raw := r.URL.Query().Get("url")
    parsed, err := url.Parse(raw)
    if err != nil || parsed.Scheme != "https" || !allowedHosts[parsed.Hostname()] {
        http.Error(w, "blocked upstream", http.StatusBadRequest)
        return
    }

    addrs, _ := net.LookupIP(parsed.Hostname())
    for _, ip := range addrs {
        if ip.IsPrivate() || ip.IsLoopback() || ip.IsLinkLocalUnicast() {
            http.Error(w, "blocked upstream", http.StatusBadRequest)
            return
        }
    }

    resp, _ := (&http.Client{CheckRedirect: func(*http.Request, []*http.Request) error {
        return http.ErrUseLastResponse
    }}).Get(raw)
    writeJSON(w, map[string]int{"status": resp.StatusCode})
}
