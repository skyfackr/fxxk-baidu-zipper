'''
@author:skyfackr
@des:aes流式输出
'''
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import SHA256
from .mixin import fileLikeTranslationMixin,AESPaddingMixin
import base64,logging
class AESEncryptStream(fileLikeTranslationMixin,AESPaddingMixin):
    '''
    流式加密aes
    '''
    def __init__(self,data,password):
        self.__data=data
        self.__pw=password
        self.__bs=AES.block_size
        self.__iv=Random.new().read(16)
        enc_data=self._pkcs7_pad(base64.b64encode(self.__data))
        enc_password=SHA256.new().update(password.encode('utf-8'))[:31]
        self.__secret=self.__iv+AES.new(enc_password,AES.MODE_CBC,self.__iv).encrypt(enc_data)
        self._setFilelikeReading(self.__secret)
        logging.info('encrypt data:{} complete with password:{}'.format(self.__data,self.__pw))
        return

class AESDecryptStream(fileLikeTranslationMixin,AESPaddingMixin):
    '''
    流式解密aes
    '''
    def __init__(self,data,password):
        self.__data=data
        self.__pw=password
        self.__iv=data[0:15]
        dec_data=data[16:]
        dec_password=SHA256.new().update(password.encode('utf-8'))[:31]
        self.__ans=base64.b64decode(self._pkcs7_unpad(AES.new(dec_password,AES.MODE_CBC,self.__iv).decrypt(dec_data)))
        self._setFilelikeReading(self.__ans)
        logging.info('decrypt data:{} complete with password:{}'.format(self.__data,self.__pw))
        return