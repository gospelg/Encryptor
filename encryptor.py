from Crypto.Cipher import AES
import hashlib
import os
import random
import struct

def get_file():
    working_file = raw_input("Input the file to encrypt or decrypt. Type the path exactly.\n")
    try:
        os.path.isfile(working_file)
        return working_file
    except:
        print "That is not a valid file."
        get_file()
def encrypt(file, chunksize=64*1024):
    #record the original filesize
    filesize = os.path.getsize(file)
    password = raw_input("Please enter the password\n")
    #encryption key is a hash of the password
    key = hashlib.sha256(password).digest()
    #set initialization vector
    iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])
    encryption_engine = AES.new(key, AES.MODE_CBC, iv)
    outfile_name = file + '.enc'
    with open(file, 'rb') as infile:
        with open(outfile_name, 'wb') as outfile:
           #write size of og file to new file
           outfile.write(struct.pack('<Q', filesize))
           outfile.write(iv)
           #make sure chunks are the corect size, then encrypt and write
           while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)
                outfile.write(encryption_engine.encrypt(chunk))
    print "Your file has been encrypted."
    main()
def decrypt(file, chunksize=64*1024):
    password = raw_input("Please enter the password\n")
    #encryption key is a hash of the password, originally used to encrypt
    key = hashlib.sha256(password).digest()
    #the decrypted file will be the same name, just without the added .enc ext
    outfile_name = os.path.splitext(file)[0]

    with open(file, 'rb') as infile:
        og_size = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(outfile_name, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
            #delete added padding when encrypted
            outfile.truncate(og_size)
    print "Your file has been decrypted."
    main()
def main(): #main input loop

    print "Welcome to file encryptor. Type exit at any time to end."
    encrypt_action = raw_input("Would you like to encrypt a file? (Y or N)\n")
    if encrypt_action.lower() == 'y':
        working_file = get_file()
        encrypt(working_file)
    elif encrypt_action.lower() == 'n':
        decrypt_action = raw_input("Would you like to decrypt a file? (Y or N)\n")
        if decrypt_action.lower() == 'y':
            working_file = get_file()
            decrypt(working_file)
        elif decrypt_action == 'exit':
            exit()
        else:
            main()
    elif encrypt_action == 'exit':
        exit()
    else:
        main()
main()
