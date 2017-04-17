#!/usr/bin/env python

import sys, hashlib

try:
    import rncryptor
except ImportError:
    print "do pip install -r requirements.txt"
    sys.exit(-1)


def get_password(email):
    data = "010104KEY" + email
    return hashlib.md5(data).hexdigest()

def decrypt_data(data, password):
    cryptor = rncryptor.RNCryptor()
    decrypted_data = None
    try:
        decrypted_data = cryptor.decrypt(data, password)
    except rncryptor.DecryptionError as e:
        print "Decrypted file seems to be invalid! (probably wrong e-mail used?)"
        raise e

    return decrypted_data

def verify_data_is_zip(data):
    return data.startswith("PK")

def main():
    if len(sys.argv) != 4:
        print "Usage: %s your@email.com input-file.sifri output.epub" % sys.argv[0]
        return

    email, in_file, out_file = sys.argv[1:]

    password = get_password(email)
    encrypted_data = open(in_file, "rb").read()
    decrypted_data = decrypt_data(encrypted_data, password)
    open(out_file, "wb").write(decrypted_data)

    if verify_data_is_zip(decrypted_data):
        print "Successfully decrypted epub into:", out_file
    else:
        print "Decrypted file seems to be invalid! (probably wrong e-mail used?)"


if __name__ == "__main__":
    main()
