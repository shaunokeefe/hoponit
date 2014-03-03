import mock

from django.test import TestCase

from hoponit.harvest import untappd
from hoponit.harvest import tasks


class UntappdAPITest(TestCase):


    @mock.patch('hoponit.harvest.requests', autospec=True)
    def test_get_checkins_response_ok(self, requests_mock):
        requests_mock.get.return_value = mock_response = mock.Mock()
        mock_response.status_code = 200

        response = untappd.get_checkins()

        self.assertEqual(response.status_code, 200)

    @mock.patch('hoponit.harvest.requests', autospec=True)
    def test_get_checkins_response_bad(self):
        requests_mock.get.return_value = mock_response = mock.Mock()
        mock_response.status_code = 500

        response = untappd.get_checkins()

        self.assertEqual(response.status_code, 500)

    @mock.patch('hoponit.harvest.requests', autospec=True)
    def test_get_checkins_response_rate_limit(self):
        requests_mock.get.return_value = mock_response = mock.Mock()
        mock_response.status_code = 200

        response = untappd.get_checkins()
        self.assertEqual(response.status_code, '???')

    @mock.patch('hoponit.harvest.requests', autospec=True)
    def test_get_checkins_get_checkins(self):
        requests_mock.get.return_value = mock_response = mock.Mock()
        mock_response.status_code = 200

        response = untappd.get_checkins()

        self.assertEqual(response.status_code, 200)

    @mock.patch('hoponit.harvest.requests', autospec=True)
    def test_get_checkins_add_multiple_checkins(self):
        requests_mock.get.return_value = mock_response = mock.Mock()
        mock_response.status_code = 200

        untappd.get_checkins()

    @mock.patch('hoponit.harvest.requests', autospec=True)
    def test_get_venues_response_ok(self):
        requests_mock.get.return_value = mock_response = mock.Mock()
        mock_response.status_code = 200

        untappd.get_checkins()

    @mock.patch('hoponit.harvest.requests', autospec=True)
    def test_get_venuess_response_bad(self):
        requests_mock.get.return_value = mock_response = mock.Mock()
        mock_response.status_code = 200

        untappd.get_venues()


class HarvestTaskTest(TestCase):

    @mock.patch('hoponit.harvest.hammock', autospec=True)
    def test_get_checkins_response_ok(self):
        result = tasks.get_checkins()

    def test_get_checkins_task_response_bad(self):
        result = tasks.get_checkins()

    def test_get_checkins_task_add_venue(self):
        result = tasks.get_checkins()

    def test_get_venue_add_venue(self):
        venue_name = 'test_name'
        result = tasks.get_venue(venue_name)

    def test_get_venue_add_venue_checkins(self):
        venue_name = 'test_name'
        result = tasks.get_venue(venue_name)
