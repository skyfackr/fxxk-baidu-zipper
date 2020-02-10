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
import base64,logging
from .numberTester import isNum
class UnsupportError(Exception):
    pass
class VerificationError(Exception):
    pass

def decoder(all_data:bytes,password):
    '''
    解封装数据

    返回5个数据，依次为原数据，是否加密，原数据，加密前数据（如果存在），解压时间
    '''
    #提取总校验
    try:
        #all_data=base64.b16decode(all_data).decode()
        #pass
        all_data=all_data.decode()
    except Exception:
        raise UnsupportError('1')
    sha256_size=64
    if all_data[sha256_size]!='|':
        raise UnsupportError('2')
    all_sha=all_data[0:sha256_size]
    all_data=all_data[sha256_size+1:]
    if SHA256.new(all_data.encode('utf-8')).hexdigest()!=all_sha:
        raise VerificationError('3')
    #提取头
    split_iter=all_data.find('|')
    header_len=all_data[0:split_iter]
    if not header_len.isdigit():
        raise UnsupportError('4')
    header_len=int(header_len)
    header=all_data[split_iter+1:split_iter+1+header_len]
    #提取数据
    if all_data[split_iter+1+header_len:split_iter+1+header_len+2]!='||':
        raise UnsupportError('5')
    fin_data=all_data[split_iter+1+header_len+2:]
    #解析头
    header_list=header.split('|')
    if len(header_list)!=8:
        raise UnsupportError('6')
    ver=header_list[0]
    timestamp=header_list[1]
    res_size=header_list[2]
    fin_size=header_list[3]
    is_enc=header_list[4]
    benc_sha=header_list[5]
    fin_sha=header_list[6]
    res_sha=header_list[7]
    
    #测试代码
    #logging.info(benc_sha)
    #logging.info(timestamp)
    #logging.info(res_size)
    #logging.info(fin_size)
    #logging.info(len(fin_data))
    #logging.info(header)
    #测试结尾
    if not (isNum(timestamp) and res_size.isdigit() and fin_size.isdigit()):
        raise UnsupportError('7')
    if not (is_enc=='0' or is_enc=='1'):
        raise UnsupportError('8')
    if not(len(fin_sha)==sha256_size and len(res_sha)==sha256_size):
        raise UnsupportError('9-1')
    if not ((benc_sha=='' or len(benc_sha)==sha256_size)):
        raise UnsupportError('9-2')
    timestamp=complex(timestamp)
    res_size=int(res_size)
    fin_size=int(fin_size)
    if is_enc=='1':
        is_enc=True
    else:
        is_enc=False
    #文件数据验证
    if fin_size!=len(fin_data):
        raise VerificationError('10')
    
    if SHA256.new(fin_data.encode()).hexdigest()!=fin_sha:
        raise VerificationError('11')
    try:
        fin_data=base64.b64decode(fin_data.encode())
    except Exception:
        raise UnsupportError('17')
    #解密操作
    before_enc_data=None
    if is_enc:
        if benc_sha==None:
            raise UnsupportError('12')
        try:
            gen=AESDecryptStream(fin_data,password).read()
        except Exception as e:
            #logging.warn('error',exc_info=e)
            raise VerificationError('13-1')
        before_enc_data=gen.__next__()
        if SHA256.new(before_enc_data).hexdigest()!=benc_sha:
            raise VerificationError('13-2')
    #解压操作
    compressed_data=fin_data
    if before_enc_data!=None:
        compressed_data=before_enc_data
    try:
        res_data,decompress_time=decompresser(compressed_data).get()
    except Exception as e:
        raise UnsupportError('16-'+str(e))
    #验证
    if res_size!=len(res_data):
        raise VerificationError('14')
    if SHA256.new(res_data).hexdigest()!=res_sha:
        raise VerificationError('15')
    return fin_data,is_enc,res_data,before_enc_data,decompress_time