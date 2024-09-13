from django.db import models
from members.models import Members

class Event(models.Model):
    eventName = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.eventName

class Attendance(models.Model):
    member = models.ForeignKey(Members, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member.firstName} {self.member.lastName} attended {self.event.eventName}"
