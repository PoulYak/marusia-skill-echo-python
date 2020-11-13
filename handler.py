import json


def webhook(event, context):
    request_message = json.loads(event['body'])
    return {
        "statusCode": 200,
        "body": json.dumps(handler_function(request_message))
    }


state = 0


def handler_function(req_mess):
    global state
    buttons = []
    end_session = False
    message = ''
    session = req_mess['session']
    request = req_mess['request']
    print(request)

    if session['new'] or state == 0:

        message = 'Вы на тренажере Маруся, поздравляю, выберите тип тренировок'
        buttons = [button('Разовая тренировка'), button('Комплекс на день')]
        state = 1

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
