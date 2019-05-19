#!/usr/bin/env python
#
# AES cryptography algorithm implementation in Counter mode
#
# Author: Radek Domanski
# email: radek.domanski # gmail.com

from Crypto.Cipher import AES
from Crypto.Util import Counter
import sys, argparse

def main():
    cmd = argparse.ArgumentParser(
	    prog="aes-ctr.py",
	    formatter_class=argparse.RawDescriptionHelpFormatter,
	    description = '''
	    \rAES implementation in counter mode. This version supports 128 bits key encryption only.
	    \rThis is experimental script. NO INPUT VALIDATION
	    ''',
	    epilog = '''
	    \rExemplary usage:\n
	    \r2) Decryption
	    \r$ decrypt_files -i ciphertext -o plaintext -k abcdef1234567890abcdef1234567890 
	    ''')
    cmd.add_argument("-i", "--input", help="File containing plaintext/ciphertext", type=str, required=True, metavar="IN")
    cmd.add_argument("-o", "--output", help="Output file to store result of the program", type=str, metavar="OUT")
    cmd.add_argument("-k", "--key", help="Encryption 128bits key", type=str, required=True)

    args=cmd.parse_args()	
    
    # Retrieve options and arguments # 
    if args.output:
	OUT_FILE = args.output
    else:
	OUT_FILE = ''

    IN_FILE = args.input

    KEY = validateHex(args.key)
   
    # Read file that contains plaintext / ciphertext #  
    f = open(IN_FILE, 'rb')

    # Read bytes of IV
    IV = (f.read(16)).encode("hex")

    # Read the all file
    text = f.read()
    f.close()

    # If key or init counter didn't pass validation test then abort #
    if KEY and IV:

	# Decryption #
	crypto(text.encode("hex"), KEY, IV, OUT_FILE)

    else:
	print "Invalid Key or iv"

# Validate if passed value is hexadecimal and has proper length #
# Function returns passed argument if value is correct #
# If passed value is not valid, function returns False #
def validateHex(hex):
    if len(hex) is not 32:
	return False
    else:
	try:
	    int(hex,16)
	    return hex
	except ValueError:
	    return False

# Core function that performs encryption / decryption #
def crypto(text, key, iv, output):

    BlockSizeForHex = 16;
    encryptionKey = key.decode("hex")

    # Create new Counter object #
    # Object will automatically increment counter on each cryptographic round #
    counter = Counter.new(128, initial_value=int(iv,16))

    # Create new AES CTR object #
    cipher=AES.new(encryptionKey, AES.MODE_CTR, counter=counter)

    result = ''

    # Iterate over the all file's bytes #
    for i in range(0,len(text),BlockSizeForHex):

	# AES CTR operates on 16 bytes blocks #
	block = text[i:i+BlockSizeForHex]
	
	#Decryt all bytes of each block
	result += cipher.decrypt(block.decode("hex"))

    if output:
	f = open(output,'wb')
	f.write(result)
	f.close()
    else:
	print result

if __name__ == '__main__':
    main()

