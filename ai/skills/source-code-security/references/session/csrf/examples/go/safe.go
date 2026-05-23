package main

import "net/http"

func loginHandler(w http.ResponseWriter, r *http.Request) {
    user := Authenticate(r.FormValue("email"), r.FormValue("password"))
    sessionID := RotateSession(user.ID)

    http.SetCookie(w, &http.Cookie{
        Name:     "sid",
        Value:    sessionID,
        HttpOnly: true,
        Secure:   true,
        SameSite: http.SameSiteLaxMode,
        Path:     "/",
    })
    http.Redirect(w, r, "/dashboard", http.StatusFound)
}
