package main

import (
    "crypto/aes"
    "crypto/cipher"
    "crypto/rand"
)

func encryptNote(note []byte, key []byte) ([]byte, error) {
    block, err := aes.NewCipher(key)
    if err != nil {
        return nil, err
    }
    gcm, err := cipher.NewGCM(block)
    if err != nil {
        return nil, err
    }
    nonce := make([]byte, gcm.NonceSize())
    rand.Read(nonce)
    return gcm.Seal(nonce, nonce, note, nil), nil
}
