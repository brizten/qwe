from cryptography.fernet import Fernet

# Define the key
key = b''

# Create a Fernet cipher instance with the key
cipher = Fernet(key)


def encrypt_message(message):
    message_bytes = message.encode()
    encrypted_message = cipher.encrypt(message_bytes)
    return encrypted_message


def decrypt_message(encrypted_message):
    decrypted_message = cipher.decrypt(encrypted_message)
    decrypted_string = decrypted_message.decode()
    return decrypted_string


message = "pctrpassword"
encrypted = encrypt_message(message)
print("Encrypted message:", encrypted)

decrypted = decrypt_message(encrypted)
print("Decrypted message:", decrypted)
