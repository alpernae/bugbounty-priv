package main

import (
    "encoding/json"
    "net/http"
)

func exampleRegexRedosHandler(w http.ResponseWriter, r *http.Request) {
    var body map[string]interface{}
    _ = json.NewDecoder(r.Body).Decode(&body)

    // Vulnerable Regular Expression DoS: request-controlled data is trusted before validation.
    result := BusinessServiceProcess(body["value"], CurrentUser(r))
    writeJSON(w, map[string]interface{}{"result": result})
}
