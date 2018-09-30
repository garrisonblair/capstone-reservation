from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.accounts.models.Student import Student
from apps.accounts.models.Room import Room

class Booking(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
	
    def save(self, *args, **kwargs):	
        if Booking.objects.filter(room=self.room, date=self.date, start_time=self.start_time, end_time=self.end_time).exists():
            print('The room is occupied at the specified period.')
        elif Booking.objects.filter(room=self.room, date=self.date, start_time__gte=self.start_time, start_time__lte=self.end_time).exists():
            print('The specified period is overlapped with other bookings.')
        elif Booking.objects.filter(room=self.room, date=self.date, end_time__gte=self.start_time, end_time__lte=self.end_time).exists():
            print('The specified period is overlapped with other bookings.')
        else:
            super(Booking, self).save(*args, **kwargs)
			
    def __str__(self):
        return 'Booking: %d, Student: %s, Room: %s, Date: %s, Start time: %s, End Time: %s' % (self.id, self.student.student_id, self.room.room_id, self.date, self.start_time, self.end_time)
		