'''
@author:skyfackr
@des:decompress的应用封装
'''
from ..globalEnvironmention import globalEnv
from ..ossmiddleware import ossMiddleware
import logging,json
from ..fileMaker import decoder,UnsupportError,VerificationError
from Crypto.Hash import SHA256
from .returnMaker import __failedReturnMaker,__successReturnMaker

def decompress(download_path,upload_path,password=None):
    '''
    应用decompress
    '''
    mode='decompress'
    logging.info('action decompress:'+json.dumps({
        'download_path':download_path,
        'upload_path':upload_path
    }))
    OSSMW:ossMiddleware=globalEnv.OSSMW
    try:
        logging.info('start downloading file{}'.format(download_path))
        all_data=OSSMW.download(download_path)
    except ossMiddleware.errors.DownloadError as e:
        logging.warn('download error:'+str(e))
        return __failedReturnMaker('OSSDownloadError',str(e),mode)
    logging.info('download {} complete.starting decoding file...'.format(download_path))
    if round(len(all_data)/1024/1024)>int(globalEnv.MaxDecompressFileSizeWithMbytes):
        return __failedReturnMaker('OutOfSizeError','your file size is to large({}m).system limit is {}m'.format(str(round(len(all_data)/1024/1024)),str(globalEnv.MaxDecompressFileSizeWithMbytes)),mode)
    try:
        fin_data,is_enc,res_data,benc_data,time=decoder(all_data,password)
    except UnsupportError as e:
        logging.warn('decode {} failed.type donot support({})'.format(download_path,str(e)))
        return __failedReturnMaker('FileTypeError','FileTypeError({})'.format(str(e)),mode)
    except VerificationError as e:
        logging.warn('decode {} failed.verify failed({})'.format(download_path,str(e)))
        return __failedReturnMaker('VerifactionError','VerifactionError({})'.format(str(e)),mode)
    logging.info('decode {} complete.starting uploading to {}'.format(download_path,upload_path))
    try:
        OSSMW.upload(res_data,upload_path)
    except ossMiddleware.errors.UploadError as e:
        logging.warn('upload error:'+str(e))
        return __failedReturnMaker('OSSUploadError',str(e),mode)
    logging.info('upload to {} complete'.format(upload_path))
    sha256=SHA256.new(res_data).hexdigest()
    return __successReturnMaker(time,upload_path,sha256,len(res_data),mode)