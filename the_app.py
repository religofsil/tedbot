import flask
import telebot
import config
from bot import bot


WEBHOOK_URL_BASE = "https://{}:{}".format(config.WEBHOOK_HOST, config.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(config.TOKEN)

# удаляем предыдущие вебхуки, если они были
bot.remove_webhook()

# ставим новый вебхук
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)


app = flask.Flask(__name__)

# пустая главная страничка для проверки
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'


# обрабатываем вызовы вебхука
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)