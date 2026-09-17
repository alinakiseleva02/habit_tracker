from django import forms
from .models import Habit, HabitSchedule, HabitLog, HabitStat

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = '__all__'

class HabitScheduleForm(forms.ModelForm):
    class Meta:
        model = HabitSchedule
        fields = '__all__'

class HabitLogForm(forms.ModelForm):
    class Meta:
        model = HabitLog
        fields = '__all__'

class HabitStatForm(forms.ModelForm):
    class Meta:
        model = HabitStat
        fields = '__all__'