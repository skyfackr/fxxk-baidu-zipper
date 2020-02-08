'''
@author:skyfackr
@des:主函数
'''
from .actionSwitcher import switch
import json
def mainfunc(event,context):
    '''
    主函数
    '''
    return switch(json.loads(event))