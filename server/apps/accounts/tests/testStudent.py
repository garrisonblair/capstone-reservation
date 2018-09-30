from django.test import TestCase

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
