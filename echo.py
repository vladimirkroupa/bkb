import json
import requests
from pygments import lexers, formatters, highlight
from flask import Flask, request, make_response, Response

app = Flask(__name__)

BOT_TOKEN = 'xoxb-406015307664-474302986038-Zha6XIdhRqfDScZiClHMVZBP'

fegit_action = '''
{
    "text": "Would you like to play a game?",
    "attachments": [
        {
            "text": "Choose a game to play",
            "fallback": "You are unable to choose a game",
            "callback_id": "wopr_game",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "game",
                    "text": "Chess",
                    "type": "button",
                    "value": "chess"
                },
                {
                    "name": "game",
                    "text": "Falken's Maze",
                    "type": "button",
                    "value": "maze"
                },
                {
                    "name": "game",
                    "text": "Thermonuclear War",
                    "style": "danger",
                    "type": "button",
                    "value": "war",
                    "confirm": {
                        "title": "Are you sure?",
                        "text": "Wouldn't you prefer a good game of chess?",
                        "ok_text": "Yes",
                        "dismiss_text": "No"
                    }
                }
            ]
        }
    ]
}'''

select_action = {
    'text': 'Wat do u want?',
    'channel': 'CBZNKNVJB',
    'attachments': [
        {
            'text': 'Choose',
            'callback_id': 'cargo_action_select',
            'actions': [
                {
                    'name': 'cargo_action',
                    'text': 'Nová výpůjčka',
                    'type': 'button',
                    'value': 'create_loan',
                    'style': 'primary',
                },
                {
                    'name': 'cargo_action',
                    'text': 'Přehled mých výpůjček',
                    'type': 'button',
                    'value': 'list_my_loans'
                }
            ]
        }
    ]
}


def pretty_print(a_json):
    formatted_json = json.dumps(a_json, indent=2)
    colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
    print(colorful_json)


@app.route("/event", methods=["POST"])
def handle_event():
    print('handling /event')
    payload = request.get_json()
    pretty_print(payload)

    if 'challenge' in payload:
        challenge = payload['challenge']
        return Response(challenge, mimetype='text/plain')
    elif 'event' in payload:
        event = payload['event']
        type = event['type']
        subtype = event.get('subtype')
        print(subtype)
        if type == 'message' and subtype not in {'bot_message', 'message_changed'}:
            text = event['text']
            print(f'received message: {text}')
            resp = requests.post('https://slack.com/api/chat.postMessage',
                                 data=json.dumps(select_action),
                                 headers={'Content-type': 'application/json',
                                          'Authorization': 'Bearer ' + BOT_TOKEN})
            # print(resp.text)

    return make_response()


@app.route("/interaction", methods=["POST"])
def handle_interaction():
    print('handling /interaction')
    # print(request.mimetype)
    # print(request.form)
    payload = json.loads(request.form.get('payload'))
    del payload['original_message']
    pretty_print(payload)

    response_url = payload['response_url']

    resp = requests.post(response_url,
                         data=fegit_action,
                         headers={'Content-type': 'application/json',
                                  'Authorization': 'Bearer ' + BOT_TOKEN})

    return make_response()


# Start the Flask server


if __name__ == "__main__":
    app.run(port=8080, debug=True)
