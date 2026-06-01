from django.db import models
from django.conf import settings

class Course(models.Model):
    CAT = [('python','Python'),('cyber','Кибербезопасность'),('ai','Зеҳни сунъӣ')]
    title          = models.CharField(max_length=200)
    category       = models.CharField(max_length=20, choices=CAT)
    description    = models.TextField()
    icon           = models.CharField(max_length=10, default='📚')
    duration_hours = models.PositiveIntegerField(default=0)
    is_active      = models.BooleanField(default=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсҳо'
        ordering = ['id']

    def __str__(self): return self.title
    def total_videos(self): return self.videos.count()
    def total_tests(self):  return self.tests.count()
    def total_topics(self): return self.topics.count()


class Topic(models.Model):
    course      = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='topics')
    order       = models.PositiveIntegerField(default=0)
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Мавзуъ'
        verbose_name_plural = 'Мавзуъҳо'

    def __str__(self): return self.title


class Video(models.Model):
    course            = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')
    topic             = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='videos')
    order             = models.PositiveIntegerField(default=0)
    title             = models.CharField(max_length=200)
    description       = models.TextField(blank=True)
    video_file        = models.FileField(upload_to='videos/', blank=True, null=True)
    video_url         = models.URLField(blank=True)
    duration_minutes  = models.PositiveIntegerField(default=0)
    is_free           = models.BooleanField(default=False)
    created_at        = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Видео'
        verbose_name_plural = 'Видеоҳо'

    def __str__(self): return f'{self.course} — {self.title}'


class Test(models.Model):
    ANS = [('a','А'),('b','Б'),('c','В'),('d','Г')]
    course          = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tests')
    topic           = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='tests')
    question        = models.TextField()
    option_a        = models.CharField(max_length=300)
    option_b        = models.CharField(max_length=300)
    option_c        = models.CharField(max_length=300, blank=True)
    option_d        = models.CharField(max_length=300, blank=True)
    correct_answer  = models.CharField(max_length=1, choices=ANS)
    score_points    = models.PositiveIntegerField(default=10)

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тестҳо'

    def __str__(self): return self.question[:60]


class Task(models.Model):
    course        = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tasks')
    topic         = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    order         = models.PositiveIntegerField(default=0)
    title         = models.CharField(max_length=200)
    description   = models.TextField()
    starter_code  = models.TextField(blank=True)
    score_points  = models.PositiveIntegerField(default=50)

    class Meta:
        ordering = ['order']
        verbose_name = 'Вазифа'
        verbose_name_plural = 'Вазифаҳо'

    def __str__(self): return self.title


class Enrollment(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course      = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress    = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user','course')
        verbose_name = 'Бақайдгирӣ'
        verbose_name_plural = 'Бақайдгириҳо'

    def __str__(self): return f'{self.user} → {self.course}'


class VideoProgress(models.Model):
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video      = models.ForeignKey(Video, on_delete=models.CASCADE)
    watched    = models.BooleanField(default=False)
    watched_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user','video')


class TestResult(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='test_results')
    test            = models.ForeignKey(Test, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=1)
    is_correct      = models.BooleanField(default=False)
    answered_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','test')


class TaskSubmission(models.Model):
    STATUS = [('pending','⏳ Интизор'),('approved','✅ Тасдиқ'),('rejected','❌ Рад')]
    user         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')
    task         = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='submissions')
    code         = models.TextField()
    status       = models.CharField(max_length=10, choices=STATUS, default='pending')
    feedback     = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at  = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Вазифаи фиристодашуда'
        verbose_name_plural = 'Вазифаҳои фиристодашуда'

    def __str__(self): return f'{self.user} — {self.task}'
