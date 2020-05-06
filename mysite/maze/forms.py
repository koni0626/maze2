# coding:UTF-8
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class MazeForm(forms.Form):
    maze_name = forms.CharField(label='迷路名', widget=forms.TextInput(attrs={"size": 100}))
    maze_size_x = forms.IntegerField(label="迷路の幅")
    maze_size_y = forms.IntegerField(label="迷路の高さ")
    start_pos_x = forms.IntegerField(label="開始位置X")
    start_pos_y = forms.IntegerField(label="開始位置Y")
    goal_pos_x = forms.IntegerField(label="終了位置X")
    goal_pos_y = forms.IntegerField(label="終了位置Y")
    turn = forms.IntegerField(label="ターン数")
    step = forms.IntegerField(label="ステップ数")


class SignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username',)