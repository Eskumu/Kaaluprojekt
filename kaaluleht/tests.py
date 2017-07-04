from django.contrib.auth.models import User
from django.test import TestCase, Client
from kaaluleht.models import Kaal

class DashboardTestCase(TestCase):

    fixtures = [
        'kaaluleht/fixtures/users.json',
        'kaaluleht/fixtures/initial_data.json'
    ]

    def setUp(self):
        super().setUp()

        username, email, password = 'Tarmo', 'Tarmo@tarmo.tarmo', 'Kaaluleht1'
        User.objects.create_user(username=username, email=email, password=password)

        self.authenticated_client = Client()
        self.authenticated_client.login(username=username, password=password)

    def test_dashboard_requires_authentication(self):

        client = Client()
        response = client.get('/dashboard/')
        self.assertRedirects(response,'/login/?next=/dashboard/')

        response = self.authenticated_client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_blank_redirects(self):

        response = self.authenticated_client.get('')
        self.assertRedirects(response,'/dashboard/', status_code=302, target_status_code=200)

    def test_projects_on_dashboard(self):

        # there are 4 users
        # 2 should be shown (if Weight is None, then there should be no row)

        response = self.authenticated_client.get('/dashboard/')
        kaalud = response.context['kaalud']
        tdNone = "<td>None</td>"
        td80 = "<td>80.0</td>"

        self.assertEqual(len(kaalud), 4)
        self.assertContains(response, tdNone, count=0)
        self.assertContains(response, td80, count=1)

    def test_kaal_uuendus_form(self):

        # tests if form works

        self.authenticated_client.post('/dashboard/',{'kaal':70, 'change_date':'2017-06-29'})
        response = self.authenticated_client.get('/dashboard/')
        kaalud = response.context['kaalud']
        td70 = "<td>70.0</td>"
        success = '<span class="glyphicon glyphicon-thumbs-up" aria-hidden="true"></span>'

        self.assertEqual(len(kaalud), 4)
        self.assertContains(response, td70)
        self.assertContains(response, success)

    def test_kaal_uuendus_form_bad(self):

        # tests if bad form gives error

        post = self.authenticated_client.post('/dashboard/',{'kaal':70.23, 'change_date':'2017-06-29'})
        response = self.authenticated_client.get('/dashboard/')
        kaalud = response.context['kaalud']
        td70 = "<td>70.23</td>"
        warning = '<span class="glyphicon glyphicon-warning-sign" aria-hidden="true"></span>'

        self.assertEqual(len(kaalud), 4)
        self.assertContains(response, td70, 0)
        self.assertContains(response, warning)


class DetailTestCase(TestCase):

    fixtures = [
        'kaaluleht/fixtures/users.json',
        'kaaluleht/fixtures/initial_data.json'
    ]

    def setUp(self):
        super().setUp()

        username, email, password = 'Tarmo', 'Tarmo@tarmo.tarmo', 'Kaaluleht1'
        User.objects.create_user(username=username, email=email, password=password)

        self.authenticated_client = Client()
        self.authenticated_client.login(username=username, password=password)

    def test_get_url_works(self):

        # tests if get_absulute_url works

        kaal = Kaal.objects.get(pk=1)
        response = self.authenticated_client.get(kaal.get_absolute_url())

        self.assertEqual(response.status_code,200)

    def test_detail_requires_authentication(self):

        client = Client()
        kaal = Kaal.objects.get(pk=1)
        response = self.client.get(kaal.get_absolute_url())
        print(kaal.get_absolute_url())
        self.assertRedirects(response,'/login/?next={}'.format(kaal.get_absolute_url()))

        response = self.authenticated_client.get(kaal.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_object_is_right(self):

        kaal = Kaal.objects.get(pk=1)
        response = self.authenticated_client.get(kaal.get_absolute_url())
        andmed = response.context['andmed']
        date = "<td>June 27, 2017</td>"

        self.assertEqual(len(andmed), 8)
        self.assertContains(response, date, 3)