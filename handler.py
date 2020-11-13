import json
from random import randint


def webhook(event, context):
    request_message = json.loads(event['body'])
    response = handler_function(request_message)
    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }


exercises = []
state = 0
exercises_description = ''


def handler_function(req_mess):
    global exercises_description
    print(req_mess)
    global state
    global exercises
    print(state)
    buttons = []
    end_session = False
    message = ''
    session = req_mess['session']
    request = req_mess['request']
    list_of_tok = request['nlu']['tokens']
    if session['new'] or state == 0:
        with open('upr.txt') as fin:
            exercises = fin.readlines()
        message = 'Вы на тренажере Маруся, поздравляю, выберите тип тренировок'
        buttons = [button('Разовая тренировка'), button('Комплекс на день')]
        state = 1
    elif state == 1 and (
            'разовую' in list_of_tok or 'единоразовую' in list_of_tok or 'разовая' in list_of_tok or 'единоразовая' in list_of_tok or 'одноразовая' in list_of_tok or 'одноразовую' in list_of_tok or 'розовая' in list_of_tok or 'розовую' in list_of_tok):
        message = 'Отлично, начнем\n'
        state = 2
    elif state == 2 and exercises:
        if (
                "следующее" in list_of_tok or "следующий" in list_of_tok or "следующая" in list_of_tok or "сделал" in list_of_tok or "сделала" in list_of_tok or "сделали" in list_of_tok) or (
                'разовую' in list_of_tok or 'единоразовую' in list_of_tok or 'разовая' in list_of_tok or 'единоразовая' in list_of_tok or 'одноразовая' in list_of_tok or 'одноразовую' in list_of_tok or 'розовая' in list_of_tok or 'розовую' in list_of_tok):
            ind = randint(0, len(exercises) - 1)
            exercise_name, exercises_description = exercises[ind].split(';')
            exercises.pop(ind)
            message += exercise_name
            buttons = [button('Следующее'), button('Как делать')]
            print(state)

        else:
            message = exercises_description
    elif state == 2 and not exercises and not next(list_of_tok):
        message += 'Поздравляю, тренировка сделана'
        end_session = True
    elif stupid(list_of_tok):
        message = exercises_description


    response_message = {
        "response": {
            "text": message,
            "tts": message,
            "buttons": buttons,
            "end_session": end_session
        },
        "session": {derived_key: req_mess['session'][derived_key] for derived_key in
                    ['session_id', 'user_id', 'message_id']},
        "version": req_mess['version']
    }
    print(response_message)
    return response_message


def button(title):
    return {"title": title}

def stupid(word_list):
    if 'как' in word_list and 'делать' in word_list:
        return True
    return False


def next(word_list):
    if "следующее" in word_list or "следующий" in word_list or "следующая" in word_list or "сделал" in word_list or "сделала" in word_list or "сделали" in word_list or "готов" in word_list or "готовы" in word_list or "готовим" in word_list or "готова" in word_list or "готово" in word_list or "всё":
        return True
    return False
