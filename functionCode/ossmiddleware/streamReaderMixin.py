'''
@author:skyfackr
@des:流式读取mixin
'''
class streamReaderMixiner():
    '''
    流式读取mixin
    '''
    def _streamRead(self,data,num=1):
        '''
        流式读取
        '''
        if num==None:
            return data.read()
        ans=''
        while True:
            tmp=data.read(num)
            if not tmp:
                break
            ans+=tmp
        return ans

