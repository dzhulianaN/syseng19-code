from django.test import TestCase
from django.utils import timezone
from match.models import Cohort,Programme
from match.serializers import CohortSerializer,UserSerializer
import json

class UserSerializerTests(TestCase):

    def setUp(self):
        user_s = UserSerializer(data={
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Smith',
            'password': 'hunter2',
            'profile': {
                'position': 'Consultant',
                'department': 'HR',
                'dateOfBirth': '2000-11-30',
                'joinDate': '2016-01-03',
                'bio': 'I like people, places and things'
            }
        })
        user_s.is_valid()
        self.user = user_s.save()
        self.programme = Programme.objects.create(
            name = 'Test Programme',
            description = 'This is a test programme.',
            defaultCohortSize = 100,
            createdBy = self.user)

    def test_serialize_valid_cohort(self):
        data = {
            'programme': self.programme.programmeId,
            'cohortSize': 200,
            'createdBy':self.user.pk
        }
        serializer = CohortSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        cohort = serializer.save()
        self.assertTrue(cohort.openDate, timezone.now())
