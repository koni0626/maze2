# coding:UTF-8
import os
import json
import hashlib
import uuid

from django.db.models import Max

from .models import Maze
from .models import ApiKeys
from .models import PracticeHistory
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .Component.mouse2 import Mouse2

@csrf_exempt
def start(request, api_key, map_id):
    # api_keyからユーザーIDを取得する
    try:
        api_key_record = ApiKeys.objects.get(api_key=api_key)
        user = api_key_record.user
    except ApiKeys.DoesNotExist:
        ret = {"status": "NG", "message": "api_keyが不正です"}
        return JsonResponse(ret)

    # マップIDからマップの情報を取得する
    try:
        maze = Maze.objects.get(id=map_id)
    except Maze.DoesNotExist:
        ret = {"status": "NG", "message": "map_idが不正です"}
        return JsonResponse(ret)

    # token生成
    token = hashlib.sha256(str(uuid.uuid4()).encode('utf-8')).hexdigest()
    # ここでユーザの操作履歴を保存する
    try:
        history = PracticeHistory(user=user,
                                  token=token,
                                  maze=maze,
                                  turn=0,
                                  step=0,
                                  pos_x=maze.start_pos_x,
                                  pos_y=maze.start_pos_y,
                                  action=0)
        history.save()
    except:
        ret = {"status": "NG", "message": "記録に失敗しました"}
        return JsonResponse(ret)

    ret = {"status": "OK",
           "token": token,
           "start_pos": (maze.start_pos_x, maze.start_pos_y),
           "goal_pos": (maze.goal_pos_x, maze.goal_pos_y),
           "turn": maze.turn,
           "step": maze.step}

    return JsonResponse(ret)


@csrf_exempt
def sensor(request, token):
    mouse = Mouse2(token)
    sensor = mouse.get_sensor()

    return JsonResponse({"status": "OK", "sensor": sensor})


@csrf_exempt
def action(request, token, action):
    mouse = Mouse2(token)
    try:
        record = mouse.set_action(action)
        mouse.save_history()
    except:
        return JsonResponse({"status": "NG"})

    return JsonResponse({"status": "OK"})
