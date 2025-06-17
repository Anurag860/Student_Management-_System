import hashlib

# Simple Caesar cipher for name encryption/decryption
def encrypt_name(name, shift=3):
    return ''.join(chr((ord(c) + shift) % 256) for c in name)

def decrypt_name(name, shift=3):
    return ''.join(chr((ord(c) - shift) % 256) for c in name)

# Secure SHA256 hashing for password storage
def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_hash, provided_password):
    return stored_hash == encrypt_password(provided_password)
