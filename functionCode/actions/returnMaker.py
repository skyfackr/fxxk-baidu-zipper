'''
@author:skyfackr
@des:返回信息快速构造函数
'''
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
