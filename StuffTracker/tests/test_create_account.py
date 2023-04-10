from django.test import TestCase, Client
from StuffTracker.models import Stuff, MyUser

# test class for create account criterion 1:
# when an unused username and a password are entered
# then that account should be created, the user should be logged in,
# they should be redirected to the item page, and their list should be empty.


# test class for create account criterion 2:
# when an in-use username and nonmatching password is entered,
# then the user should not be logged in and no changes should be made to the account.


