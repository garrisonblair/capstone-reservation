# import datetime
#
# from django.test import TestCase
# from unittest import mock, skip
#
# from apps.booking_exporter.WEBCalendarExporter.WEBCalendarExporter import WEBCalendarExporter
# from apps.booking_exporter.models.bookingExporterModels import ExternalRoomID
#
# from apps.booking.models.Booking import Booking
# from apps.rooms.models.Room import Room
# from apps.accounts.models.User import User
# from apps.system_administration.models.system_settings import SystemSettings
#
#
# class testWebCalendarExporter(TestCase):
#
#     TEST_ICS = """BEGIN:VCALENDAR
# METHOD:PUBLISH
# BEGIN:VEVENT
# UID:1
# SUMMARY:Test Booking
# DESCRIPTION:Test Bookings
# CLASS:PUBLIC
# STATUS:TENTATIVE
# DTSTART:20181012T103000
# DTEND:20181012T120000
# END:VEVENT
# END:VCALENDAR"""
#
#     def setUp(self):
#         room = Room(name="Room 1")
#         room.save()
#
#         external_id = ExternalRoomID(external_id="_ROOM1_")
#         external_id.room = room
#         external_id.save()
#
#         booker = User.objects.create_user(username="s_loc")
#         booker.save()
#
#         self.booking = Booking(start_time=datetime.time(12, 0, 0),
#                                end_time=datetime.time(13, 0, 0),
#                                date=datetime.date(2018, 10, 12),
#                                booker=booker,
#                                room=room)
#         self.booking.save()
#
#         self.response_mock = mock.Mock()
#         self.response_mock.text = ""
#
#         self.session_mock = mock.Mock()
#         self.session_mock.post.return_value = self.response_mock
#
#     def testLoginSuccess(self):
#
#         settings = SystemSettings.get_settings()
#
#         settings.webcalendar_username = "f_daigl"
#         settings.webcalendar_password = "mySafePassword"
#         settings.save()
#
#         exporter = WEBCalendarExporter(self.session_mock)
#         exporter.login()
#
#         self.assertEqual(self.session_mock.post.call_count, 1)
#
#         self.assertEqual(self.session_mock.post.call_args[1],
#                          {"data": {
#                                 "login": settings.webcalendar_username,
#                                 "password": settings.webcalendar_password}
#                           })
#
#         self.assertEqual(self.session_mock.post.call_args[0][0],
#                          WEBCalendarExporter.LOGIN_URL)
#
#     @skip
#     def testBackupBooking(self):
#
#         serializer_mock = mock.Mock()
#         serializer_mock.serialize_booking.return_value = self.TEST_ICS
#
#         self.exporter = WEBCalendarExporter(self.session_mock, serializer_mock)
#         self.exporter.backup_booking(self.booking)
#
#         self.assertEqual(self.session_mock.post.call_args[0][0],
#                          WEBCalendarExporter.IMPORT_HANDLER_URL)
#
#         self.assertEqual(self.session_mock.post.call_args[1],
#                          {'data': {
#                             'overwrite': 'Y',
#                             'calUser': self.booking.room.externalroomid.external_id,
#                             'ImportType': 'ICAL',
#                             'exc_private': '1'},
#                          'files': {
#                             'FileName': ('booking.ics', self.TEST_ICS)}
#                           })
