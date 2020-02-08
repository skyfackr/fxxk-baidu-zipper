'''
@author:skyfackr
@des:compress的应用封装
'''
from ..globalEnvironmention import globalEnv
from ..ossmiddleware import ossMiddleware
import logging,json
from ..fileMaker import encoder
from Crypto.Hash import SHA256
from .returnMaker import __failedReturnMaker,__successReturnMaker

def compress(download_path,upload_path,password=None):
    '''
    应用compress
    '''
    logging.info('action compress:'+json.dumps({
        'download_path':download_path,
        'upload_path':upload_path
    }))
    OSSMW:ossMiddleware=globalEnv.OSSMW
    try:
        logging.info('starting download file:{}'.format(download_path))
        res_data=OSSMW.download(download_path)
    except ossMiddleware.errors.DownloadError as e:
        logging.warn('download error:'+str(e))
        return __failedReturnMaker('OSSDownloadError',str(e))
    logging.info('download {} complete.starting encoding file...'.format(download_path))
    all_data,time=encoder(res_data,password=password)
    logging.info('encode {} complete.starting uploading to {}'.format(download_path,upload_path))
    try:
        OSSMW.upload(all_data,upload_path)
    except ossMiddleware.errors.UploadError as e:
        logging.warn('upload error:'+str(e))
        return __failedReturnMaker('OSSUploadError',str(e))
    logging.info('upload to {} complete'.format(upload_path))
    sha256=SHA256.new(all_data).hexdigest()
    return __successReturnMaker(time,upload_path,sha256)