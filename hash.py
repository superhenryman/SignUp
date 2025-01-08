import hashlib
def hash_text(data):
    sha256 = hashlib.sha256()
    sha256.update(data.encode('utf-8'))
    hashed_text = sha256.hexdigest()
    return hashed_text