from django.test import TestCase, Client
from StuffTracker.models import Stuff, MyUser


# test class for create account criterion 1:
# when an unused username and a password are entered
# then that account should be created, the user should be logged in,
# they should be redirected to the item page, and their list should be empty.
class SuccessfulCreateAccount(TestCase):
    monkey = None
    users = None

    # setup method
    def setUp(self):
        self.monkey = Client()
        self.users = {"user1": "password1", "user2": "password2", "user3": "password3"}

    # tests
    def test_logged_in(self):
        for username in self.users.keys():
            resp = self.monkey.post("/", {"name": username, "password": self.users[username]}, follow=True)
            self.assertEqual(resp.context["name"], username,
                             "created account " + username + " but logged in under " + resp.context["name"])

    def test_empty_item_list(self):
        for user in self.users.keys():
            resp = self.monkey.post("/", {"name": user, "password": user}, follow=True)
            self.assertEqual(len(resp.context["things"]), 0, "list should be empty but contains an item, user: " + user)


# test class for create account criterion 2:
# when an in-use username and nonmatching password is entered,
# then the user should not be logged in and no changes should be made to the account.
class FailedCreateAccount(TestCase):
    monkey = None
    users = None
    bad_passwords = None

    # setup method
    def setUp(self):
        self.monkey = Client()
        self.users = {"user1": ["item1", "item3"], "user2": ["item2"], "user3": []}
        self.bad_passwords = ["df", "", "adpe23^m", "user-1", "42"]

        for username in self.users.keys():
            temp_user = MyUser(name=username, password=username)
            temp_user.save()
            for item in self.users[username]:
                Stuff(name=item, owner=temp_user).save()

    def test_create_account_failed(self):
        for user in self.users.keys():
            for password in self.bad_passwords:
                if not user.__eq__(password):
                    resp = self.monkey.post("/", {"name": user, "password": password}, follow=True)
                    self.assertEqual(resp.context["message"], "bad password",
                                     "wrong error message: expected \"bad password\".")

    def test_password_unchanged(self):
        for user in self.users.keys():
            for password in self.bad_passwords:
                if not user.__eq__(password):
                    self.monkey.post("/", {"name": user, "password": password}, follow=True)
            resp = self.monkey.post("/", {"name": user, "password": user}, follow=True)
            self.assertEqual(resp.context["name"], user,
                             "failed account creation changed password of existing account")

    def test_item_list_unchanged(self):
        for user in self.users.keys():
            for password in self.bad_passwords:
                if not user.__eq__(password):
                    self.monkey.post("/", {"name": user, "password": password}, follow=True)
            resp = self.monkey.post("/", {"name": user, "password": user}, follow=True)
            self.assertListEqual(resp.context["things"], self.users[user],
                                 "failed account creation changed existing account's list; user: " + user)

