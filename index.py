# -*- coding: utf-8 -*-
import logging,json,sys,traceback,os
from functionCode.mainfunc import mainfunc
from functionCode.ossmiddleware import ossMiddleware
from functionCode.globalEnvironmention import globalEnv

# if you open the initializer feature, please implement the initializer function, as below:


def init(context):
  OSSMW=ossMiddleware(context.credentials.accessKeyId,context.credentials.accessKeySecret,context.credentials.securityToken)
  globalEnv.setStaticMember('OSSMW',OSSMW)
  globalEnv.setStaticMember('instanceID',context.requestId)
  logging.info('init success')







def handler(event, context):
  os.chdir('/tmp')
  logging.info('request arrived:'+json.dumps({
    'instanceID':globalEnv.instanceID,
    'requestID':context.requestId,
    'event':json.loads(event)
  }))
  try:
    ans=mainfunc(event,context)
  except Exception as e:
    etype,evalue,emsg=sys.exc_info()
    logging.error('unknown error occured:'+json.dumps({
      'etype':str(etype),
      'evalue':str(e),
      'traceback':str(traceback.format_tb(emsg))
    }))
    return json.dumps({
      'success':False,
      'msg':{
        'errcode':'UnknownError',
        'errmsg':'An unknown error has occured.Please contact us with your uuid below.'
      },
      'uuid':context.requestId
    },sort_keys=True)
  if type(ans)==dict and 'success' in ans.keys() and 'msg' in ans.keys():
    ans['uuid']=context.requestId
  ans=json.dumps(ans,sort_keys=True,ensure_ascii=False)
  logging.info('returned msg:'+ans)
  return ans