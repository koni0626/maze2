# coding:UTF-8
# 練習用迷路作成コマンド
import os
import sqlite3
import uuid
import json
import glob
import cv2
import numpy as np

from maze.Component.maze import MazeManager

DB_PATH = "db.sqlite3"
CREATE_MAZE_NUM = 100
MEDIA_ROOT = r"./media"

if __name__ == '__main__':
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    try:
        sql = 'DROP TABLE maze_maze;'
        c.execute(sql)
    except:
        pass

    sql = 'CREATE TABLE "maze_maze" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "maze_size_x" integer NOT NULL, "maze_size_y" integer NOT NULL, "start_pos_x" integer NOT NULL, "start_pos_y" integer NOT NULL, "goal_pos_x" integer NOT NULL, "goal_pos_y" integer NOT NULL, "turn" integer NOT NULL, "step" integer NOT NULL, "maze_file_name" varchar(260) NOT NULL, "maze_img_file" varchar(260) NOT NULL, "level" integer NOT NULL)'
    c.execute(sql)

    maze_size = (33, 33)
    start_pos = (1, 31)
    goal_pos = (17, 17)
    turn = 5
    step = 50

    output_dir = os.path.join(MEDIA_ROOT, "maze")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    json_list = glob.glob(os.path.join(output_dir, "*.json"))
    for file in json_list:
        print("delete {}".format(file))
        os.remove(file)

    png_list = glob.glob(os.path.join(output_dir, "*.png"))
    for file in png_list:
        print("delete {}".format(file))
        os.remove(file)


    for i in range(9):
        maze_data = MazeManager(maze_size, start_pos, goal_pos)
        file_id = str(uuid.uuid4())
        db_maze_file = file_id + ".json"
        db_img_file = file_id + ".png"
        maze_file = os.path.join(output_dir, file_id + ".json")
        img_file = os.path.join(output_dir, file_id + ".png")
        with open(maze_file, "w") as f:
            json.dump(maze_data.get_list(), f)
        os.chmod(maze_file, 0o666)

        png = maze_data.image_rate(32)
       # png = cv2.resize(png, (480, 270), interpolation=cv2.INTER_CUBIC)
       # png = cv2.resize(png, (960, 540), interpolation=cv2.INTER_CUBIC)
       # png = cv2.resize(png, (1920, 1080), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(img_file, png)

        sql = "insert into maze_maze (maze_size_x, maze_size_y, start_pos_x, start_pos_y, goal_pos_x, goal_pos_y, turn, step, maze_file_name, maze_img_file, level) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        c.execute(sql, (maze_size[0], maze_size[1], start_pos[0], start_pos[1], goal_pos[0], goal_pos[1], turn, step, db_maze_file, db_img_file, 1))
        print("create {}".format(maze_file))

    conn.commit()



