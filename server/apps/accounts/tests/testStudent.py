from django.test import TestCase
from django.contrib.auth.models import User

from apps.accounts.models.Student import Student


class TestStudent(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testStudentCreation(self):
        student_id = '12345678'

        student = Student(student_id=student_id)
        student.user = None
        student.save()

        read_student = Student.objects.get(student_id=student_id)

        self.assertEqual(read_student, student)

    def testStudentCreatedWithUser(self):
        new_user = User.objects.create_user('JohnDoe', 'JohnDoe@gmail.com', 'VerySafePassword')

        student = Student.objects.get(user=new_user)

        self.assertEqual(student.user, new_user)
        self.assertEqual(new_user.student, student)
