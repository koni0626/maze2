from django.urls import path
from . import views
from . import rests

urlpatterns = [
    path('', views.index, name='index'),
    path('stage/', views.stage, name='stage'),
    path('practice/<int:maze_id>/<int:action>', views.practice, name='practice'),
    path('history_list/<int:maze_id>', views.history_list, name='history_list'),
    path('history_delete/<int:maze_id>/<str:token>', views.history_delete, name='history_delete'),
    path('replay/<int:maze_id>/<str:token>', views.replay, name='replay'),

    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('api_key/', views.api_key, name='api_key'),

    path('v1/start/<str:api_key>/<int:map_id>', rests.start, name='rest_start'),
    path('v1/sensor/<str:token>', rests.sensor, name='rest_sensor'),
    path('v1/turn_left/<str:token>', rests.turn_left, name='turn_left'),
    path('v1/turn_right/<str:token>', rests.turn_right, name='turn_right'),
    path('v1/go_straight/<str:token>', rests.go_straight, name='go_straight'),

]
