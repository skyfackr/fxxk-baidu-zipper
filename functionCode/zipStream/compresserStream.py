'''
@author:skyfackr
@des:流式压缩
'''
from .streamReaderMixin import streamReaderMixiner
import pylzma,time,logging
from ..globalEnvironmention import globalEnv
class compresser(streamReaderMixiner):
    '''
        流式压缩
        '''
    #__slots__=['__init__','get']
    def __init__(self,file_object,fastBytes:int=int(globalEnv.fastBytes)):
        
        self.__fileObj=file_object
        self.__fb=fastBytes
        try:
            self.__file=file_object.read()
        except AttributeError:
            self.__file=file_object
        return
    
    def get(self):
        '''
        读取压缩数据并返回使用时间

        'return'第一个为数据，第二个为时间
        '''
        logging.info('start compressing')
        start_time=time.time()
        data=pylzma.compress(self.__file,fastBytes=self.__fb,eos=True)
        end_time=time.time()
        logging.info('compress complete,use time:{}'.format(end_time-start_time))
        return data,end_time-start_time



