import os
import json
import numpy as np
import hashlib
import uuid
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .models import Maze, ApiKeys
from .Component.mouse import Mouse


def signup(request):
    """
    サインアップでユーザ新規追加という意味らしい
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)

            # APIキーを作成する
            api_key = hashlib.sha256(str(uuid.uuid4()).encode('utf-8')).hexdigest()
            api_key_record = ApiKeys(user=user, api_key=api_key)
            api_key_record.save()

            return redirect('index')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        #ここのフォームがcreate用のフォームになっている。
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            # ここをダッシュボードにする
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


@login_required(login_url='login/')
def logout(request):
    auth.logout(request)
    return redirect('index')


def index(request):

    return render(request, "index.html", {'data': "hello world!!!"})


def practice(request, maze_id, action=0):
    record = Maze.objects.get(id=maze_id)
    json_file = record.maze_file_name
    full_path = os.path.join("maze_media/maze/", json_file)
    data = None
    with open(full_path) as f:
        data = json.load(f)

    if action == 0:
        mouse_pos_x = record.start_pos_x
        mouse_pos_y = record.start_pos_y
        request.session["mouse_pos_x"] = mouse_pos_x
        request.session["mouse_pos_y"] = mouse_pos_y
        request.session["mouse_vec"] = 0
        request.session["status"] = 0
        request.session["memory"] = np.zeros((record.maze_size_x, record.maze_size_y)).tolist()

    mouse = Mouse(request.session, data)
    try:
        result = mouse.set_action(action)
        mouse_pos_x = result["mouse_pos_x"]
        mouse_pos_y = result["mouse_pos_y"]
        mouse_vec = result["mouse_vec"]
        mouse_icon = result["mouse_icon"]

        request.session["mouse_pos_x"] = mouse_pos_x
        request.session["mouse_pos_y"] = mouse_pos_y
        request.session["mouse_vec"] = mouse_vec
        request.session["mouse_icon"] = mouse_icon
        data[mouse_pos_y][mouse_pos_x] = 4.
    except:
        mouse_pos_x = request.session["mouse_pos_x"]
        mouse_pos_y = request.session["mouse_pos_y"]
        mouse_icon = request.session["mouse_icon"]

    data[mouse_pos_y][mouse_pos_x] = 4.

    sensor, memory = mouse.get_sensor()
    request.session["memory"] = memory
    for y in range(record.maze_size_y):
        for x in range(record.maze_size_x):
            if memory[y][x] == 0:
                data[y][x] = 5

    return render(request, "practice.html", {'record': record, 'maze_data': data, 'mouse_icon': mouse_icon, 'sensor': sensor, 'memory': memory})


@login_required(login_url='login/')
def dashboard(request):
    # 練習用ステージを選択する
    maze_records = Maze.objects.all()

    return render(request, "dashboard.html", {"maze_records": maze_records})


@login_required(login_url='login/')
def api_key(request):
    user = request.user
    record = ApiKeys.objects.get(user=user)
    api_key = record.api_key
    print(api_key)
    return render(request, "api_key.html", {"api_key": api_key})