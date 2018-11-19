import json
import requests
from pygments import lexers, formatters, highlight
from flask import Flask, request, make_response, Response
from bot.actions import handle_list_own_loans

app = Flask(__name__)

BOT_TOKEN = 'xoxb-406015307664-474302986038-Zha6XIdhRqfDScZiClHMVZBP'

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
    actions = payload['actions']
    # FIXME: is this possible?
    if len(actions) > 1:
        raise ValueError("Unable to respond to more than 1 action")
    action = actions[0]
    action_name = action['name']
    action_value = action['value']

    # FIXME route now using action name and value
    # FIXME hardwired routing
    return handle_list_own_loans(response_url)


# Start the Flask server
if __name__ == "__main__":
    app.run(port=8080, debug=True)
