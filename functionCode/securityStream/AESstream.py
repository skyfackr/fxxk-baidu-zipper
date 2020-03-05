'''
@author:skyfackr
@des:aes流式输出
'''
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import SHA256,MD5
from .mixin import fileLikeTranslationMixin,AESPaddingMixin
import base64,logging,gc
from ..globalEnvironmention import globalEnv
class AESEncryptStream(fileLikeTranslationMixin,AESPaddingMixin):
    '''
    流式加密aes
    '''
    def __init__(self,data,password):
        #self.__data=data
        self.__pw=password
        self.__bs=AES.block_size
        self.__iv=Random.new().read(16)
        #b64data=base64.b16encode(data)
        b64data=data
        del data
        gc.collect()
        enc_data=self._pkcs7_pad(b64data)
        del b64data
        gc.collect()
        for i in range(int(globalEnv.EncryptKeyMD5Times)):
            password=MD5.new(password.encode('utf-8')).hexdigest()
        enc_password=password.encode()
        self.__secret=self.__iv+AES.new(enc_password,AES.MODE_CBC,self.__iv).encrypt(enc_data)
        del enc_data
        gc.collect()
        self._setFilelikeReading(self.__secret)
        logging.info('encrypt data complete')
        return

class AESDecryptStream(fileLikeTranslationMixin,AESPaddingMixin):
    '''
    流式解密aes
    '''
    def __init__(self,data,password):
        #self.__data=data
        #self.__pw=password
        self.__iv=data[0:16]
        dec_data=data[16:]
        for i in range(int(globalEnv.EncryptKeyMD5Times)):
            password=MD5.new(password.encode('utf-8')).hexdigest()
        dec_password=password.encode()
        #self.__ans=base64.b16decode(self._pkcs7_unpad(AES.new(dec_password,AES.MODE_CBC,self.__iv).decrypt(dec_data)))
        self.__ans=self._pkcs7_unpad(AES.new(dec_password,AES.MODE_CBC,self.__iv).decrypt(dec_data))
        self._setFilelikeReading(self.__ans)
        logging.info('decrypt  complete')
        return