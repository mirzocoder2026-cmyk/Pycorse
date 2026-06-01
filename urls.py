from django.urls import path
from . import views

urlpatterns = [
    path('',                          views.home_view,          name='home'),
    path('courses/',                  views.course_list_view,   name='course_list'),
    path('courses/<int:pk>/',         views.course_detail_view, name='course_detail'),
    path('rating/',                   views.rating_view,        name='rating'),
    path('admin-panel/',              views.admin_panel_view,   name='admin_panel'),
    path('admin-panel/<str:section>/',views.admin_content_view, name='admin_content'),
    path('api/video/<int:vid>/watched/',   views.api_video_watched, name='api_video_watched'),
    path('api/test/<int:tid>/submit/',     views.api_test_submit,   name='api_test_submit'),
    path('api/task/<int:task_id>/submit/', views.api_task_submit,   name='api_task_submit'),
]
