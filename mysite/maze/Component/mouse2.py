# coding:UTF-8
import os
import json
import traceback
from django.db.models import Max
from maze.models import Maze
from maze.models import PracticeHistory
from maze.models import TokenStatus

class MouseError(Exception):
    pass

class Mouse2(object):
    def __init__(self, token):
        max_id = PracticeHistory.objects.filter(token=token).aggregate(Max('id'))
        history = PracticeHistory.objects.get(id=max_id["id__max"])
        map_id = history.maze_id
        self.maze = Maze.objects.get(id=map_id)
        json_file = self.maze.maze_file_name
        self.maze_max_turn = self.maze.turn
        self.maze_max_step = self.maze.step
        self.goal_pos_x = self.maze.goal_pos_x
        self.goal_pos_y = self.maze.goal_pos_y
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
        self.step = history.step
        self.action = history.action

    def is_turn_over(self):
        print("{}-{}".format(self.turn, self.maze_max_turn))
        ret = False
        if self.turn >= self.maze_max_turn:
            ret = True
        return ret

    def is_step_over(self):
        print("{}-{}".format(self.step, self.maze_max_step))
        ret = False
        if self.step >= self.maze_max_step:
            ret = True
        return ret

    def is_last_turn(self):
        if self.turn == self.maze_max_turn - 1:
            return True
        return False

    def set_next_turn(self):
        self.step = 0
        self.turn += 1
        self.now_pos_x = self.maze.start_pos_x
        self.now_pos_y = self.maze.start_pos_y
        self.now_vec = 0

    def save_history(self):
        if self.step >= self.maze.step:
            self.step = self.maze.step
        if self.turn >= self.maze_max_turn:
            self.turn = self.maze_max_turn

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
        self.step += 1
        if self.is_step_over():
            raise MouseError("step over", 1)
        if self.is_turn_over():
            raise MouseError("turn over", 2)

        self.now_vec += 1
        if self.now_vec > 3:
            self.now_vec = 0
        return {"mouse_pos_x": self.now_pos_x, "mouse_pos_y": self.now_pos_y, "mouse_vec": self.now_vec}

    def turn_left(self):
        self.step += 1
        if self.is_step_over():
            raise MouseError("step over", 1)
        if self.is_turn_over():
            raise MouseError("turn over", 2)

        self.now_vec -= 1
        if self.now_vec < 0:
            self.now_vec = 3
        return {"mouse_pos_x": self.now_pos_x, "mouse_pos_y": self.now_pos_y, "mouse_vec": self.now_vec}

    def go_straight(self):
        self.step += 1
        if self.is_step_over():
            raise MouseError("step over", 1)
        if self.is_turn_over():
            raise MouseError("turn over", 2)
        if self.is_collision():
            raise MouseError("collision", 3)

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

    def is_goal(self):
        ret = False
        if self.now_pos_x == self.goal_pos_x and self.now_pos_y == self.goal_pos_y:
            ret = True
        return ret

    def game_clear(self):
        ret = True
        try:
            token_record = TokenStatus.objects.get(token=self.token)
            token_record.status = 2
            token_record.save()
        except Exception as e:
            traceback.print_exc()
            ret = False
        return ret

    def game_over(self):
        try:
            token_status = TokenStatus.objects.get(token=self.token)
            token_status.status = 1
            token_status.save()
        except Exception as e:
            traceback.print_exc()