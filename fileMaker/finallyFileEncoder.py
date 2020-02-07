'''
@author:skyfackr
@des:将最终数据进行校验生成以及封装
'''
from Crypto.Hash import  SHA256
from datetime import time,datetime
from ..globalEnvironmention import globalEnv
from ..securityStream import AESDecryptStream
from ..zipStream import decompresser
from ..securityStream.mixin import fileLikeTranslationMixin
import base64



def encoder(fin_data,isEncrypt:bool,res_data,before_enc_data=None):
    '''
    封装数据

    :param fin_data:最终数据
    :param isEncrypt:是否加密
    :param res_data:原数据
    :param before_enc_data:加密前数据，如果加密则此项必选
    '''
    if isEncrypt and before_enc_data==None:
        raise ValueError('before_enc_data must be given if isEncrypt is True')
    fin_sha=SHA256.new(fin_data.encode('utf-8')).hexdigest()
    res_sha=SHA256.new(res_data.encode('utf-8')).hexdigest()
    if isEncrypt:
        benc_sha=SHA256.new(before_enc_data.encode('utf-8')).hexdigest()
    else:
        benc_sha=''
    timestamp=str(int(time.mktime(time.strptime(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S'))))
    ver=str(globalEnv.Version)
    fin_size=str(len(fin_data))
    res_size=str(len(res_data))
    is_enc=0
    if isEncrypt:
        is_enc=1
    header=ver+'|'+timestamp+'|'+res_size+'|'+fin_size+'|'+is_enc+'|'+benc_sha+'|'+fin_sha+'|'+res_sha
    all_data=str(len(header))+'|'+header+'||'+fin_data
    all_sha=SHA256.new(all_data.encode('utf-8')).hexdigest()
    all_data=all_sha+'|'+all_data
    all_data=base64.b64encode(all_data.encode('utf-8'))
    return all_data

