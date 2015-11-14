from Crypto.Cipher import AES
import base64, os

class Encryptor():

    def __init__(self, passWord):

        padKey = lambda s: s + (AES.block_size-(len(s)%AES.block_size))*'{'
        self.passWord = padKey(passWord)
        self.IV = os.urandom(AES.block_size)
        print(self.IV)
        self.cipher = AES.new(self.passWord, AES.MODE_CBC, self.IV)

    def pad(self, s):

        return  s + b"\0" * (AES.block_size - len(s)%AES.block_size)

    def encrypt_files(self, filePaths):

        for f in filePaths:
            with open(f,'rb') as fid:
                plainText = fid.read()
            enc = self.cipher.encrypt(self.pad(plainText))
            with open(f+'.enc', 'wb') as fidout:
                fidout.write(self.IV)
                fidout.write(enc)

    def decrypt_files(self, filePaths):

        for f in filePaths:
            with open(f, 'rb') as fid:
                enc = fid.read()
            print(enc[:AES.block_size])
            decrypter = AES.new(self.passWord, AES.MODE_CBC, enc[:AES.block_size])
            decData = decrypter.decrypt(enc[AES.block_size:])
            with open(f[:-4], 'wb') as fidout:
                fidout.write(decData)



if __name__ == '__main__':

    e =Encryptor('f7B$APA8')
    #e.encrypt_files([r'C:\Users\Pysenberg\Desktop\encyrption test\the_yank_we_can_t_be_stop_d_original_mix.mp3'])
    e.decrypt_files([r'C:\Users\Pysenberg\Desktop\encyrption test\the_yank_we_can_t_be_stop_d_original_mix.mp3.enc'])