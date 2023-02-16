# ngrok http https://localhost:5000
# export FLASK_APP=alisa.py && python3 -m flask run --host=0.0.0.0 --cert=adhoc
import dialogic.server.flask_server
import requests
import config
from telebot import util
from dialogic.dialog_connector import DialogConnector
from dialogic.dialog_manager import TurnDialogManager
from dialogic.server.flask_server import FlaskServer
from dialogic.cascade import DialogTurn, Cascade
from os.path import getctime
from datetime import datetime as dt

csc = Cascade()

user_name = ''
def user_id_tg_generate(user_id_alice):
    # user_id_alice = ''

    print('\n', dialogic.server.flask_server.request.json, '\n')

    if user_id_alice == config.user_id_ya:
        user_name = 'Александр'
        user_id_tg = config.user_id_tg
        print(' - авторизация успешна: ', user_name, user_id_tg)
        return user_name + ' ' + user_id_tg
    else:
        print('\n - ERROR NAME -\n  - user_id: ', user_id_alice, '\n')
        user_name = 'error auth'
        user_id_tg = config.user_id_tg
        requests.post(f'https://api.telegram.org/bot{config.tg_token}/sendMessage?chat_id={user_id_tg}&text={user_name}\n{user_id_alice}')


@csc.add_handler(priority=1)
def fallback(turn: DialogTurn):
    # pass
    turn.response_text = 'Привет!'

@csc.add_handler(priority=2)
def fallback(turn: DialogTurn):
    user_id_alice = dialogic.server.flask_server.request.json['session']['user']['user_id']
    user_id = user_id_tg_generate(user_id_alice).split()
    user_name = user_id[0]
    user_id_tg = user_id[1]
    turn.response_text = f'Привет, {user_name}!'

@csc.add_handler(priority=10, regexp='(hello|hi|привет|здравствуй)')
def hello(turn: DialogTurn):
    user_id_alice = dialogic.server.flask_server.request.json['session']['user']['user_id']
    user_id = user_id_tg_generate(user_id_alice).split()
    user_name = user_id[0]
    user_id_tg = user_id[1]
    turn.response_text = f'Здравствуй, {user_name}'
    print(' - ответ на привет! -')

@csc.add_handler(priority=10, regexp='(найди|найди мне|найти|искать|ищи)')
def find(turn: DialogTurn):
    user_id_alice = dialogic.server.flask_server.request.json['session']['user']['user_id']
    user_id = user_id_tg_generate(user_id_alice).split()
    user_name = user_id[0]
    user_id_tg = user_id[1]
    input = turn.text.split()
    print(' - COMMAND: ', input)
    if input[1] == 'мне':
        search_word = ''.join(input[2:])
        pass
    elif len(input[1]) <= 2:
        search_word = ''.join(input[1:])
    else:
        search_word = ''.join(input[1:])
    print(' - search_word: ', search_word)

    def search_in_192():
        with open(config.file_neighbors_txt_home, 'r', encoding='utf-8') as file:
            data = file.readlines()
            # data = data.split()
            for line in data:
                all_data_in_line = line.split()
                if str(search_word) in str(all_data_in_line[0:3]):
                    print()
                    print(' - найдено: ', all_data_in_line[0:3])
                    result = all_data_in_line[0] + ' ' + all_data_in_line[1] + ' ' + all_data_in_line[2]
                    requests.post(f'https://api.telegram.org/bot{config.tg_token}/sendMessage?chat_id={user_id_tg}&text={result}')
                    print()
                    return result
                else:
                    pass
    result_search = search_in_192()
    print(' - result_search:', result_search)
    if result_search == None:
        print('ничего не найдено')
        turn.response_text = f'{search_word} не найдено'
    else:
        result_tg = result_search.split()
        print(result_tg)
        print(f'{result_tg[1]} найдено. отправлено.')
        turn.response_text = f'{result_tg[1]} найдено, отправлено.'

@csc.add_handler(priority=10, regexp='(все онлайн|покажи всех|показать всех)')
def find(turn: DialogTurn):
    user_id_alice = dialogic.server.flask_server.request.json['session']['user']['user_id']
    user_id = user_id_tg_generate(user_id_alice).split()
    user_name = user_id[0]
    user_id_tg = user_id[1]
    input = turn.text.split()
    print(' - COMMAND: ', input)
    date_modif_file = f"обновлено: {dt.fromtimestamp(getctime(config.file_neighbors_txt_home)).strftime('%H:%M %d-%m-%Y')}"
    with open(config.file_neighbors_txt_home, 'r', encoding='utf-8') as file:
        data = file.readlines()
        # data = data.split()
        all_data = []
        for line in data:
            all_data_in_line = line.split()[0:3]
            all_data.append(all_data_in_line[0] + ' ' + all_data_in_line[1] + ' ' + all_data_in_line[2] + '\n')
        # print(*all_data)
        print(type(all_data))
        print(len(all_data))
        all_data_str = ''.join(all_data)
        # print(all_data_str)

        splitted_text = util.split_string(all_data_str, 3000)
        for text in splitted_text:
            print()
            print(text)
            print()
            requests.post(f'https://api.telegram.org/bot{config.tg_token}/sendMessage?chat_id={user_id_tg}&text={text}')
        requests.post(f'https://api.telegram.org/bot{config.tg_token}/sendMessage?chat_id={user_id_tg}&text={date_modif_file}\nкол-во: {len(all_data)}')

        turn.response_text = 'выполнено'
        turn.suggests.append('все онлайн')

    # kolichestvo = large_text.splitlines()
    # bot.send_message(message.chat.id, f'{date_modif_file}\nкол-во : {len(kolichestvo)}')



dm = TurnDialogManager(cascade=csc)
connector = DialogConnector(dialog_manager=dm)
server = FlaskServer(connector=connector)

if __name__ == '__main__':
    server.parse_args_and_run()