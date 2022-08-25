from cryptography.fernet import Fernet
import pickle

key = Fernet.generate_key()
fernet = Fernet(key)
keyfile = open("new_key.key", "wb")
pickle.dump(fernet, keyfile)
keyfile.close()