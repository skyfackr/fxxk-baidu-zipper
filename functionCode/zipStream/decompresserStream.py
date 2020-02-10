'''
@author:skyfackr
@des:流式解压
'''
import pylzma,time,logging
from .streamReaderMixin import streamReaderMixiner
class decompresser(streamReaderMixiner):
    '''
    流式解压
    '''
    def __init__(self,file_object):
        self.__fileObj=file_object
        try:
            self.__file=file_object.read()
        except AttributeError:
            self.__file=file_object
        return

    def get(self):
        '''
        读取解压数据并返回使用时间

        'return'第一个为数据，第二个为时间
        '''
        logging.info('start decompressing')
        start_time=time.time()
        data=pylzma.decompress(self.__file)
        end_time=time.time()
        use_time=end_time-start_time
        logging.info('decompress complete,using time:{}'.format(use_time))
        return data,use_time