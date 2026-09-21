from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from .models import Habit, HabitSchedule, HabitLog, HabitStat
from .forms import HabitForm, HabitScheduleForm, HabitLogForm, HabitStatForm
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class HabitListView(View):
    def get(self, request):
        name_query = request.GET.get('name')
        active_query = request.GET.get('active')

        if name_query:
            habits = Habit.objects.filter(name__icontains=name_query)
        elif active_query == 'true':
            habits = Habit.objects.filter(schedules__active=True).distinct()
        else:
            habits = Habit.objects.all()

        data = [{
            'id': h.id,
            'name': h.name,
            'description': h.description,
            'repeat_time': h.repeat_time,
            'times_per_day': h.times_per_day,
            'max_streak': h.max_streak,
            'created_at': h.created_at
        } for h in habits]
        
        return JsonResponse({'data': data})

    def post(self, request):
        try:
            new_data = json.loads(request.body)
            form = HabitForm(new_data)
            
            if form.is_valid():
                habit = form.save()
                return JsonResponse({
                    'id': habit.id,
                    'name': habit.name,
                    'description': habit.description,
                    'repeat_time': str(habit.repeat_time),
                    'times_per_day': habit.times_per_day,
                    'max_streak': habit.max_streak,
                    'created_at': habit.created_at
                }, status=201)
            
            return JsonResponse({'errors': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class HabitDetailView(View):
    def get(self, request, id):
        habit = get_object_or_404(Habit, id=id)
        data = {
            'id': habit.id,
            'name': habit.name,
            'description': habit.description,
            'repeat_time': habit.repeat_time,
            'times_per_day': habit.times_per_day,
            'max_streak': habit.max_streak,
            'created_at': habit.created_at
        }
        return JsonResponse(data)

    def put(self, request, id):
        try:
            habit = get_object_or_404(Habit, id=id)
            new_data = json.loads(request.body)
            
            form = HabitForm(new_data, instance=habit)
            
            if form.is_valid():
                habit = form.save()
                return JsonResponse({
                    'id': habit.id,
                    'name': habit.name,
                    'description': habit.description,
                    'repeat_time': str(habit.repeat_time),
                    'times_per_day': habit.times_per_day,
                    'max_streak': habit.max_streak,
                    'created_at': habit.created_at
                }, status=200) 
            
            return JsonResponse({'errors': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class ScheduleListView(View):
    def get(self, request, habit_id):
        schedules = HabitSchedule.objects.filter(habit_id=habit_id)
        data = [{
            'id': s.id,
            'habit_id': s.habit_id,
            'weekday': s.weekday,
            'active': s.active
        } for s in schedules]
        return JsonResponse({'data': data})

    def post(self, request, habit_id):
        try:
            new_data = json.loads(request.body)
            new_data['habit'] = habit_id 
            
            form = HabitScheduleForm(new_data)
            if form.is_valid():
                schedule = form.save()
                return JsonResponse({
                    'id': schedule.id,
                    'habit_id': schedule.habit_id,
                    'weekday': schedule.weekday,
                    'active': schedule.active
                }, status=201)
            return JsonResponse({'errors': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class ScheduleDetailView(View):
    def get(self, request, habit_id, id):
        schedule = get_object_or_404(HabitSchedule, id=id, habit_id=habit_id)
        data = {
            'id': schedule.id,
            'habit_id': schedule.habit_id,
            'weekday': schedule.weekday,
            'active': schedule.active
        }
        return JsonResponse(data)

    def put(self, request, habit_id, id):
        try:
            schedule = get_object_or_404(HabitSchedule, id=id, habit_id=habit_id)
            new_data = json.loads(request.body)
            new_data['habit'] = habit_id 
            
            form = HabitScheduleForm(new_data, instance=schedule)
            if form.is_valid():
                schedule = form.save()
                return JsonResponse({
                    'id': schedule.id,
                    'habit_id': schedule.habit_id,
                    'weekday': schedule.weekday,
                    'active': schedule.active
                }, status=200)
            return JsonResponse({'errors': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)


class ScheduleGlobalDetailView(View):
    def get(self, request, id):
        schedule = get_object_or_404(HabitSchedule, id=id)
        data = {
            'id': schedule.id,
            'habit_id': schedule.habit_id,
            'weekday': schedule.weekday,
            'active': schedule.active
        }
        return JsonResponse(data)


class ScheduleSearchView(View):
    def get(self, request):
        weekday_query = request.GET.get('weekday')
        active_query = request.GET.get('active')

        schedules = HabitSchedule.objects.all()
        if weekday_query:
            schedules = schedules.filter(weekday=weekday_query)
        if active_query:
            is_active = active_query.lower() == 'true'
            schedules = schedules.filter(active=is_active)

        data = [{
            'id': s.id,
            'habit_id': s.habit_id,
            'weekday': s.weekday,
            'active': s.active
        } for s in schedules]
        return JsonResponse({'data': data})

@method_decorator(csrf_exempt, name='dispatch')
class LogListView(View):
    def get(self, request, habit_id):
        logs = HabitLog.objects.filter(habit_id=habit_id)
        data = [{
            'id': l.id,
            'habit_id': l.habit_id,
            'completed_at': l.completed_at,
            'count_done': l.count_done,
            'note': l.note
        } for l in logs]
        return JsonResponse({'data': data})

    def post(self, request, habit_id):
        try:
            new_data = json.loads(request.body)
            new_data['habit'] = habit_id 
            
            form = HabitLogForm(new_data)
            if form.is_valid():
                log = form.save()
                return JsonResponse({
                    'id': log.id,
                    'habit_id': log.habit_id,
                    'completed_at': log.completed_at,
                    'count_done': log.count_done,
                    'note': log.note
                }, status=201)
            return JsonResponse({'errors': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class LogDetailView(View):
    def get(self, request, habit_id, id):
        log = get_object_or_404(HabitLog, id=id, habit_id=habit_id)
        data = {
            'id': log.id,
            'habit_id': log.habit_id,
            'completed_at': log.completed_at,
            'count_done': log.count_done,
            'note': log.note
        }
        return JsonResponse(data)

    def put(self, request, habit_id, id):
        try:
            log = get_object_or_404(HabitLog, id=id, habit_id=habit_id)
            new_data = json.loads(request.body)
            new_data['habit'] = habit_id
            
            form = HabitLogForm(new_data, instance=log)
            if form.is_valid():
                log = form.save()
                return JsonResponse({
                    'id': log.id,
                    'habit_id': log.habit_id,
                    'completed_at': log.completed_at,
                    'count_done': log.count_done,
                    'note': log.note
                }, status=200)
            return JsonResponse({'errors': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)


class LogGlobalDetailView(View):
    def get(self, request, id):
        log = get_object_or_404(HabitLog, id=id)
        data = {
            'id': log.id,
            'habit_id': log.habit_id,
            'completed_at': log.completed_at,
            'count_done': log.count_done,
            'note': log.note
        }
        return JsonResponse(data)


class LogSearchView(View):
    def get(self, request):
        from_date = request.GET.get('from')
        to_date = request.GET.get('to')
        habit_id = request.GET.get('habit_id')
        date_query = request.GET.get('date')

        logs = HabitLog.objects.all()

        if from_date and to_date:
            logs = logs.filter(completed_at__date__range=[from_date, to_date])
        
        if habit_id and date_query:
            logs = logs.filter(habit_id=habit_id, completed_at__date=date_query)
        elif habit_id:
            logs = logs.filter(habit_id=habit_id)
        elif date_query:
            logs = logs.filter(completed_at__date=date_query)

        data = [{
            'id': l.id,
            'habit_id': l.habit_id,
            'completed_at': l.completed_at,
            'count_done': l.count_done,
            'note': l.note
        } for l in logs]
        return JsonResponse({'data': data})

@method_decorator(csrf_exempt, name='dispatch')
class StatListView(View):
    def get(self, request, habit_id):
        stats = HabitStat.objects.filter(habit_id=habit_id)
        data = [{
            'id': s.id,
            'habit_id': s.habit_id,
            'period_start': s.period_start,
            'period_end': s.period_end,
            'total_done': s.total_done,
            'current_streak': s.current_streak,
            'max_streak': s.max_streak,
            'success_rate': s.success_rate
        } for s in stats]
        return JsonResponse({'data': data})

    def post(self, request, habit_id):
        try:
            new_data = json.loads(request.body)
            new_data['habit'] = habit_id
            
            form = HabitStatForm(new_data)
            if form.is_valid():
                stat = form.save()
                return JsonResponse({
                    'id': stat.id,
                    'habit_id': stat.habit_id,
                    'period_start': stat.period_start,
                    'period_end': stat.period_end,
                    'total_done': stat.total_done,
                    'current_streak': stat.current_streak,
                    'max_streak': stat.max_streak,
                    'success_rate': stat.success_rate
                }, status=201)
            return JsonResponse({'errors': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class StatDetailView(View):
    def get(self, request, habit_id, id):
        stat = get_object_or_404(HabitStat, id=id, habit_id=habit_id)
        data = {
            'id': stat.id,
            'habit_id': stat.habit_id,
            'period_start': stat.period_start,
            'period_end': stat.period_end,
            'total_done': stat.total_done,
            'current_streak': stat.current_streak,
            'max_streak': stat.max_streak,
            'success_rate': stat.success_rate
        }
        return JsonResponse(data)

    def put(self, request, habit_id, id):
        try:
            stat = get_object_or_404(HabitStat, id=id, habit_id=habit_id)
            new_data = json.loads(request.body)
            new_data['habit'] = habit_id
            
            form = HabitStatForm(new_data, instance=stat)
            if form.is_valid():
                stat = form.save()
                return JsonResponse({
                    'id': stat.id,
                    'habit_id': stat.habit_id,
                    'period_start': stat.period_start,
                    'period_end': stat.period_end,
                    'total_done': stat.total_done,
                    'current_streak': stat.current_streak,
                    'max_streak': stat.max_streak,
                    'success_rate': stat.success_rate
                }, status=200)
            return JsonResponse({'errors': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)


class StatGlobalDetailView(View):
    def get(self, request, id):
        stat = get_object_or_404(HabitStat, id=id)
        data = {
            'id': stat.id,
            'habit_id': stat.habit_id,
            'period_start': stat.period_start,
            'period_end': stat.period_end,
            'total_done': stat.total_done,
            'current_streak': stat.current_streak,
            'max_streak': stat.max_streak,
            'success_rate': stat.success_rate
        }
        return JsonResponse(data)


class StatSearchView(View):
    def get(self, request):
        from_date = request.GET.get('from')
        to_date = request.GET.get('to')

        stats = HabitStat.objects.all()
        if from_date and to_date:
            stats = stats.filter(period_start__gte=from_date, period_end__lte=to_date)

        data = [{
            'id': s.id,
            'habit_id': s.habit_id,
            'period_start': s.period_start,
            'period_end': s.period_end,
            'total_done': s.total_done,
            'current_streak': s.current_streak,
            'max_streak': s.max_streak,
            'success_rate': s.success_rate
        } for s in stats]
        return JsonResponse({'data': data})