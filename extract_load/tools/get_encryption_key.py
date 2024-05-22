from cryptography.fernet import Fernet

key = Fernet.generate_key()
print(key.decode())  # Copy this key and store it in your .env file
