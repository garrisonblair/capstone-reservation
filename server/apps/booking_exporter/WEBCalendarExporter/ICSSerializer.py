

class ICSSerializer:

    def serialize_booking(self, booking):

        #booking.student
        #booking.student_group (conditionally)
        summary = ""

        print('booking.student: ', booking.student)
        print('booking.student_group: ', booking.student_group)
        print('booking.start_time: ', booking.start_time)
        print('booking.end_time: ', booking.end_time)

        # DTSTART:20181012T103000
        # DTEND:20181012T120000

        ics_file = """"BEGIN:VCALENDAR
        METHOD:PUBLISH
        BEGIN:VEVENT
        UID:{}
        SUMMARY:{}
        DESCRIPTION:{}
        CLASS:PUBLIC
        STATUS:TENTATIVE
        DTSTART:{}
        DTEND:{}
        END:VEVENT
        END:VCALENDAR"""

#        ics_file.format(booking.id, 1,1, , )
        return ics_file


