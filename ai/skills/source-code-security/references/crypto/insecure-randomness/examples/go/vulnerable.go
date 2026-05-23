package main

import (
    "fmt"
    "math/rand"
    "time"
)

func CreatePasswordResetToken(userID string) string {
    suffix := rand.Intn(1_000_000)
    return fmt.Sprintf("%s.%d.%06d", userID, time.Now().Unix(), suffix)
}
