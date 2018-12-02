from django.test import TestCase
from django.contrib.auth.models import User
from apps.accounts.models.Booker import Booker
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory
from apps.util.PrivilegeCategoryManager import PrivilegeCategoryManager


class FakeLDAP:
    data = dict(
        username1=[
            'memberOf: soen490, DC=Concordia',
            'memberOf: soen284, DC=Concordia',
            'memberOf: comp335, DC=Concordia',
            'memberOf: phys202, DC=Concordia',
        ],
        username2=[
            'memberOf: soen490, DC=Concordia',
            'memberOf: soen311, DC=Concordia',
            'memberOf: comp248, DC=Concordia',
            'memberOf: comp390, DC=Concordia',
        ]
    )

    def get_user_groups(self, username):
        return self.data.get(username)


class TestPrivilegeCategoryManager(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='username1', email="user1@gmail", password="abc")
        self.user1.save()
        self.booker1 = Booker(booker_id="1")
        self.booker1.user = self.user1
        self.booker1.save()

        self.user2 = User.objects.create_user(username='username2', email="user2@gmail", password="123")
        self.user2.save()
        self.booker2 = Booker(booker_id="2")
        self.booker2.user = self.user2
        self.booker2.save()

        self.category1 = PrivilegeCategory()
        self.category1.name = "Cat 1"
        self.category1.is_default = True
        self.category1.save()

        self.category2 = PrivilegeCategory()
        self.category2.name = "Cat 2"
        self.category2.related_course = 'soen490'
        self.category2.save()

        self.category3 = PrivilegeCategory()
        self.category3.name = "Cat 3"
        self.category3.related_course = 'comp335'
        self.category3.save()

        self.ldap = FakeLDAP()

    def testAssignPrivilegesSuccess(self):
        manager = PrivilegeCategoryManager()
        manager.assign_booker_privileges(self.booker1, self.ldap)

        privileges1 = self.booker1.privilege_categories.all()
        self.assertEqual(privileges1.count(), 3)
        self.assertEqual(privileges1[0], self.category1)
        self.assertEqual(privileges1[1], self.category2)
        self.assertEqual(privileges1[2], self.category3)

        manager.assign_booker_privileges(self.booker2, self.ldap)

        privileges2 = self.booker2.privilege_categories.all()
        self.assertEqual(privileges2.count(), 2)
        self.assertEqual(privileges2[0], self.category1)
        self.assertEqual(privileges2[1], self.category2)

    def testAssignAllPrivilegesSuccess(self):
        manager = PrivilegeCategoryManager()
        manager.assign_all_booker_privileges(self.ldap)

        privileges1 = self.booker1.privilege_categories.all()
        self.assertEqual(privileges1.count(), 3)
        self.assertEqual(privileges1[0], self.category1)
        self.assertEqual(privileges1[1], self.category2)
        self.assertEqual(privileges1[2], self.category3)

        privileges2 = self.booker2.privilege_categories.all()
        self.assertEqual(privileges2.count(), 2)
        self.assertEqual(privileges2[0], self.category1)
        self.assertEqual(privileges2[1], self.category2)

    def testAssignPrivilegeLDAPUserDoesNotExist(self):
        self.user1.username = "wrong_username"
        self.user1.save()

        manager = PrivilegeCategoryManager()
        manager.assign_booker_privileges(self.booker1, self.ldap)

        privileges1 = self.booker1.privilege_categories.all()
        self.assertEqual(privileges1.count(), 1)
        self.assertEqual(privileges1[0], self.category1)

    def testAssignPrivilegesForAllUsersSuccess(self):
        manager = PrivilegeCategoryManager()
        manager.assign_all_booker_privileges(self.ldap)

        privileges1 = self.booker1.privilege_categories.all()
        print(self.booker1.privilege_categories.all())
        self.assertEqual(privileges1.count(), 3)
        self.assertEqual(privileges1[0], self.category1)
        self.assertEqual(privileges1[1], self.category2)
        self.assertEqual(privileges1[2], self.category3)

        privileges2 = self.booker2.privilege_categories.all()
        self.assertEqual(privileges2.count(), 2)
        self.assertEqual(privileges2[0], self.category1)
        self.assertEqual(privileges2[1], self.category2)
