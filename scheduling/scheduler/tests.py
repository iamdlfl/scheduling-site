from django.test import TestCase

from .models import Person

# Create your tests here.

class PersonModelTests(TestCase):

    def test_avail_ratio_returns_zero_for_zero_avail(self):

        """ The availability ratio will not return zero if the person has no availability"""
        problem_person = Person(name="Blank", shifts=5)
        self.assertIs(problem_person.calculate_avail_ratio(), 0)