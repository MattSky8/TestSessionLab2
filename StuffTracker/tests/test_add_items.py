from django.test import TestCase, Client
from StuffTracker.models import Stuff, MyUser


# test class for add item criterion 1:
# when a nonempty string is entered,
# the item should be added to the user's list and displayed
class AddItemSimple(TestCase):
    monkey = None
    users = None

    def setUp(self):
        self.monkey = Client()
        self.users = {"user1": ["item1", "item3"], "user2": ["item2"], "user3": []}

        for username in self.users.keys():
            temp_user = MyUser(name=username, password=username)
            temp_user.save()

    def test_item_added(self):
        for user in self.users.keys():
            self.monkey.post("/", {"name": user, "password": user}, follow=True)
            for item in self.users[user]:
                resp = self.monkey.post("/things/", {"name": user, "stuff": item}, follow=True)
                self.assertIn(item, resp.context["things"], "item not added to user's list")

    def test_no_extra_items(self):
        for user in self.users.keys():
            self.monkey.post("/", {"name": user, "password": user}, follow=True)
            for item in self.users[user]:
                resp = self.monkey.post("/things/", {"name": user, "stuff": item}, follow=True)
                for resp_item in resp.context["things"]:
                    self.assertIn(resp_item, self.users[user], "extra item in user's list")

# test class for add item criterion 2:
# when an empty string is entered,
# no item should be added to the user's list or displayed
class AddItemEmptyString(TestCase):
    monkey = None
    users = None

    def setUp(self):
        self.monkey = Client()
        self.users = {"user1": ["item1", "item3"], "user2": ["item2"], "user3": []}

        for username in self.users.keys():
            temp_user = MyUser(name=username, password=username)
            temp_user.save()
            for item in self.users[username]:
                Stuff(name=item, owner=temp_user).save()

    def test_empty_string_not_added(self):
        for user in self.users.keys():
            self.monkey.post("/", {"name": user, "password": user}, follow=True)
            resp = self.monkey.post("/things/", {"name": user, "stuff": ""}, follow=True)
            self.assertNotIn("", resp.context["things"], "empty string item should not be added to user's list")

    def test_correct_size(self):
        for user in self.users.keys():
            self.monkey.post("/", {"name": user, "password": user}, follow=True)
            for item in self.users[user]:
                resp = self.monkey.post("/things/", {"name": user, "stuff": ""}, follow=True)
                for resp_item in resp.context["things"]:
                    self.assertIn(resp_item, self.users[user], "extra item in user's list")

# test class for add item criterion 3:
# when a duplicate item is entered,
# the item should still be added
class AddItemDuplicate(TestCase):
    monkey = None
    users = None

    def setUp(self):
        self.monkey = Client()
        self.users = {"user1": ["item1", "item3"], "user2": ["item2"], "user3": []}

        for username in self.users.keys():
            temp_user = MyUser(name=username, password=username)
            temp_user.save()
            for item in self.users[username]:
                Stuff(name=item, owner=temp_user).save()

    def test_duplicate_added(self):
        for user in self.users.keys():
            self.monkey.post("/", {"name": user, "password": user}, follow=True)
            expected_list_size = len(self.users[user])
            for item in self.users[user]:
                resp = self.monkey.post("/things/", {"name": user, "stuff": item}, follow=True)
                expected_list_size += 1
                self.assertEqual(expected_list_size, len(resp.context["things"]), "duplicate item not added to list")