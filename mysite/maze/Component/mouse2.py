# coding:UTF-8
import os
import json
from django.db.models import Max
from maze.models import Maze
from maze.models import PracticeHistory


class Mouse2(object):
    def __init__(self, token):
        max_id = PracticeHistory.objects.filter(token=token).aggregate(Max('id'))
        history = PracticeHistory.objects.get(id=max_id["id__max"])
        map_id = history.maze_id
        record = Maze.objects.get(id=map_id)
        json_file = record.maze_file_name

        self.now_pos_x = history.pos_x
        self.now_pos_y = history.pos_y
        self.now_vec = history.vec
        full_path = os.path.join("maze_media/maze/", json_file)
        with open(full_path) as f:
            self.data = json.load(f)

        self.token = token
        self.user = history.user
        self.maze = history.maze
        self.turn = history.turn
        self.step = history.step + 1
        self.action = history.action


    def save_history(self):
        history = PracticeHistory(user=self.user,
                                  token=self.token,
                                  maze=self.maze,
                                  turn=self.turn,
                                  step=self.step,
                                  pos_x=self.now_pos_x,
                                  pos_y=self.now_pos_y,
                                  vec = self.now_vec,
                                  action=self.action)
        history.save()

    def get_sensor(self):
        if self.now_vec == 0:
            # 北
            left = self.data[self.now_pos_y][self.now_pos_x - 1]
            front = self.data[self.now_pos_y - 1][self.now_pos_x]
            right = self.data[self.now_pos_y][self.now_pos_x + 1]

        elif self.now_vec == 1:
            # 東
            left = self.data[self.now_pos_y - 1][self.now_pos_x]
            front = self.data[self.now_pos_y][self.now_pos_x + 1]
            right = self.data[self.now_pos_y + 1][self.now_pos_x]

        elif self.now_vec == 2:
            # 南
            left = self.data[self.now_pos_y][self.now_pos_x + 1]
            front = self.data[self.now_pos_y + 1][self.now_pos_x]
            right = self.data[self.now_pos_y][self.now_pos_x - 1]
        else:
            # 西
            left = self.data[self.now_pos_y + 1][self.now_pos_x]
            front = self.data[self.now_pos_y][self.now_pos_x - 1]
            right = self.data[self.now_pos_y - 1][self.now_pos_x]
        if left != 1:
            left = 0
        if front != 1:
            front = 0
        if right != 1:
            right = 0

        return [left, front, right]

    def is_collision(self):
        ret = False
        now_pos_x = self.now_pos_x
        now_pos_y = self.now_pos_y
        now_vec = self.now_vec
        # 向いている方向に進む
        if now_vec == 0:
            "北に進む"
            now_pos_y -= 1
        elif now_vec == 1:
            "東に進む"
            now_pos_x += 1
        elif now_vec == 2:
            "南に進む"
            now_pos_y += 1
        elif now_vec == 3:
            "西に進む"
            now_pos_x -= 1

        if self.data[now_pos_y][now_pos_x] == 1:
            ret = True
        return ret

    def turn_right(self):
        self.now_vec += 1
        if self.now_vec > 3:
            self.now_vec = 0
        return {"mouse_pos_x": self.now_pos_x, "mouse_pos_y": self.now_pos_y, "mouse_vec": self.now_vec}

    def turn_left(self):
        self.now_vec -= 1
        if self.now_vec < 0:
            self.now_vec = 3
        return {"mouse_pos_x": self.now_pos_x, "mouse_pos_y": self.now_pos_y, "mouse_vec": self.now_vec}

    def go_straight(self):
        if self.is_collision():
            raise Exception("collision")

        # 向いている方向に進む
        if self.now_vec == 0:
            "北に進む"
            self.now_pos_y -= 2
        elif self.now_vec == 1:
            "東に進む"
            self.now_pos_x += 2
        elif self.now_vec == 2:
            "南に進む"
            self.now_pos_y += 2
        elif self.now_vec == 3:
            "西に進む"
            self.now_pos_x -= 2

        return {"mouse_pos_x": self.now_pos_x, "mouse_pos_y": self.now_pos_y, "mouse_vec": self.now_vec}