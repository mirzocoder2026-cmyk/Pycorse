from django.contrib import admin
from .models import Course, Topic, Video, Test, Task, Enrollment, TaskSubmission

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title','category','duration_hours','is_active')
    list_filter  = ('category','is_active')

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title','course','order')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title','course','order','duration_minutes')

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('question','course','correct_answer','score_points')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title','course','score_points')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user','course','progress','enrolled_at')

@admin.register(TaskSubmission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user','task','status','submitted_at')
    list_filter  = ('status',)
