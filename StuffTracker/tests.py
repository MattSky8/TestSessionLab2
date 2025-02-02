from django.test import TestCase, Client
from .models import Stuff, MyUser

# Create your tests here.
"""
Write a system test using Client that makes sure that on a successful login the correct user's item list is displayed. Load the test database with records to support your test.
Write a system test using Client that makes sure on an unsuccessful login, the home page is redisplayed with a message. Load the test database with records to support your test.
Write a system test that shows that an item added to the list immediately shows up in the rendered response. Load the test database with records to support your test.
"""


class LoginList(TestCase):
    monkey = None
    thingList = None

    def setUp(self):
        # completed
        self.monkey = Client()
        self.thingList = {"one": ["cat", "dog"], "two": ["cake"]}

        # fill test database with the things in thingList
        for i in self.thingList.keys():
            temp = MyUser(name=i, password=i)
            temp.save()
            for j in self.thingList[i]:
                Stuff(name=j, owner=temp).save()

    def test_correctName(self):
        for i in self.thingList.keys():
            resp = self.monkey.post("/", {"name": i, "password": i}, follow=True)
            self.assertEqual(resp.context["name"], i, "name not passed from login to list")
            # should check session as well

    def test_complete(self):
        # completed, confirms all the items defined in thingList appear in their owner's page
        for i in self.thingList.keys():
            resp = self.monkey.post("/", {"name": i, "password": i}, follow=True)
            for j in self.thingList[i]:
                self.assertIn(j, resp.context["things"], "list missing an item, user: " + i)

    def test_precise(self):
        # completed, makes ure that there are no extra items in any owner's page
        for i in self.thingList.keys():
            resp = self.monkey.post("/", {"name": i, "password": i}, follow=True)
            for j in resp.context["things"]:
                self.assertIn(j, self.thingList[i], "list contains an extra item, user: " + i)


class LoginFail(TestCase):
    monkey = None
    thingList = None

    def setUp(self):
        # completed
        self.monkey = Client()
        self.thingList = {"one": ["cat", "dog"], "two": ["cake"]}
        # fill test database
        for i in self.thingList.keys():
            temp = MyUser(name=i, password=i)
            temp.save()
            for j in self.thingList[i]:
                Stuff(name=j, owner=temp).save()

    # test methods should confirm correct error message is displayed when a bad password is entered.
    # I had separate tests for no password, someone else's password

    def test_incorrect_password(self):
        randompasswords = ['ahf', 'hello', 'admin', '50d022od']
        for user in self.thingList.keys():
            for password in randompasswords:
                if not user.__eq__(password):
                    resp = self.monkey.post("/", {"name": user, "password": password}, follow=True)
                    self.assertEqual(resp.context["message"], "bad password",
                                     "wrong error message: expected \"bad password\".")

    def test_no_password(self):
        for user in self.thingList.keys():
            resp = self.monkey.post("/", {"name": user, "password": ""}, follow=True)
            self.assertEqual(resp.context["message"], "bad password",
                             "wrong error message: expected \"bad password\".")

    def test_other_password(self):
        for user in self.thingList.keys():
            for password in self.thingList.keys():
                if not user.__eq__(password):
                    resp = self.monkey.post("/", {"name": user, "password": password}, follow=True)
                    self.assertEqual(resp.context["message"], "bad password",
                                     "wrong error message: expected \"bad password\".")


class AddItem(TestCase):
    monkey = None
    thingList = None
    user = None

    def setUp(self):
        # completed
        self.monkey = Client()
        self.thingsToAdd = ["cat", "dog", "cake"]
        # fill test database
        self.user = "one"
        temp = MyUser(name=self.user, password=self.user)
        temp.save()
        self.monkey.post("/", {"name": self.user, "password": self.user}, follow=True)

    # need to create database in setup
    # confirm that after an add item form is submitted, that the new item is in the database and appears in the response webpage

    def test_item_added(self):
        for item in self.thingsToAdd:
            resp = self.monkey.post("/things/", {"name": self.user, "stuff": item}, follow=True)
            self.assertIn(item, resp.context["things"], "item not added to user's list")
