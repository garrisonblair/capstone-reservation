

class ICSSerializer:

    def serialize_booking(self, booking):

        student_id = booking.student.student_id
        student_group = booking.student_group

        summary = 'Student: ' + str(student_id) + ', ' + 'Group: ' + str(student_group)

        description = summary

        dt_start_yyyy = booking.date.year
        dt_start_mm = booking.date.month
        dt_start_dd = booking.date.day

        if len(str(dt_start_mm)) == 1:
            dt_start_mm = '0' + str(dt_start_mm)

        if len(str(dt_start_dd)) == 1:
            dt_start_dd = '0' + str(dt_start_dd)

        dt_start_date = str(dt_start_yyyy) + str(dt_start_mm) + str(dt_start_dd)


        dt_end_yyyy = booking.date.year
        dt_end_mm = booking.date.month
        dt_end_dd = booking.date.day

        if len(str(dt_end_mm)) == 1:
            dt_end_mm = '0' + str(dt_end_mm)

        if len(str(dt_end_dd)) == 1:
            dt_end_dd = '0' + str(dt_end_dd)

        dt_end_date = str(dt_end_yyyy) + str(dt_end_mm) + str(dt_end_dd)


        dt_start_h = booking.start_time.hour
        dt_start_m = booking.start_time.minute
        dt_start_s = booking.start_time.second

        if len(str(dt_start_h)) == 1:
            dt_start_h = '0' + str(dt_start_h)

        if len(str(dt_start_m)) == 1:
            dt_start_m = '0' + str(dt_start_m)

        if len(str(dt_start_s)) == 1:
             dt_start_s = '0' + str(dt_start_s)

        dt_start_time = str(dt_start_h) + str(dt_start_m) + str(dt_start_s)


        dt_end_h = booking.end_time.hour
        dt_end_m = booking.end_time.minute
        dt_end_s = booking.end_time.second

        if len(str(dt_end_h)) == 1:
            dt_end_h = '0' + str(dt_end_h)

        if len(str(dt_end_m)) == 1:
            dt_end_m = '0' + str(dt_end_m)

        if len(str(dt_end_s)) == 1:
             dt_end_s = '0' + str(dt_end_s)

        dt_end_time = str(dt_end_h) + str(dt_end_m) + str(dt_end_s)

        dt_start = 'DTSTART:' + str(dt_start_date) + 'T' + str(dt_start_time)
        dt_end = 'DTEND:' + str(dt_end_date) + 'T' + str(dt_end_time)

#        print('Constructed DTSTART', str(dt_start))
#        print('Constructed DTEND', str(dt_end))

        arg0 = booking.id
        arg1 = summary
        arg2 = description
        arg3 = dt_start
        arg4 = dt_end

        ics_file = """BEGIN:VCALENDAR
METHOD:PUBLISH
BEGIN:VEVENT
UID: %s
SUMMARY:%s
DESCRIPTION:%s
CLASS:PUBLIC
STATUS:TENTATIVE
DTSTART:%s
DTEND:%s
END:VEVENT
END:VCALENDAR""" % (str(arg0), str(arg1), str(arg2), str(arg3), str(arg4))

        print(str(ics_file))

        return ics_file


