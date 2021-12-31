from django.test import TestCase
from rest_framework.test import APIClient
from directory.models import User, Company
from django.urls import reverse

"""
To make a test API call over an authenticated API endpoint, follow
this pattern:


```
from django.urls import reverse
from rest_framework.test import APIClient

client = APIClient()
user = ...
client.force_authenticate(user=self.user)
response = client.get(reverse('{REVERSED_URL}'))
```

Use mysite/fill_db_flowchart.png to understand the hierarchy

"""
api_client = APIClient()


class UsersViewSetAPICase(TestCase):

    def setUp(self):
        self.wayne_co = Company.objects.create(name="Wayne Enterprises")

        self.batman = User.objects.create_user(username="Batman",
                                               first_name="Bruce", last_name="Wayne", company=self.wayne_co)

        self.robin = User.objects.create_user(username="Robin",
                                              first_name="Jason", last_name="Todd", company=self.wayne_co, reports_to=self.batman)

        self.nightwing = User.objects.create_user(username="Nightwing",
                                                  first_name="Dick", last_name="Grayson", company=self.wayne_co, reports_to=self.batman)

        self.stark_co = Company.objects.create(name="Stark Enterprises")

        self.ironman = User.objects.create_user(username="Ironman",
                                                first_name="Tony", last_name="Stark", company=self.stark_co)

        self.falcon = User.objects.create_user(username="Falcon",
                                               first_name="Sam", last_name="Wilson", company=self.stark_co, reports_to=self.ironman)

        self.happy = User.objects.create_user(username="Happy",
                                              first_name="Harold", last_name="Hogan", company=self.stark_co, reports_to=self.ironman)

        self.spiderman = User.objects.create_user(username="Spiderman",
                                                  first_name="Peter", last_name="Parker", company=self.stark_co, reports_to=self.happy)

    def test_should_not_allow_unathenticated_requests(self):

        non_auth_client = APIClient()

        response = non_auth_client.get(reverse("users-list"))

        assert response.status_code == 401

    def test_should_show_users_same_company(self):

        user: User = self.spiderman

        api_client.force_authenticate(user=user)

        response = api_client.get(reverse("users-list"))

        employees = response.data

        for employee in employees:
            print(employee)
            comp = Company.objects.filter(id=employee["company"]).first()
            assert comp == user.company

        user: User = self.batman

        api_client.force_authenticate(user=user)

        response = api_client.get(reverse("users-list"))

        employees = response.data

        for employee in employees:
            comp = Company.objects.filter(id=employee["company"]).first()
            assert comp == user.company

    def test_should_show_everyone_below(self):

        user: User = self.ironman
        api_client.force_authenticate(user=user)
        url = reverse("users-reports", kwargs={"pk": user.pk})

        response = api_client.get(url)

        employees = response.data

        assert len(employees) == 3

        for employee in employees:
            assert employee["first_name"] in ("Peter", "Harold", "Sam")

    def test_should_show_everyone_above(self):
        user: User = self.spiderman
        api_client.force_authenticate(user=user)
        url = reverse("users-managers", kwargs={"pk": user.pk})

        response = api_client.get(url)

        employees = response.data

        assert len(employees) == 2

        for employee in employees:
            assert employee["first_name"] in ("Tony", "Harold")

    def test_should_show_users_with_manager(self):
        user: User = self.spiderman
        api_client.force_authenticate(user=user)
        url = reverse("users-list") + "?has_manager=true"

        response = api_client.get(url)

        employees = response.data

        assert len(employees) == 3

        # only Tony has no managers
        for employee in employees:
            assert employee["first_name"] != "Tony"

    def test_should_show_users_with_no_manager(self):
        user: User = self.ironman
        api_client.force_authenticate(user=user)
        url = reverse("users-list") + "?has_manager=false"

        response = api_client.get(url)

        employees = response.data

        assert len(employees) == 1

        assert employees[0]["first_name"] == "Tony"

    def test_should_show_users_who_are_manager(self):
        user: User = self.ironman
        api_client.force_authenticate(user=user)
        url = reverse("users-list") + "?is_manager=true"

        response = api_client.get(url)

        employees = response.data
        assert len(employees) == 2
        # The people have reportees
        for employee in employees:
            assert employee["first_name"] in ("Tony", "Harold")

    def test_should_show_users_who_are_not_manager(self):
        user: User = self.ironman
        api_client.force_authenticate(user=user)
        url = reverse("users-list") + "?is_manager=false"

        response = api_client.get(url)

        employees = response.data

        assert len(employees) == 2
        # nobody reports to them
        for employee in employees:
            assert employee["first_name"] in ("Sam", "Peter")
