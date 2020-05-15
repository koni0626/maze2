# coding:UTF-8
import os
import json
import hashlib
import uuid
import traceback
from django.db.models import Max

from .models import Maze
from .models import ApiKeys
from .models import PracticeHistory
from .models import TokenStatus
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from .Component.mouse2 import Mouse2


def token_check(token):
    ret = True
    result = None
    try:
        token_status = TokenStatus.objects.get(token=token)
        if token_status.status == 1:
            result = {"status": "NG", "message": "ゲームオーバーです"}
            ret = False
        elif token_status.status == 2:
            result = {"status": "NG", "message": "すでにゴールしています"}
    except Exception as e:
        result = {"status": "NG", "message": "tokenが不正です"}
        ret = False

    return ret, result


def adjust_step(mouse):
    ret = False
    msg = {"status": "OK"}
    if mouse.is_step_over():
        try:
            mouse.set_next_turn()
            if mouse.is_turn_over():
                mouse.game_over()
                #mouse.save_history()
                ret = True
                msg = {"status": "NG", "message": "本走行終了です"}
            else:
                mouse.save_history()
                ret = True
                msg = {"status": "NG", "message": "ターン終了です"}
        except Exception as e:
            traceback.print_exc()
            msg = {"status": "NG"}
    return ret, msg


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
        with transaction.atomic():
            history = PracticeHistory(user=user,
                                      token=token,
                                      maze=maze,
                                      turn=0,
                                      step=0,
                                      pos_x=maze.start_pos_x,
                                      pos_y=maze.start_pos_y,
                                      vec=0,
                                      action=0)
            history.save()

            token_status = TokenStatus(token=token,
                                       status=0)
            token_status.save()

            ret = {"status": "OK",
                   "token": token,
                   "start_pos": (maze.start_pos_x, maze.start_pos_y),
                   "goal_pos": (maze.goal_pos_x, maze.goal_pos_y),
                   "turn": maze.turn,
                   "step": maze.step}

    except Exception as e:
        traceback.print_exc()
        ret = {"status": "NG", "message": "記録に失敗しました"}

    return JsonResponse(ret)




@csrf_exempt
def sensor(request, token):
    ret, result = token_check(token)
    if not ret:
        return JsonResponse(result)

    mouse = Mouse2(token)
    sensor = mouse.get_sensor()

    return JsonResponse({"status": "OK", "sensor": sensor})


@csrf_exempt
def turn_right(request, token):
    ret, result = token_check(token)
    if not ret:
        return JsonResponse(result)

    try:
        mouse = Mouse2(token)
        mouse.turn_right()
        mouse.save_history()
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"status": "NG"})

    _, msg = adjust_step(mouse)

    return JsonResponse(msg)


@csrf_exempt
def turn_left(request, token):
    ret, result = token_check(token)
    if not ret:
        return JsonResponse(result)

    try:
        mouse = Mouse2(token)
        mouse.turn_left()
        mouse.save_history()
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"status": "NG"})

    _, msg = adjust_step(mouse)

    return JsonResponse(msg)


@csrf_exempt
def go_straight(request, token):
    ret, result = token_check(token)
    if not ret:
        return JsonResponse(result)

    mouse = Mouse2(token)
    if not mouse.go_straight():
        # 衝突した
        try:
            mouse.game_over()
            mouse.save_history()
            return JsonResponse({"status": "NG", "message": "壁に衝突しました。ゲームオーバーです"})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({"status": "NG"})

    ret, msg = adjust_step(mouse)
    if ret:
        return JsonResponse(msg)

    if mouse.is_goal():
        try:
            if mouse.is_last_turn():
                mouse.game_clear()
                mouse.save_history()
                return JsonResponse({"status": "NG", "message": "ゲームクリアです"})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({"status": "NG"})

    try:
        mouse.save_history()
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"status": "NG"})

    return JsonResponse({"status": "OK"})


@csrf_exempt
def is_goal(request, token):
    try:
        token_check(token)
    except Exception as e:
        return JsonResponse({"status": "OK", "goal": 0})

    # 履歴の最終状態が(7,7)かどうかを見ればいい。
    response = {"status": "NG"}
    try:
        mouse = Mouse2(token)
        if mouse.is_goal():
            response = {"status": "OK", "goal": 1}
        else:
            response = {"status": "OK", "goal": 0}
    except Exception as e:
        traceback.print_exc()

    return JsonResponse(response)