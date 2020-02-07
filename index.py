# -*- coding: utf-8 -*-
import logging
from .mainfunc import mainfunc
from .ossmiddleware import ossMiddleware
from .globalEnvironmention import globalEnv

# if you open the initializer feature, please implement the initializer function, as below:
def handler(event, context):
  raise RuntimeError('not finished')
  logger = logging.getLogger()
  logger.info('hello world')
  return 'hello world'

OSSMW=None
def init(context):
  global OSSMW
  OSSMW=ossMiddleware(context.credentials.accessKeyId,context.credentials.accessKeySecret,context.credentials.securityToken)
  globalEnv.setStaticMember('OSSMW',OSSMW)
  logging.info('init success')
