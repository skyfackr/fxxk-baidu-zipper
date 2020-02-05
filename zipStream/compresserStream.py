'''
@author:skyfackr
@des:流式压缩
'''
from .streamReaderMixin import streamReaderMixiner
import pylzma,time,logging
class compresser(streamReaderMixiner):
    '''
        流式压缩
        '''
    def __init__(self,file_object):
        
        self.__fileObj=file_object
        self.__zipper=pylzma.compressfile(file_object,fastBytes=255,eos=True)
        return
    
    def get(self):
        '''
        读取压缩数据并返回使用时间

        'return'第一个为数据，第二个为时间
        '''
        logging.info('start compressing')
        start_time=time.time()
        data=self._streamRead(self.__zipper)
        end_time=time.time()
        logging.info('compress complete,use time:{}'.format(end_time-start_time))
        return data,end_time-start_time



