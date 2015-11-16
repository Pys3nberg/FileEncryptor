from Crypto.Cipher import AES
import hashlib, os

def pad(s):
    # Take in a binary string and pad it so that we can make the data full blocks of 16bytes, which is teh block size
    # used by the AES encryption algo
    return  s + b"\x00" * (AES.block_size - len(s)%AES.block_size)

def setup_cipher(key):
    # A simple padding anonymous function to make sure the key is 16bytes long
    padKey = lambda s: s + (AES.block_size-(len(s)%AES.block_size))*'{'
    passWord = padKey(key)
    # Generate a random IV, this will be included in the file
    IV = os.urandom(AES.block_size)
    # Setup the cipher
    cipher = AES.new(passWord, AES.MODE_CBC, IV)
    # Return the cipher object and IV
    return cipher, IV


def encrypt_file(key, file):
        # The key must be between 1 and 16 characters long
        if len(key) <= 16:
            # Setup a d new cipher
            cipher, IV = setup_cipher(key)
            # Check to see if there is an encrypted directory, if not make one
            if not(os.path.isdir(os.path.join(os.path.dirname(file), 'encrypted'))):
                os.mkdir(os.path.join(os.path.dirname(file), 'encrypted'))
            # Open and read the content of the file passed in
            with open(file,'rb') as fid:
                plainText = fid.read()
            # Encrypt the data
            enc = cipher.encrypt(pad(plainText))
            # Generate a new path name for the encrypted file
            newFilePath = os.path.join(os.path.dirname(file), 'encrypted', os.path.basename(file)+'.enc')
            # Open the new file to write too
            with open(newFilePath, 'wb') as fidout:
                # First we right the original file size plus a null char so that we can get rid of padding properly
                # when decrypting
                fidout.write(str(os.path.getsize(file)).encode()+b'\x00')
                # Write the 16byte IV
                fidout.write(IV)
                # Write the encrypted data
                fidout.write(enc)
                # Finally write the a 32byte MD5 checksum so that when decrypting we can check the integrity
                fidout.write(hashlib.md5(plainText).hexdigest().encode('utf-8'))

        elif len(key) == 0:
            print('Please Enter a Key')

        else:
            print('please enter a key which is between 1 and 16 characters long.')

def decrypt_file(key, file):
        # A simple padding anonymous function to make sure the key is 16bytes long
        padKey = lambda s: s + (AES.block_size-(len(s)%AES.block_size))*'{'
        passWord = padKey(key)
        # Open the encrypted file and read in data
        with open(file, 'rb') as fid:
            # Read in data and split at the first null char found, the first element will be th filesize,
            # the rest of teh data will be IV, encrypted data and checksum
            data = fid.read().split(b'\x00', 1)
            fileSize = int(data[0].decode())
            enc = data[1]
        # Create a cipher using the IV found in the file (first 16bytes after the file size)
        decrypter = AES.new(passWord, AES.MODE_CBC, enc[:AES.block_size])
        # Decrypt the file using the IV at the beginning of the file and the data up to the checksum
        # also get rid of the padding using teh file size we found.
        decData = decrypter.decrypt(enc[AES.block_size:-32])[:fileSize]
        # Perform and MD5 checksum on the decrypted data and compare to the checksum from the file, only write
        # The new file if the check sums match
        if hashlib.md5(decData).hexdigest() == enc[-32:].decode('utf-8'):
            with open(file[:-4], 'wb') as fidout:
                fidout.write(decData)
        else:
            print('Checksum check failed, please check your password')

if __name__ == '__main__':

    encrypt_file('hello', 'spec.txt')
    decrypt_file('hello', os.path.join('encrypted','spec.txt.enc'))