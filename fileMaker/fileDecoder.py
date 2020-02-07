'''
@author:skyfackr
@des:文件分析并解压
'''
from Crypto.Hash import  SHA256
from datetime import time,datetime
from ..globalEnvironmention import globalEnv
from ..securityStream import AESDecryptStream
from ..zipStream import decompresser
from ..securityStream.mixin import fileLikeTranslationMixin
import base64
class UnsupportError(Exception):
    pass
class VerificationError(Exception):
    pass

def decoder(all_data:str,password):
    '''
    解封装数据

    返回5个数据，依次为原数据，是否加密，原数据，加密前数据（如果存在），解压时间
    '''
    #提取总校验
    try:
        all_data=base64.b64decode(all_data).decode('utf-8')
    except Exception:
        raise UnsupportError
    sha256_size=64
    if all_data[sha256_size]!='|':
        raise UnsupportError
    all_sha=all_data[0:sha256_size]
    all_data=all_data[sha256_size+1:]
    if SHA256.new(all_data.encode('utf-8')).hexdigest()!=all_sha:
        raise VerificationError
    #提取头
    split_iter=all_data.find('|')
    header_len=all_data[0:split_iter]
    if not header_len.isdigit():
        raise UnsupportError
    header_len=int(header_len)
    header=all_data[split_iter+1:split_iter+1+header_len]
    #提取数据
    if all_data[split_iter+1+header_len:split_iter+1+header_len+2]!='||':
        raise UnsupportError
    fin_data=all_data[split_iter+1+header_len+2:]
    #解析头
    header_list=header.split('|')
    if len(header_list)!=8:
        raise UnsupportError
    ver=header_list[0]
    timestamp=header_list[1]
    res_size=header_list[2]
    fin_size=header_list[3]
    is_enc=header_list[4]
    benc_sha=header_list[5]
    fin_sha=header_list[6]
    res_sha=header_list[7]
    if not (timestamp.isdigit() and res_size.isdigit() and fin_size.isdigit()):
        raise UnsupportError
    if not (is_enc=='0' or is_enc=='1'):
        raise UnsupportError
    if not(len(fin_sha)==sha256_size and len(res_sha)==sha256_size and (benc_sha==None or len(benc_sha)==sha256_size)):
        raise UnsupportError
    timestamp=int(timestamp)
    res_size=int(res_size)
    fin_size=int(fin_size)
    is_enc=bool(is_enc)
    #文件数据验证
    if fin_size!=len(fin_data):
        raise VerificationError
    if SHA256.new(fin_data.encode('utf-8')).hexdigest()!=fin_sha:
        raise VerificationError
    #解密操作
    before_enc_data=None
    if is_enc:
        if benc_sha==None:
            raise UnsupportError
        before_enc_data=AESDecryptStream(fin_data,password).read()
        if SHA256.new(before_enc_data.encode('utf-8')).hexdigest()!=benc_sha:
            raise VerificationError
    #解压操作
    compressed_data=fin_data
    if before_enc_data!=None:
        compressed_data=before_enc_data
    dataobj=fileLikeTranslationMixin()
    dataobj._setFilelikeReading(compressed_data)
    res_data,decompress_time=decompresser(dataobj).get()
    #验证
    if res_size!=len(res_data):
        raise VerificationError
    if SHA256.new(res_data.encode('utf-8')).hexdigest()!=res_sha:
        raise VerificationError
    return fin_data,is_enc,res_data,before_enc_data,decompress_time