from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.login, name='login'),              # Default homepage → login page
    path('login/', views.login, name='login'),        # Explicit login URL
    path('signup/', views.signup, name='signup'),     # Signup form page
    path('signup_user/', views.signup_user, name='signup_user'),  # AJAX POST handler for signup
    
    
    path('home/', views.home, name='home'),
    path('login_user/', views.login_user, name='login_user'),
    path('get_username/', views.get_username, name='get_username'),
    
    
    
    
    
    path('user/', views.user_profile, name='user_profile'),
    path('upload/',views.upload,name = 'upload'),
    
    # New path to fetch random questions for user to answer
    path('get_random_questions/', views.get_random_questions, name='get_random_questions'),
    
    path('submit_answers/', views.submit_answers, name='submit_answers'),
    path('evaluate_answers/', views.evaluate_answers, name='evaluate_answers'),
    
    
    path('save_report/', views.save_report, name='save_report'),
    
    path('view_answers/', views.view_answers, name='view_answers'),


    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
