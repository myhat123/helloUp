from cryptography.fernet import Fernet

def encrypt(token: str, acc: str) -> str:
    '''加密'''

    f = Fernet(token.encode())
    return f.encrypt(acc.encode()).decode()

def decrypt(token: str, enc_acc: str) -> str:
    '''解密'''

    f = Fernet(token.encode())
    return f.decrypt(enc_acc.encode()).decode()

if __name__ == '__main__':
    key = Fernet.generate_key()
    
    #从byte转str
    token = key.decode()

    s = encrypt(token, '62174378490347')
    print(s)

    t = decrypt(token, s)
    print(t)