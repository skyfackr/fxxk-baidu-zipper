'''
@author:skyfackr
@des:测试并输出内存信息（测试阶段使用）
'''
import psutil,logging,json,gc
def log_mem():
    mem_data=psutil.virtual_memory()
    total=str(round(mem_data.total/1024/1024))
    available=str(round(mem_data.available/1024/1024))
    used=str(round(mem_data.used/1024/1024))
    perc=str(round(mem_data.percent))
    free=str(round(mem_data.free/1024/1024))
    logging.info('memory_info:'+json.dumps({
        'total':total+'m',
        'available':available+'m',
        'used':'{}m({}%)'.format(used,perc),
        'free':free+'m'
    }))