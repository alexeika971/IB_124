from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def encrypt_ecb(data: bytes, key: bytes) -> bytes:
    """
    Encrypt data using AES-128 in ECB mode with PKCS#7 padding.
    
    Args:
        data: The plaintext data to encrypt.
        key: The 16-byte AES key.
    
    Returns:
        The encrypted ciphertext.
    
    Raises:
        ValueError: If the key is not 16 bytes.
    """
    if len(key) != 16:
        raise ValueError("Key must be 16 bytes for AES-128.")
    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = pad(data, AES.block_size)
    return cipher.encrypt(padded_data)

def decrypt_ecb(data: bytes, key: bytes) -> bytes:
    """
    Decrypt data using AES-128 in ECB mode and remove PKCS#7 padding.
    
    Args:
        data: The ciphertext data to decrypt.
        key: The 16-byte AES key.
    
    Returns:
        The decrypted plaintext.
    
    Raises:
        ValueError: If the key is not 16 bytes, or if decryption or padding removal fails.
    """
    if len(key) != 16:
        raise ValueError("Key must be 16 bytes for AES-128.")
    cipher = AES.new(key, AES.MODE_ECB)
    try:
        decrypted_data = cipher.decrypt(data)
    except Exception as e:
        raise ValueError(f"Decryption failed: {e}")
    
    try:
        plaintext = unpad(decrypted_data, AES.block_size)
    except ValueError as e:
        raise ValueError(f"PKCS#7 padding validation failed: {e}")
    return plaintext