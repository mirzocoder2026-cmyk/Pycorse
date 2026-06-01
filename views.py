from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
import json

from .models import Course, Topic, Video, Test, Task, Enrollment, VideoProgress, TestResult, TaskSubmission
from users.models import CustomUser


def home_view(request):
    return render(request, 'courses/home.html', {'courses': Course.objects.filter(is_active=True)})


@login_required
def course_list_view(request):
    enrolled_ids = Enrollment.objects.filter(user=request.user).values_list('course_id', flat=True)
    return render(request, 'courses/course_list.html', {
        'courses': Course.objects.filter(is_active=True),
        'enrolled_ids': list(enrolled_ids),
    })


@login_required
def course_detail_view(request, pk):
    course     = get_object_or_404(Course, pk=pk)
    enrollment, _ = Enrollment.objects.get_or_create(user=request.user, course=course)
    watched    = list(VideoProgress.objects.filter(user=request.user, video__course=course, watched=True).values_list('video_id', flat=True))
    answered   = list(TestResult.objects.filter(user=request.user, test__course=course).values_list('test_id', flat=True))
    total      = course.videos.count() + course.tests.count()
    done       = len(watched) + len(answered)
    progress   = int(done / total * 100) if total else 0
    enrollment.progress = progress
    enrollment.save()
    return render(request, 'courses/course_detail.html', {
        'course': course, 'enrollment': enrollment,
        'topics': course.topics.all(), 'videos': course.videos.all(),
        'tests': course.tests.all(), 'tasks': course.tasks.all(),
        'watched': watched, 'answered': answered, 'progress': progress,
    })


@login_required
@require_POST
def api_video_watched(request, vid):
    video = get_object_or_404(Video, pk=vid)
    vp, created = VideoProgress.objects.get_or_create(user=request.user, video=video)
    if not vp.watched:
        vp.watched = True; vp.watched_at = timezone.now(); vp.save()
        request.user.score += 5; request.user.save()
    return JsonResponse({'ok': True, 'score': request.user.score})


@login_required
@require_POST
def api_test_submit(request, tid):
    test   = get_object_or_404(Test, pk=tid)
    data   = json.loads(request.body)
    answer = data.get('answer','')
    correct = (answer == test.correct_answer)
    result, created = TestResult.objects.get_or_create(
        user=request.user, test=test,
        defaults={'selected_answer': answer, 'is_correct': correct}
    )
    if not created:
        return JsonResponse({'ok': True, 'correct': result.is_correct, 'correct_answer': test.correct_answer, 'already': True})
    if correct:
        request.user.score += test.score_points; request.user.save()
    return JsonResponse({'ok': True, 'correct': correct, 'correct_answer': test.correct_answer, 'score': request.user.score})


@login_required
@require_POST
def api_task_submit(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    data = json.loads(request.body)
    code = data.get('code','').strip()
    if not code:
        return JsonResponse({'ok': False, 'msg': 'Код холӣ аст!'})
    sub = TaskSubmission.objects.create(user=request.user, task=task, code=code)
    return JsonResponse({'ok': True, 'id': sub.id})


def rating_view(request):
    students = CustomUser.objects.filter(role='student', is_active=True).order_by('-score')[:50]
    return render(request, 'courses/rating.html', {'students': students})


def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.role == 'admin')


@login_required
@user_passes_test(is_admin)
def admin_panel_view(request):
    return render(request, 'courses/admin_panel.html', {
        'total_students': CustomUser.objects.filter(role='student').count(),
        'total_courses':  Course.objects.count(),
        'total_videos':   Video.objects.count(),
        'pending':        TaskSubmission.objects.filter(status='pending').count(),
        'submissions':    TaskSubmission.objects.select_related('user','task').order_by('-submitted_at')[:15],
        'top_students':   CustomUser.objects.filter(role='student').order_by('-score')[:10],
        'courses':        Course.objects.all(),
    })


@login_required
@user_passes_test(is_admin)
def admin_content_view(request, section):
    ctx = {'section': section, 'courses': Course.objects.all()}

    if request.method == 'POST':
        action = request.POST.get('action','')

        if action == 'add_course':
            Course.objects.create(
                title=request.POST['title'], category=request.POST['category'],
                description=request.POST.get('description',''), icon=request.POST.get('icon','📚'),
                duration_hours=request.POST.get('duration_hours',0))
            messages.success(request, 'Курс илова шуд!')

        elif action == 'del_course':
            Course.objects.filter(pk=request.POST['pk']).delete()
            messages.success(request, 'Ҳазф шуд!')

        elif action == 'add_video':
            course = get_object_or_404(Course, pk=request.POST['course_id'])
            Video.objects.create(
                course=course, title=request.POST['title'],
                description=request.POST.get('description',''),
                duration_minutes=request.POST.get('duration_minutes',0),
                video_url=request.POST.get('video_url',''),
                video_file=request.FILES.get('video_file'),
                order=course.videos.count()+1)
            messages.success(request, 'Видео илова шуд!')

        elif action == 'del_video':
            Video.objects.filter(pk=request.POST['pk']).delete()
            messages.success(request, 'Ҳазф шуд!')

        elif action == 'add_topic':
            course = get_object_or_404(Course, pk=request.POST['course_id'])
            Topic.objects.create(
                course=course, title=request.POST['title'],
                description=request.POST.get('description',''),
                order=course.topics.count()+1)
            messages.success(request, 'Мавзуъ илова шуд!')

        elif action == 'del_topic':
            Topic.objects.filter(pk=request.POST['pk']).delete()
            messages.success(request, 'Ҳазф шуд!')

        elif action == 'add_test':
            course = get_object_or_404(Course, pk=request.POST['course_id'])
            Test.objects.create(
                course=course, question=request.POST['question'],
                option_a=request.POST['option_a'], option_b=request.POST['option_b'],
                option_c=request.POST.get('option_c',''), option_d=request.POST.get('option_d',''),
                correct_answer=request.POST['correct_answer'],
                score_points=request.POST.get('score_points',10))
            messages.success(request, 'Тест илова шуд!')

        elif action == 'del_test':
            Test.objects.filter(pk=request.POST['pk']).delete()
            messages.success(request, 'Ҳазф шуд!')

        elif action == 'add_task':
            course = get_object_or_404(Course, pk=request.POST['course_id'])
            Task.objects.create(
                course=course, title=request.POST['title'],
                description=request.POST.get('description',''),
                starter_code=request.POST.get('starter_code',''),
                score_points=request.POST.get('score_points',50),
                order=course.tasks.count()+1)
            messages.success(request, 'Вазифа илова шуд!')

        elif action == 'del_task':
            Task.objects.filter(pk=request.POST['pk']).delete()
            messages.success(request, 'Ҳазф шуд!')

        elif action == 'approve':
            sub = get_object_or_404(TaskSubmission, pk=request.POST['pk'])
            sub.status='approved'; sub.feedback=request.POST.get('feedback','Баракалла!')
            sub.reviewed_at=timezone.now(); sub.save()
            sub.user.score += sub.task.score_points; sub.user.save()
            messages.success(request, 'Тасдиқ шуд!')

        elif action == 'reject':
            sub = get_object_or_404(TaskSubmission, pk=request.POST['pk'])
            sub.status='rejected'; sub.feedback=request.POST.get('feedback','Аз нав кӯшиш кун.')
            sub.reviewed_at=timezone.now(); sub.save()
            messages.success(request, 'Рад шуд!')

        return redirect('admin_content', section=section)

    if section == 'courses':
        ctx['items'] = Course.objects.all()
    elif section == 'videos':
        ctx['items'] = Video.objects.select_related('course').all()
    elif section == 'topics':
        ctx['items'] = Topic.objects.select_related('course').all()
    elif section == 'tests':
        ctx['items'] = Test.objects.select_related('course').all()
    elif section == 'tasks':
        ctx['items'] = Task.objects.select_related('course').all()
    elif section == 'submissions':
        ctx['items'] = TaskSubmission.objects.select_related('user','task__course').order_by('-submitted_at')
    elif section == 'students':
        ctx['items'] = CustomUser.objects.filter(role='student').order_by('-score')

    return render(request, 'courses/admin_content.html', ctx)
