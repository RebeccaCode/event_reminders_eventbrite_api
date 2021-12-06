import json
import os
from datetime import datetime

import requests

from eventbrite_event import EventBriteEvent


class EventBriteEventUtility(object):
    def __init__(self):
        self.__eventbrite_private_token__ = os.environ.get('EVENTBRITE_PRIVATE_TOKEN')

        self.__eventbrite_organization_id__ = os.environ.get('EVENTBRITE_ORGANIZATION_ID')

        self.__eventbrite_api_url__ = os.environ.get('EVENTBRITE_API_URL')

        self.__eventbrite_api_url_events__ = '/'.join(
            [self.__eventbrite_api_url__, 'organizations', self.__eventbrite_organization_id__, 'events'])

        self.__eventbrite_api_url_event_attendees__ = '/'.join(
            [self.__eventbrite_api_url__, 'events', '{event_id}', 'attendees'])

        self.__eventbrite_authentication_header__ = {'Authorization': f'Bearer {self.__eventbrite_private_token__}'}

    def get_future_events(self, number_days_forward_to_look=5):
        payload = {'time_filter': 'current_future', 'order_by': 'start_asc'}

        org_events = []
        do_work = True
        r = requests.get(self.__eventbrite_api_url_events__, headers=self.__eventbrite_authentication_header__,
                         params=payload, verify=False)
        while do_work:
            json_response = json.loads(r.text)
            org_events.extend(json_response.get('events'))

            max_start = EventBriteEventUtility.get_max_start(json_response.get('events'))
            delta = max_start - datetime.now()

            if abs(delta.days) >= abs(number_days_forward_to_look):
                do_work = False
            elif json_response.get('pagination').get('has_more_items'):
                r = requests.get(self.__eventbrite_api_url_events__,
                                 headers=self.__eventbrite_authentication_header__,
                                 params={'continuation': json_response.get('pagination').get('continuation')},
                                 verify=False)
            else:
                do_work = False

        result = []
        for event in org_events:
            eb_event = EventBriteEvent(event)
            if abs(eb_event.days_from_now()) <= abs(number_days_forward_to_look):
                result.append(EventBriteEvent(event))

        return result

    def get_past_events(self, number_of_days_back_to_look=5):
        payload = {'time_filter': 'past', 'order_by': 'start_desc'}

        org_events = []
        do_work = True
        r = requests.get(self.__eventbrite_api_url_events__, headers=self.__eventbrite_authentication_header__,
                         params=payload, verify=False)
        while do_work:
            json_response = json.loads(r.text)
            org_events.extend(json_response.get('events'))

            min_start = EventBriteEventUtility.get_min_start(json_response.get('events'))
            delta = min_start - datetime.now()

            if abs(delta.days) >= abs(number_of_days_back_to_look):
                do_work = False
            elif json_response.get('pagination').get('has_more_items'):
                r = requests.get(self.__eventbrite_api_url_events__,
                                 headers=self.__eventbrite_authentication_header__,
                                 params={'continuation': json_response.get('pagination').get('continuation')},
                                 verify=False)
            else:
                do_work = False

        result = []
        for event in org_events:
            eb_event = EventBriteEvent(event)
            if abs(eb_event.days_from_now()) <= abs(number_of_days_back_to_look):
                result.append(eb_event)

        return result

    def replace_event_attendees(self, eventbrite_event):
        event_id = eventbrite_event.get_event_id()
        url = self.__eventbrite_api_url_event_attendees__.format(event_id=event_id)
        r = requests.get(url,
                         headers=self.__eventbrite_authentication_header__, verify=False)

        eventbrite_event.set_attendees(json.loads(r.text).get('attendees'))
        return eventbrite_event

    @staticmethod
    def get_max_start(eventbrite_event_json_list):
        max_start = None
        for event in eventbrite_event_json_list:
            compare = datetime.fromisoformat(event.get('start').get('local'))
            if max_start is None or max_start < compare:
                max_start = compare
            else:
                continue
        return max_start

    @staticmethod
    def get_min_start(eventbrite_event_json_list):
        min_start = None
        for event in eventbrite_event_json_list:
            compare = datetime.fromisoformat(event.get('start').get('local'))
            if min_start is None or min_start > compare:
                min_start = compare
            else:
                continue
        return min_start

    @staticmethod
    def save_event_list_to_file(eventbrite_event_list, file_path):
        json_list = []
        for event in eventbrite_event_list:
            json_list.append(event.get_json_event())

        with open(file_path, 'w') as f:
            json.dump(json_list, f)

    @staticmethod
    def load_events_from_file(file_path):
        with open(file_path, 'r') as f:
            json_list = json.load(f)

        result = []
        for item in json_list:
            result.append(EventBriteEvent(item))

        return result
