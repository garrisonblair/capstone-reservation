from django.test import TestCase

from apps.accounts.models.Booker import Booker


class TestBooker(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testStudentCreation(self):
        booker_id = '12345678'

        student = Booker(booker_id=booker_id)
        student.user = None
        student.save()

        read_student = Booker.objects.get(booker_id=booker_id)

        self.assertEqual(read_student, student)

    def testStudentToString(self):
        booker_id = '12345678'

        student = Booker(booker_id=booker_id)

        student_string = student.__str__()

        self.assertEqual(student_string, booker_id)
