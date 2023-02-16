from alice_scripts import Skill, request, say, suggest
# import telebot
import config
import logging
import requests

# bot = telebot.TeleBot(config.TOKEN_TEST)
skill = Skill(__name__)
logging.basicConfig(level=logging.DEBUG)

@skill.script
def run_script():
    print(' - start! - ')
    yield say('Привет?')
    question = request.command
    print('\n -- request: ', request, '\n')
    print('\n -- request command: ', request.command, '\n')

    while True:
        # найди 1251
        if request.command == 'найди' or request.command == 'найти' or request.command == 'найди мне':
            print(' - COMMAND: ', request.command.split())

            # открываем файл
            with open(config.file_neighbors_txt_home, 'r', encoding='utf-8') as file:
                data = file.readlines()
                # data = data.split()
                for line in data:
                    all_data_in_line = line.split()
                    if '0250' in str(all_data_in_line[0:3]):
                        print()
                        result = all_data_in_line[0] + ' ' + all_data_in_line[1] + ' ' + all_data_in_line[2]
                        req = requests.post(f'https://api.telegram.org/bot{config.tg_token}/sendMessage?chat_id={config.alerusford_user_id_tg}&text={result}')
                        print()
                    else:
                        pass



            # если переменная есть то
            yield say('найдено, что хотите сделать? пинг? закрыть?')
            if request.command == 'пинг' or request.command == 'пинк' or request.command == 'pink' or request.command == 'ping':
                user_id_alice = request['session']['user']['user_id']
                print('user_id_alice: ', user_id_alice)
                print(' !!! условие пинг !!! ')
                req = requests.post(f'https://api.telegram.org/bot{config.tg_token}/sendMessage?chat_id={config.alerusford_user_id_tg}&text=тестируем post запрос!')
                # print(req.status_code)
                yield say('выполнилось условие пинг. закрыть?')
                result = 'ping'

            elif request.command == 'закрыть':
                print(' !!! условие закрыть !!! ')
                result = 'аривидерчи'
                yield say('аривидерчи', end_session=True)

            else:
                yield say('иначе')
                print(' - иначе - ')
                # run_script()

            # while not request.has_lemmas('пинг', 'о системе', 'об оборудовании', 'закрыть'):
            #     yield say('что надо сделать? пингануть? о системе? об оборудовании? закрыть?')
        else:
            print(' - условие иначе. нет условия - ')
            yield say('условие иначе. нет условия')
            # run_script()
        yield say(f'ок, {result} - выполнено и закрыто. Слушаю Вас.')