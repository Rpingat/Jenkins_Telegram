import logging
import os
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler, ConversationHandler
import jenkins
from settings import *

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

token = BOT_TOKEN
bot = telegram.Bot(token=token)
print(bot.get_me())
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
server = jenkins.Jenkins(JENKINS_URL, username=JENKINS_USER, password=JENKINS_PASS)

def build(update, context):
    inp = update.message.text
    jenkins_job_name ="test"
    pms = inp.split(' ')

    if len(pms)%2 == 0:
        return
    params={}
    for i in range(1, len(pms), 2):
        params[pms[i]] = pms[i+1]
    print(params)
    k = server.build_job_url(jenkins_job_name, params, token=None).strip("https://")
    command = 'curl -X POST "https://{}:{}@{}"'.format(JENKINS_USER, JENKINS_TOKEN, k)
    os.system(command)

build_handler = CommandHandler('build', build)
dispatcher.add_handler(build_handler)

def main():
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
