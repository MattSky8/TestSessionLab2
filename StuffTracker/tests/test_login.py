from django.test import TestCase, Client
from StuffTracker.models import Stuff, MyUser


# test class for login criterion 1:
# given a valid matching username and password are entered,
# the user should be logged in
# and shown only and all items from their list
class SuccessfulLogin(TestCase):
    monkey = None
    users = None

    # setup method
    def setUp(self):
        self.monkey = Client()
        self.users = {"user1": ["item1", "item3"], "user2": ["item2"], "user3": []}

        for username in self.users.keys():
            temp_user = MyUser(name=username, password=username)
            temp_user.save()
            for item in self.users[username]:
                Stuff(name=item, owner=temp_user).save()

    # tests
    def test_correct_name(self):
        for user in self.users.keys():
            resp = self.monkey.post("/", {"name": user, "password": user}, follow=True)
            self.assertEqual(resp.context["name"], user, "name not passed from login to list")
            # should check session as well

    def test_complete(self):
        for user in self.users.keys():
            resp = self.monkey.post("/", {"name": user, "password": user}, follow=True)
            for item in self.users[user]:
                self.assertIn(item, resp.context["things"], "list missing an item, user: " + user)

    def test_precise(self):
        for user in self.users.keys():
            resp = self.monkey.post("/", {"name": user, "password": user}, follow=True)
            for item in resp.context["things"]:
                self.assertIn(item, self.users[user], "list contains an extra item, user: " + user)


# test class for login criterion 2:
# given the user has entered a valid username
# but not the matching password,
# then they should not be logged in
# and an error message should be displayed.
class FailedLogin(TestCase):
    monkey = None
    users = None

    # setup method
    def setUp(self):
        self.monkey = Client()
        self.users = {"user1": ["item1", "item3"], "user2": ["item2"], "user3": []}

        for username in self.users.keys():
            temp_user = MyUser(name=username, password=username)
            temp_user.save()
            for item in self.users[username]:
                Stuff(name=item, owner=temp_user).save()

    def test_incorrect_password(self):
        randompasswords = ['ahf', 'hello', 'admin', '50d022od']
        for user in self.users.keys():
            for password in randompasswords:
                if not user.__eq__(password):
                    resp = self.monkey.post("/", {"name": user, "password": password}, follow=True)
                    self.assertEqual(resp.context["message"], "bad password",
                                     "wrong error message: expected \"bad password\".")

    def test_no_password(self):
        for user in self.users.keys():
            resp = self.monkey.post("/", {"name": user, "password": ""}, follow=True)
            self.assertEqual(resp.context["message"], "bad password",
                             "wrong error message: expected \"bad password\".")

    def test_other_password(self):
        for user in self.users.keys():
            for password in self.users.keys():
                if not user.__eq__(password):
                    resp = self.monkey.post("/", {"name": user, "password": password}, follow=True)
                    self.assertEqual(resp.context["message"], "bad password",
                                     "wrong error message: expected \"bad password\".")