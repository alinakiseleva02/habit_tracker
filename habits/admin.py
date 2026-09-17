from django.contrib import admin
from .models import Habit, HabitSchedule, HabitLog, HabitStat

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'times_per_day', 'created_at')

@admin.register(HabitSchedule)
class HabitScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'habit', 'weekday', 'active')

@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'habit', 'completed_at', 'count_done')

@admin.register(HabitStat)
class HabitStatAdmin(admin.ModelAdmin):
    list_display = ('id', 'habit', 'period_start', 'period_end', 'success_rate')