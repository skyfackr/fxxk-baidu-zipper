'''
@author:skyfackr
@des:oss中间件主文件
'''
import oss2,logging,tempfile,traceback,sys,json,os
from ..globalEnvironmention import globalEnv
from .streamReaderMixin import streamReaderMixiner
class ossMiddleware(streamReaderMixiner):
    '''
    oss中间件
    '''
    class errors():
        class DownloadError(Exception):
            pass
        class UploadError(Exception):
            pass


    def __init__(self,id,secret,token,bucket=globalEnv.OSSBucketName,endpoint=globalEnv.OSSEndpoint):
        self.__id=id
        self.__secret=secret
        self.__token=token
        self.__bucket=bucket
        self.__endpoint=endpoint
        auth=oss2.StsAuth(id,secret,token,auth_version=oss2.AUTH_VERSION_2)
        oss2.set_stream_logger(level=logging.WARNING)
        self.__client=oss2.Bucket(auth,endpoint,bucket)
        logging.info('link oss complete,bucket:{},endpoint:{}'.format(bucket,endpoint))
        return

    def download(self,filepath,maxinum_try=int(globalEnv.OSSMaxinumDownload),threads=int(globalEnv.OSSDownloadThread)):
        '''
        下载文件
        '''
        tmpname=tempfile.mktemp()
        trytime=0
        while True:
            if trytime>=maxinum_try:
                raise self.errors.DownloadError('Interal error')
            trytime+=1
            logging.info('start download {} for {} time'.format(filepath,trytime))
            try:
                oss2.resumable_download(self.__client,filepath,tmpname,num_threads=threads)
            except Exception as e:
                etype,evalue,emsg=sys.exc_info()
                logging.warn('download {} failed at {} time:{}'.format(filepath,trytime,json.dumps({
                    'etype':str(etype),
                    'evalue':str(e),
                    'traceback':str(traceback.format_tb(emsg))
                })))
                if trytime>=maxinum_try:
                    logging.warn('download {} aborted'.format(filepath))
                    raise self.errors.DownloadError('download failed and timeout')
            else:
                logging.info('download {} finished'.format(filepath))
                break
        if not os.path.exists(tmpname):
            logging.error('cannot find downloaded file!')
            raise self.errors.DownloadError('Interal error')
        with open(tmpname,'rb') as fp:
            data=fp.read()
        os.remove(tmpname)
        return data



    def upload(self,filedata,filename,maxinum_try=int(globalEnv.OSSMaxinumUpload),threads=int(globalEnv.OSSUploadThread)):
        '''
        上传文件
        '''
        tmp=tempfile.NamedTemporaryFile(mode='rb+')
        tmp.write(filedata)
        tmp.flush()
        tmp.seek(0)
        trytime=0
        while True:
            if trytime>=maxinum_try: 
                tmp.close()
                raise self.errors.UploadError('Interal error')
            trytime+=1
            logging.info('start upload {} for {} time'.format(filename,trytime))
            try:
                oss2.resumable_upload(self.__client,filename,tmp.name,num_threads=threads)
            except Exception as e:
                etype,evalue,emsg=sys.exc_info()
                logging.warn('upload {} failed at {} time:{}'.format(filename,trytime,json.dumps({
                    'etype':str(etype),
                    'evalue':str(e),
                    'traceback':str(traceback.format_tb(emsg))
                })))
                if trytime>=maxinum_try:
                    logging.warn('upload {} aborted'.format(filename))
                    tmp.close()
                    raise self.errors.UploadError('Upload failed and timeout')
            else:
                logging.info('upload {} finished'.format(filename))
                break
        tmp.close()
        return






