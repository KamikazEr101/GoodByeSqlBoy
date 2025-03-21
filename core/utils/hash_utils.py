import hashlib

# 对输入的自然语言进行加密
def sha256_encrypt(input_string):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_string.encode('utf-8'))
    return sha256_hash.hexdigest()