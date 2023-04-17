from twofish import Twofish
import os
from dotenv import load_dotenv

BLOCK_SIZE = 16

load_dotenv()

ENCRYPT_KEY = os.getenv('ENCRYPT_KEY')


def encrypt(plaintext):
    if len(plaintext) % BLOCK_SIZE:  # add padding
        padded_plaintext = str(
            plaintext+'%'*(BLOCK_SIZE-len(plaintext) % BLOCK_SIZE)).encode('utf-8')
    else:
        padded_plaintext = plaintext.encode('utf-8')
    T = Twofish(str.encode(ENCRYPT_KEY))
    ciphertext = b''
    for x in range(int(len(padded_plaintext)/BLOCK_SIZE)):
        ciphertext += T.encrypt(padded_plaintext[x*BLOCK_SIZE:(x+1)*BLOCK_SIZE])
    return ciphertext


def decrypt(ciphertext):
    T = Twofish(str.encode(ENCRYPT_KEY))
    plaintext = b''
    for x in range(int(len(ciphertext)/BLOCK_SIZE)):
        plaintext += T.decrypt(ciphertext[x*BLOCK_SIZE:(x+1)*BLOCK_SIZE])
    return str.encode(plaintext.decode('utf-8').strip('%'))
