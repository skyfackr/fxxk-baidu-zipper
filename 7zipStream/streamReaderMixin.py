'''
@author:skyfackr
@des:流式读取mixin
'''
class streamReaderMixiner():
    '''
    流式读取mixin
    '''
    def _streamRead(self,data):
        '''
        流式读取
        '''
        ans=''
        while True:
            tmp=data.read(1)
            if not tmp:
                break
            ans+=tmp
        return ans

