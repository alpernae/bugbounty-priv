package examples;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.security.MessageDigest;

public class WeakCryptoExample {
    public byte[] encrypt(byte[] note, String password) throws Exception {
        byte[] key = MessageDigest.getInstance("MD5").digest(password.getBytes());
        Cipher cipher = Cipher.getInstance("DES/ECB/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, new SecretKeySpec(key, "DES"));
        return cipher.doFinal(note);
    }
}
