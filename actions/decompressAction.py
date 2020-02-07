'''
@author:skyfackr
@des:decompress的应用封装
'''
from ..globalEnvironmention import globalEnv
from ..ossmiddleware import ossMiddleware
import logging,json
from ..fileMaker import decoder,UnsupportError,VerificationError
from Crypto.Hash import SHA256
def __failedReturnMaker(errcode,errmsg):
    '''
    失败时生成返回信息
    '''
    return {
        'success':False,
        'msg':{
            'errcode':str(errcode),
            'errmsg':str(errmsg)
        }
    }


def __successReturnMaker(time,path,sha256):
    '''
    成功时返回成功信息
    '''
    return {
        'success':True,
        'msg':{
            'time':int(time),
            'path':str(path),
            'sha256':str(sha256)
        }
    }

def decompress(download_path,upload_path,password=None):
    '''
    应用decompress
    '''
    logging.info('action decompress:'+json.dumps({
        'download_path':download_path,
        'upload_path':upload_path
    }))
    OSSMW:ossMiddleware=globalEnv.OSSMW
    try:
        logging.info('downloading {}...'.format(download_path))
        all_data=OSSMW.download(download_path)
    except ossMiddleware.errors.DownloadError as e:
        logging.warn('download error:'+str(e))
        return __failedReturnMaker('OSSDownloadError',str(e))
    logging.info('download {} complete.starting decoding file...'.format(download_path))
    try:
        fin_data,is_enc,res_data,benc_data,time=decoder(all_data,password)
    except UnsupportError:
        logging.warn('decode {} failed.type donot support'.format(download_path))
        return __failedReturnMaker('FileTypeError','FileTypeError')
    except VerificationError:
        logging.warn('decode {} failed.verify failed'.format(download_path))
        return __failedReturnMaker('VerifactionError','VerifactionError')
    logging.info('decode {} complete.starting uploading to {}'.format(download_path,upload_path))
    try:
        OSSMW.upload(res_data,upload_path)
    except ossMiddleware.errors.UploadError as e:
        logging.warn('upload error:'+str(e))
        return __failedReturnMaker('OSSUploadError',str(e))
    logging.info('upload to {} complete'.format(upload_path))
    sha256=SHA256.new(res_data).hexdigest()
    return __successReturnMaker(time,upload_path,sha256)