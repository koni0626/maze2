from django.urls import path
from . import views
from . import rests

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('practice/<int:maze_id>/<int:action>', views.practice, name='practice'),

    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('api_key/', views.api_key, name='api_key'),

    path('v1/start/<str:api_key>/<int:map_id>', rests.start, name='rest_start'),
    path('v1/sensor/<str:token>', rests.sensor, name='rest_sensor'),
    path('v1/action/<str:token>/<str:action>', rests.action, name='rest_action'),
]
