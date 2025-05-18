from django.db import models
from django.utils import timezone

class LogMessage(models.Model):
    message = models.CharField(max_length=300)
    log_date = models.DateTimeField("date logged")

    def __str__(self):
        """Returns a string representation of a message."""
        date = timezone.localtime(self.log_date)
        return f"'{self.message}' logged on {date.strftime('%A, %d %B, %Y at %X')}"

class WorkoutHistory(models.Model):
    day_id = models.IntegerField()
    day_title = models.CharField(max_length=200)
    duration = models.IntegerField()  # Duration in seconds
    completed_date = models.DateTimeField(auto_now_add=True)
    completed_exercises = models.JSONField(default=dict)  # Store completed exercise data

    class Meta:
        ordering = ['-completed_date']

    def __str__(self):
        return f"{self.day_title} - {self.completed_date.strftime('%Y-%m-%d %H:%M')}"

    def get_duration_display(self):
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{minutes}:{seconds:02d}"
