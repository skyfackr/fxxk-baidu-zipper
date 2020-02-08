'''
@author:skyfackr
@des:测试字符串是否为float/int/long/complex
'''
def isNum(string:str):
    '''
    测试字符串是否为float/int/long/complex
    '''
    try:
        complex(string)
    except ValueError:
        return False
    return True