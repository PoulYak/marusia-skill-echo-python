import json


def webhook(event, context):
    request_message = json.loads(event['body'])
    response = handler_function(request_message)
    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }


state = 0


def handler_function(req_mess):
    print(req_mess)
    global state
    buttons = []
    end_session = False
    message = ''
    session = req_mess['session']
    request = req_mess['request']
    list_of_tok = request['command']
    if session['new'] or state == 0:

        message = 'Вы на тренажере Маруся, поздравляю, выберите тип тренировок'
        buttons = [button('Разовая тренировка'), button('Комплекс на день')]
        state = 1
    print("/////////////////////////////////////////////////////////////////////",list_of_tok)
    if 'разовую' in list_of_tok or 'единоразовую' in list_of_tok or 'разовая' in list_of_tok or 'единоразовая' in list_of_tok or 'одноразовая' in list_of_tok or 'одноразовую' in list_of_tok or 'розовая' in list_of_tok or 'розовую' in list_of_tok:
        message = 'Отлично, начнем'
        state = 2


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


def check_user(user_id):
    with open('users_id.txt') as fin:
        users_id = list(fin.readlines())

    if user_id in users_id: return True
    else:
        with open('users_id.txt', 'a') as fout:
            print(user_id, file = fout)
        return False


