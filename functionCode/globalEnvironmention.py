'''
@author:skyfackr
@des:用于获取全局环境变量，对于不存在的变量，则会抛出异常
'''
import os,logging
class __GLOBALENV():
    '''
    （切勿直接使用,请使用globalEnv）获取全局环境变量
    '''
    #允许使用的变量名称
    __Member__=['OSSBucketName',
    'allow_zip_mode',
    'allow_unzip_mode',
    'support_encrypt_class',
    'OSSMaxinumDownload',
    'OSSMaxinumUpload',
    'OSSDownloadThread',
    'OSSUploadThread',
    'Version',
    'support_mode',
    'OSSMW',
    'instanceID',
    'OSSEndpoint',
    'fastBytes',
    'MaxCompressFileSizeWithMbytes',
    'MaxDecompressFileSizeWithMbytes',
    'EncryptKeyMD5Times',]
    #直接输出的常量名，若不在此字典则读取系统环境变量，要求名称必须在__Member__中
    __envStaticMember={}
    @classmethod
    def isMember(cls,name):
        '''
        测试环境变量是否存在
        '''
        if name in cls.__Member__:
            return True
        return False

    @classmethod
    def __getattr__(self,name):
        logger=logging.getLogger()
        logger.debug('get env:{}'.format(str(name)))
        if not self.isMember(name):
            raise AttributeError('OS Env have no attribute called {}'.format(name))
        if name in self.__envStaticMember.keys():
            return self.__envStaticMember[name]
        return os.environ.get(name)


    def setStaticMember(self,name,value):
        '''
        设定直接输出变量，变量名必须注册于__Member__，否则抛出异常
        '''
        if not self.isMember(name):
            raise AttributeError('OS Env have no attribute called {}'.format(name))
        self.__envStaticMember[name]=value
        logging.debug('set member:{} to {}'.format(name,str(value)))
        return







#我杀bug它全家
globalEnv=__GLOBALENV()