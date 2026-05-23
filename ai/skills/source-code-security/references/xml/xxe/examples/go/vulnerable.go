package main

import (
    "encoding/xml"
    "net/http"
)

type SAMLResponse struct {
    NameID string `xml:"Assertion>NameID"`
}

func consumeSAML(w http.ResponseWriter, r *http.Request) {
    var response SAMLResponse
    decoder := xml.NewDecoder(r.Body)
    _ = decoder.Decode(&response)
    writeJSON(w, map[string]string{"user": response.NameID})
}
