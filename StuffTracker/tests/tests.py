from django.test import TestCase, Client
from StuffTracker.models import Stuff, MyUser

# Create your tests here.
"""
Write a system test using Client that makes sure that on a successful login the correct user's item list is displayed. Load the test database with records to support your test.
Write a system test using Client that makes sure on an unsuccessful login, the home page is redisplayed with a message. Load the test database with records to support your test.
Write a system test that shows that an item added to the list immediately shows up in the rendered response. Load the test database with records to support your test.
"""


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
