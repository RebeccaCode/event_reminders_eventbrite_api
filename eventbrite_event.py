from datetime import datetime


class EventBriteEvent(object):
    def __init__(self):
        self.__eventbrite_event__ = None

    def __init__(self, eventbrite_event_json):
        self.__eventbrite_event__ = eventbrite_event_json

    def get_start_date(self):
        return datetime.fromisoformat(self.__eventbrite_event__.get('start').get('local'))

    def get_json_event(self):
        return self.__eventbrite_event__

    def get_event_id(self):
        return self.__eventbrite_event__.get('id')

    def set_attendees(self, attendee_json_list):
        self.__eventbrite_event__['attendees'] = attendee_json_list

    def get_attendees_json(self):
        return self.__eventbrite_event__.get('attendees')

    def clear_attendees_json(self):
        del self.__eventbrite_event__['attendees']

    def days_from_now(self):
        n = datetime.now()
        compare = self.get_start_date()
        delta = compare - n
        return delta.days

    def is_future(self):
        return self.days_from_now() > 0

    def is_today(self):
        return self.days_from_now() == 0

    def is_past(self):
        return self.days_from_now() < 0
