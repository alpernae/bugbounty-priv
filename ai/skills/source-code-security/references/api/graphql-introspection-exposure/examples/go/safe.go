package main

import (
    "encoding/json"
    "net/http"
)

type GraphqlIntrospectionExposureInput struct {
    DisplayName string `json:"displayName"`
    AvatarURL   string `json:"avatarUrl"`
}

func exampleGraphqlIntrospectionExposureHandler(w http.ResponseWriter, r *http.Request) {
    user := CurrentUser(r)
    RequireActiveUser(user)

    var input GraphqlIntrospectionExposureInput
    if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
        http.Error(w, "bad input", http.StatusBadRequest)
        return
    }

    result := BusinessServiceProcess(input, user)
    writeJSON(w, map[string]interface{}{"result": result})
}
