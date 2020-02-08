'''
@author:skyfackr
@des:应用分发器
'''
from .actions import compress,decompress
import json,demjson,logging
from .globalEnvironmention import globalEnv
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


def switch(event:dict):
    '''
    分发器
    '''
    #模式选择入口
    actions_lambda={
    'compress':lambda download_path,upload_path,password:compress(download_path,upload_path,password=password),
    'decompress':lambda download_path,upload_path,password:decompress(download_path,upload_path,password=password)
    }
    #参数测试
    needed=['mode','resource_file_path','save_file_path']
    for need in needed:
        if not need in event.keys():
            return __failedReturnMaker('ParameterError','lose any param')
    if not 'password' in event.keys():
        event['password']=None
    #应用测试
    #logging.warn(str(globalEnv.support_mode))
    allowed_modes=demjson.decode(str(globalEnv.support_mode))
    if (not event['mode'] in actions_lambda.keys()) or (not event['mode'] in allowed_modes):
        return __failedReturnMaker('ParameterError','invaild mode')
    return actions_lambda[event['mode']](event['resource_file_path'],event['save_file_path'],event['password'])