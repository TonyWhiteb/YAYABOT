from time import time
from datetime import datetime
from ProcessInterface import ProcessInterface
from utilities import *
from itchat.content import *
import os

class HistoryRecorder(ProcessInterface):
    def __init__(self):
        self.client = client
        self.coll = self.client[dbName][collName]
        self.imgFolder = 'Images'
        if not os.path.exists(self.imgFolder):
            os.mkdir(self.imgFolder)
        logging.info('HistoryRecorder Initialized.')


    def process(self,msg,type):
        if type == PICTURE:
            fn = msg('FileName')
            newfn = os.path.join(self.imgFolder,fn)
            msg['Text'](fn)
            os.rename(fn,newfn)
            msg['Content'] = '<<<IMG:{}>>>'.format(newfn)
        if  type == TEXT or type == PICTURE:
            timestamp = time()
            rtime = datetime.utcfromtimestamp(timestamp)
            r = {
                'content': msg['Content'],
                'from': msg['ActualNickName'],
                'fromId': msg['ToUserName'],
                'to': msg['User']['NickName'] if 'User' in msg and 'UserName' in msg['User'] else 'N/A',
                'timestamp': timestamp,
                'time': rtime

            }
        self.coll.insert(r)    
