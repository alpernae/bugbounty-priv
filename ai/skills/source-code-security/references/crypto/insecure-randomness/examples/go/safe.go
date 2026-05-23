package main

import (
    "crypto/rand"
    "encoding/base64"
    "fmt"
    "time"
)

func CreatePasswordResetToken(userID string) string {
    b := make([]byte, 32)
    rand.Read(b)
    return fmt.Sprintf("%s.%d.%s", userID, time.Now().Unix(), base64.RawURLEncoding.EncodeToString(b))
}
