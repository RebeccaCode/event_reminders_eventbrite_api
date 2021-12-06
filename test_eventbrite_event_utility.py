import unittest

from eventbrite_event_utility import EventBriteEventUtility


class TestEventBriteEventUtility(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        TestEventBriteEventUtility.event_utility = EventBriteEventUtility()
        TestEventBriteEventUtility.unittest_event_file_path = 'unittest_data/unittest_events.json'

    def test_init(self):
        self.assertIsNotNone(TestEventBriteEventUtility.event_utility)
        self.assertIsNotNone(TestEventBriteEventUtility.event_utility.__eventbrite_private_token__)
        self.assertIsNotNone(TestEventBriteEventUtility.event_utility.__eventbrite_authentication_header__)
        self.assertIsNotNone(TestEventBriteEventUtility.event_utility.__eventbrite_api_url__)
        self.assertIsNotNone(TestEventBriteEventUtility.event_utility.__eventbrite_organization_id__)
        self.assertIsNotNone(TestEventBriteEventUtility.event_utility.__eventbrite_api_url_events__)
        print('done')

    def test_get_future_events(self):
        num_days_forward = 100
        future_events = TestEventBriteEventUtility.event_utility.get_future_events(
            number_days_forward_to_look=num_days_forward)
        self.assertIsNotNone(future_events)
        self.assertGreaterEqual(len(future_events), 0)
        print(len(future_events))
        for event in future_events:
            days = event.days_from_now()
            if days == 0:
                self.assertTrue(event.is_today())
            else:
                self.assertTrue(event.is_future())
                self.assertLessEqual(abs(days), num_days_forward)

        event_file_path = 'unittest_output/future_events.json'
        EventBriteEventUtility.save_event_list_to_file(future_events, event_file_path)

    def test_get_past_events(self):
        num_days_back = 100
        past_events = TestEventBriteEventUtility.event_utility.get_past_events(
            number_of_days_back_to_look=num_days_back)
        self.assertIsNotNone(past_events)
        self.assertGreaterEqual(len(past_events), 0)
        print(len(past_events))
        for event in past_events:
            days = event.days_from_now()
            if days == 0:
                self.assertTrue(event.is_today())
            else:
                self.assertTrue(event.is_past())
                self.assertLessEqual(abs(days), num_days_back)

        event_file_path = 'unittest_output/past_events.json'
        EventBriteEventUtility.save_event_list_to_file(past_events, event_file_path)

    def test_load_events_from_file(self):
        events = EventBriteEventUtility.load_events_from_file(TestEventBriteEventUtility.unittest_event_file_path)
        self.assertIsNotNone(events)
        self.assertGreaterEqual(len(events), 0)
        for event in events:
            self.assertIsNotNone(event.get_event_id())

    def test_replace_event_attendees(self):
        events = EventBriteEventUtility.load_events_from_file(TestEventBriteEventUtility.unittest_event_file_path)
        self.assertIsNotNone(events)
        self.assertGreaterEqual(len(events), 0)

        updated_events = []
        total_attendees = 0
        for event in events:
            event.clear_attendees_json()
            updated_event = TestEventBriteEventUtility.event_utility.replace_event_attendees(event)
            self.assertIsNotNone(updated_event)
            self.assertIsNotNone(updated_event.get_event_id())
            self.assertIsNotNone(updated_event.get_attendees_json())
            updated_events.append(updated_event)
            total_attendees += len(updated_event.get_attendees_json())
        print(total_attendees)

        event_file_path = 'unittest_output/events_with_attendees.json'
        EventBriteEventUtility.save_event_list_to_file(updated_events, event_file_path)