'''
@author:skyfackr
@des:各种mixin
'''
from Crypto.Cipher import AES
import logging
from goto import with_goto
from ..ossmiddleware.streamReaderMixin import streamReaderMixiner
class fileLikeTranslationMixin(streamReaderMixiner):
    '''
    用于将filelike完全读取或者将字符串转为filelike的mixin
    '''
    def _setFilelikeReading(self,text:str):
        '''
        将字符串转为filelike
        '''
        self.__filelike_read_data=text
        self.__length=len(text)
        self.__flush_needed=False
        return
        
    @with_goto
    def read(self,num:int=None):
        label .reset
        self.__flush_needed=False
        nowstr=self.__filelike_read_data
        if num==None:
            num=self.__length
        now=0
        last=num
        while True:
            if self.__filelike_read_data!=nowstr or self.__flush_needed==True:
                goto .reset
            if num==self.__length:
                yield self.__filelike_read_data
                continue
            if now>=self.__length:
                yield None
            yield self.__filelike_read_data[now:last]
            now=last
            last+=num
            last=min(last,self.__length)


    def _transToStr(self,obj):
        '''
        将filelike转换为字符串
        '''
        return str(self._streamRead(obj))

    def flush_read(self):
        '''
        直接刷新read读取坐标至开头
        '''
        self.__flush_needed=True
        return




class AESPaddingMixin():
    '''
    用于aes的pad填充的mixin
    '''
    def _pkcs7_pad(self,text):
        '''
        pkcs7填充
        '''
        blocksize=AES.block_size
        length=len(text.encode('utf-8'))
        padding=blocksize-length%blocksize
        return str(text+padding*chr(padding))

    
    def _pkcs7_unpad(self,text):
        '''
        pkcs7解除填充
        '''
        length=len(text)
        unpadsize=ord(text[length-1])
        return text[0:length-unpadsize]