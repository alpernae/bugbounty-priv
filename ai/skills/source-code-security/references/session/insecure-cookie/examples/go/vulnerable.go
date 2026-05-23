package main

import "net/http"

func loginHandler(w http.ResponseWriter, r *http.Request) {
    user := Authenticate(r.FormValue("email"), r.FormValue("password"))
    sessionID := CreateSession(user.ID)

    http.SetCookie(w, &http.Cookie{
        Name:  "sid",
        Value: sessionID,
    })
    http.Redirect(w, r, "/dashboard", http.StatusFound)
}
