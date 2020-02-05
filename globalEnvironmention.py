'''
@author:skyfackr
@des:用于获取全局环境变量，对于不存在的变量，则会抛出异常
'''
import os,logging
class globalEnv():
    '''
    获取全局环境变量
    '''
    #允许使用的变量名称
    __Member__=['OSSBucketName',
    'allow_zip_mode',
    'allow_unzip_mode',
    'support_encrypt_class',
    'OSSMaxinumDownload',
    'OSSMaxinumUpload',
    'OSSDownloadThread',
    'OSSUploadThread']
    #直接输出的常量名，若不在此字典则读取系统环境变量，要求名称必须在__Member__中
    __envStaticMember={}
    def isMenber(self,name):
        '''
        测试环境变量是否存在
        '''
        if name in self.__Member__:
            return True
        return False

    def __getattr__(self,name):
        logger=logging.getLogger()
        logger.info('get env:{}'.format(str(name)))
        if not self.isMenber(name):
            raise AttributeError('OS Env have no attribute called {}'.format(name))
        if name in self.__envStaticMember.keys():
            return self.__envStaticMember[name]
        return os.environ.get(name)

