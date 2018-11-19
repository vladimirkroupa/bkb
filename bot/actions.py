from datetime import datetime
from flask import make_response
import json
import requests
from cal.bkb_calendar import list_future_loans

# FIXME duplicated, hardwired
BOT_TOKEN = 'xoxb-406015307664-474302986038-Zha6XIdhRqfDScZiClHMVZBP'

fegit_action = {
    'text': 'Přehled výpůjček',
    'attachments': []
}


def handle_list_own_loans(response_url):
    events = list_future_loans('primary', 'goobyson')
    attachments = [format_event(e) for e in events]
    fegit_action['attachments'] = attachments

    resp = requests.post(response_url,
                         data=json.dumps(fegit_action),
                         headers={'Content-type': 'application/json',
                                  'Authorization': 'Bearer ' + BOT_TOKEN})

    return make_response()


def format_event(event):
    start = event['start'].get('dateTime', event['start'].get('date'))
    end = event['end'].get('dateTime', event['start'].get('date'))
    summary = event['summary']
    event_id = event['id']
    description = event.get('description')

    start_datetime = parse_slack_datetime(start)
    end_datetime = parse_slack_datetime(end)

    # FIXME this is wrong
    start_time = start_datetime.strftime('%H:%M')
    end_time = end_datetime.strftime('%H:%M')
    # FIXME wrong again
    loan_date = start_datetime

    time_range = f'{start_time} - {end_time}'

    day_of_week_icon = get_day_of_week_icon_url(loan_date)
    day_of_month_icon = get_day_of_month_icon_url(loan_date)
    loanee_name = 'Gooby'

    date_string = start_datetime.strftime('%A %d.%-m.')

    message = {
        'fallback': 'Ur a fegit Harry',
        'author_name': date_string,
        # "author_link": "http://flickr.com/bobby/",
        "author_icon": 'https://ca.slack-edge.com/T5RD8J51D-U6S2C484S-3e70dc41db77-48',
        "title": time_range,
        # "title_link": "https://api.slack.com/",
        "text": summary,
        "fields": [
            {
                "title": "Kdo",
                # "value": loanee_name,
                "value": 'andrej',
                "short": True
            }
        ],
        'thumb_url': day_of_month_icon,
        'actions': [
            {
                "name": "loan_detail_action",
                "text": "Změnit výpůjčku",
                "type": "button",
                "value": "edit_loan"
            }
        ]
    }
    return message


def get_day_of_month_icon_url(datetime):
    day_of_month = datetime.day
    image_dir_url = 'https://img.icons8.com/ultraviolet/50/000000/'
    return f'{image_dir_url}calendar-{day_of_month}.png'


def get_day_of_week_icon_url(datetime):
    image_dir_url = 'https://img.icons8.com/ultraviolet/50/000000/'
    urls = {
        0: image_dir_url + 'monday.png',
        1: image_dir_url + 'tuesday.png',
        2: image_dir_url + 'wednesday.png',
        3: image_dir_url + 'thursday.png',
        4: image_dir_url + 'friday.png',
        5: image_dir_url + 'saturday.png',
        6: image_dir_url + 'sunday.png'
    }
    day_of_week = datetime.weekday()
    return urls.get(day_of_week)


def parse_slack_datetime(datetime_str):
    fix_tz = datetime_str[::-1].replace(':', '', 1)[::-1]
    return datetime.strptime(fix_tz, '%Y-%m-%dT%H:%M:%S%z')
