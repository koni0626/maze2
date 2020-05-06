# coding:UTF-8
import os
import json


class Mouse(object):
    def __init__(self, session, data):
        self.now_pos_x = session["mouse_pos_x"]
        self.now_pos_y = session["mouse_pos_y"]
        self.now_vec = session["mouse_vec"]
        self.memory = session["memory"]
        self.img_list = ["/maze_static/icon/icon_north.png",
                         "/maze_static/icon/icon_east.png",
                         "/maze_static/icon/icon_south.png",
                         "/maze_static/icon/icon_west.png"]
        self.icon = self.img_list[self.now_vec]
        self.data = data


    def get_mouse_icon(self, vec):
        return self.img_list[vec]

    def get_sensor(self):
        if self.now_vec == 0:
            # 北
            left = self.data[self.now_pos_y][self.now_pos_x - 1]
            front = self.data[self.now_pos_y - 1][self.now_pos_x]
            right = self.data[self.now_pos_y][self.now_pos_x + 1]
            self.memory[self.now_pos_y][self.now_pos_x - 1] = 1
            self.memory[self.now_pos_y - 1][self.now_pos_x] = 1
            self.memory[self.now_pos_y][self.now_pos_x + 1] = 1
            self.memory[self.now_pos_y][self.now_pos_x] = 1

        elif self.now_vec == 1:
            # 東
            left = self.data[self.now_pos_y - 1][self.now_pos_x]
            front = self.data[self.now_pos_y][self.now_pos_x + 1]
            right = self.data[self.now_pos_y + 1][self.now_pos_x]
            self.memory[self.now_pos_y - 1][self.now_pos_x] = 1
            self.memory[self.now_pos_y][self.now_pos_x + 1] = 1
            self.memory[self.now_pos_y + 1][self.now_pos_x] = 1
            self.memory[self.now_pos_y][self.now_pos_x] = 1

        elif self.now_vec == 2:
            # 南
            left = self.data[self.now_pos_y][self.now_pos_x + 1]
            front = self.data[self.now_pos_y + 1][self.now_pos_x]
            right = self.data[self.now_pos_y][self.now_pos_x - 1]
            self.memory[self.now_pos_y][self.now_pos_x + 1] = 1
            self.memory[self.now_pos_y + 1][self.now_pos_x] = 1
            self.memory[self.now_pos_y][self.now_pos_x - 1] = 1
            self.memory[self.now_pos_y][self.now_pos_x] = 1
        else:
            # 西
            left = self.data[self.now_pos_y + 1][self.now_pos_x]
            front = self.data[self.now_pos_y][self.now_pos_x - 1]
            right = self.data[self.now_pos_y - 1][self.now_pos_x]
            self.memory[self.now_pos_y + 1][self.now_pos_x] = 1
            self.memory[self.now_pos_y][self.now_pos_x - 1] = 1
            self.memory[self.now_pos_y - 1][self.now_pos_x] = 1
            self.memory[self.now_pos_y][self.now_pos_x] = 1
        if left != 1:
            left = 0
        if front != 1:
            front = 0
        if right != 1:
            right = 0

        return (left, front, right), self.memory

    def is_collision(self, action):
        ret = False
        now_pos_x = self.now_pos_x
        now_pos_y = self.now_pos_y
        now_vec = self.now_vec
        if action == 1:
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
        elif action == 2:
            "北を向く"
            now_vec = 0
        elif action == 3:
            "東を向く"
            now_vec = 1
        elif action == 4:
            "南を向く"
            now_vec = 2
        elif action == 5:
            "西を向く"
            now_vec = 3
        else:
            # 0 初期化
            pass

        if self.data[now_pos_y][now_pos_x] == 1:
            ret = True
        return ret

    def set_action(self, action):
        if self.is_collision(action):
            raise Exception("collision")

        if action == 1:
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
        elif action == 2:
            "北を向く"
            self.now_vec = 0
        elif action == 3:
            "東を向く"
            self.now_vec = 1
        elif action == 4:
            "南を向く"
            self.now_vec = 2
        elif action == 5:
            "西を向く"
            self.now_vec = 3
        else:
            # 0 初期化
            pass

        self.icon = self.img_list[self.now_vec]

        return {"mouse_pos_x": self.now_pos_x, "mouse_pos_y": self.now_pos_y, "mouse_vec": self.now_vec, "mouse_icon": self.icon}