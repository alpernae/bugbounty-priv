package main

import (
    "crypto/des"
    "crypto/md5"
)

func encryptNote(note []byte, password string) ([]byte, error) {
    key := md5.Sum([]byte(password))
    block, err := des.NewCipher(key[:8])
    if err != nil {
        return nil, err
    }
    out := make([]byte, len(note))
    block.Encrypt(out, note[:8])
    return out, nil
}
