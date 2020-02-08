'''
@author:skyfackr
@des:对文件数据生成并调用封装输出
'''
from .finallyFileEncoder import encoder
from ..securityStream import AESEncryptStream
from ..zipStream import compresser
import logging,tempfile
from ..securityStream.mixin import fileLikeTranslationMixin

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
    benc_data,compress_time=compresser(data).get()
    if not is_enc:
        fin_data=benc_data
        benc_data=None
    else:
        tmp=tempfile.NamedTemporaryFile(mode='rb+')
        tmp.write(data)
        tmp.flush()
        tmp.seek(0)
        del data
        gen=AESEncryptStream(benc_data,password).read()
        fin_data=gen.__next__()
    all_data=encoder(fin_data,is_enc,tmp.read(),benc_data)
    return all_data,compress_time