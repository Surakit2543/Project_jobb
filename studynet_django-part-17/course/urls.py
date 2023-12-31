from django.urls import path

from course import views

urlpatterns = [
    path('', views.get_courses),
    path('get_my_courses/', views.get_my_courses),
    path('get_frontpage_courses/', views.get_frontpage_courses),
    path('get_categories/', views.get_categories),
    path('get_author_courses/<int:user_id>/', views.get_author_courses),
    path('create/', views.create_course),
    path('edit/<slug:id>', views.edit_course),
    path('delete/<slug:id>', views.delete_course),
    path('create_file/',views.create_file),
    path('edit_file/<int:id>',views.edit_file),
    path('delete_file/<int:id>',views.delete_file),
    path('get_file/',views.get_file),
    path('download_file/<int:id>',views.downloadFile),
    path('<slug:slug>/', views.get_course),
    path('<slug:course_slug>/<slug:lesson_slug>/', views.add_comment),
    path('<slug:course_slug>/<slug:lesson_slug>/get-comments/', views.get_comments),
    path('<slug:course_slug>/<slug:lesson_slug>/get-quiz/', views.get_quiz),
]