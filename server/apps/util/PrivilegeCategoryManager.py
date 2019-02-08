from apps.util import ldap_server
from apps.accounts.models.PrivilegeCategory import PrivilegeCategory
from apps.accounts.models.User import User
import pdb


class PrivilegeCategoryManager:

    def clear_booker_privileges(self, booker):
        booker.bookerprofile.privilege_categories.clear()
        booker.save()

    def clear_all_booker_privileges(self):
        bookers = User.objects.all()
        for booker in bookers:
            self.clear_booker_privileges(booker)

    def assign_booker_privileges(self, booker, server=ldap_server):
        privilege_categories = PrivilegeCategory.objects.all()
        courses = server.get_user_groups(username=booker.username)

        # clear booker privileges before re-assigning them
        self.clear_booker_privileges(booker)

        # adding default privilege category that all users should be part of
        default_category = privilege_categories.get(is_default=True)
        if default_category:
            booker.bookerprofile.privilege_categories.add(default_category)

        # if user is not found in the LDAP he will only have default privileges
        if courses is None:
            return

        # for each existing privilege category
        # if there is no related course assigned to it, skip it
        # if there is, check if the booker is registered for that course, and assign those privileges if so
        for category in privilege_categories:
            if category.related_course is None or category.related_course == "":
                continue
            for course in courses:
                course = course.lower()
                if category.related_course in course:
                    booker.bookerprofile.privilege_categories.add(category)
                # checking for memberOf relation that contains program information
                # it will also contain the '_people_types' string
                # we find the string containing program information ('cn=X') and save the information
                if "_people_types" in course:
                    strings = course.split(",")
                    for string in strings:
                        if "cn" in string:
                            program_attributes = string.split("=")[1].split("_")
                            break
                    booker.bookerprofile.program = program_attributes[0]
                    booker.bookerprofile.graduate_level = program_attributes[1]
                    booker.bookerprofile.save()

    def assign_all_booker_privileges(self, server=ldap_server):
        bookers = User.objects.all()
        for booker in bookers:
            self.assign_booker_privileges(booker, server)
