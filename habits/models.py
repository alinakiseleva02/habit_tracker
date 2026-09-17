from django.db import models

class Habit(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    repeat_time = models.TimeField()
    times_per_day = models.SmallIntegerField()
    max_streak = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class HabitSchedule(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='schedules')
    weekday = models.SmallIntegerField() 
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.habit.name} - Day {self.weekday}"

class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='logs')
    completed_at = models.DateTimeField()
    count_done = models.SmallIntegerField()
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.habit.name} at {self.completed_at}"

class HabitStat(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='stats')
    period_start = models.DateField()
    period_end = models.DateField()
    total_done = models.IntegerField()
    current_streak = models.IntegerField()
    max_streak = models.IntegerField()
    success_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Stats for {self.habit.name} ({self.period_start} - {self.period_end})"