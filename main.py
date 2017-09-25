import itchat, time, re
from itchat.content import *
from utilities import *
from sys import argv, exit
from GlobalTextHook import GlobalTextHook
from HistoryRecorder import HistoryRecorder
from ProcessInterface import ProcessInterface
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level =logging.INFO)

isDebug = not True

itchat.auto_login(True)
plugins = [
   GlobalTextHook({'^/help$': """123"""}),
   HistoryRecorder()
]

for plugin in plugins:
    if not isinstance(plugin, ProcessInterface):
        logging.error('one of the plugins are not a subclass of ProcessInterface.')
        exit(-1)


@itchat.msg_register([PICTURE,RECORDING, ATTACHMENT, VIDEO], isGroupChat= True)
def picture_reply(msg):
    if isDebug:
        logging.info(msg)
    for plugin in plugins:
        try:
            plugin.process(msg,PICTURE)
        except Exception as e:
            logging.error(e)

@itchat.msg_register([SHARING],isGroupChat = True)
def sharing_reply(msg):
    if isDebug:
        logging.info(msg)
    for plugin in plugins:
        try:
            plugin.process(msg,SHARING)
        except Exception as e:
            logging.error(e)

@itchat.msg_register([TEXT],isGroupChat = True)
def text_reply(msg):
    if isDebug:
        logging.info(msg)
    for plugin in plugins:
        try:
            plugin.process(msg,TEXT)
        except Exception as e:
            logging.error(e)

if __name__ == '__main__':
    itchat.run()
