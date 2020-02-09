'''
@author:skyfackr
@des:对文件数据生成并调用封装输出
'''
from .finallyFileEncoder import encoder
from ..securityStream import AESEncryptStream
from ..zipStream import compresser
import logging,tempfile,gc
from ..securityStream.mixin import fileLikeTranslationMixin
from Crypto.Hash import SHA256
from ..memoryLogger import log_mem

def file_encode(data,password:str=None):
    '''
    封装函数

    返回两个参数，第一个为数据，第二个为压缩时间

    :param data:数据

    :param password:密码，如果不需要加密则无需此项
    '''
    #测试密码是否存在
    is_enc=False
    if password!=None:
        is_enc=True
    #压缩
    gc.enable()
    #gc.set_debug(gc.DEBUG_UNCOLLECTABLE)
    gc.collect()
    res_size=len(str(data))
    res_sha=SHA256.new(data).hexdigest()
    #log_mem()
    benc_data,compress_time=compresser(data).get()
    #log_mem()
    #logging.info('wait del')
    del data
    #logging.info('deled')
    gc.collect()
    #logging.info(gc.garbage)
    #log_mem()
    if not is_enc:
        fin_data=benc_data
        benc_sha=None
        del benc_data
    else:
        benc_sha=SHA256.new(benc_data)
        gen=AESEncryptStream(benc_data,password).read()
        fin_data=gen.__next__()
        del benc_data
        del password
    gc.collect()
    all_data=encoder(fin_data,is_enc,res_sha,res_size,benc_sha)
    return all_data,compress_time