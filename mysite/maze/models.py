from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Maze(models.Model):

    maze_size_x = models.IntegerField(default=0,
                                      null=False,
                                      verbose_name="マップサイズのX幅",
                                      help_text="マップサイズのX幅")

    maze_size_y = models.IntegerField(default=0,
                                      null=False,
                                      verbose_name="マップサイズのY幅",
                                      help_text="マップサイズのY幅")

    start_pos_x = models.IntegerField(default=0,
                                      null=False,
                                      verbose_name="開始位置のX",
                                      help_text="開始位置のX")

    start_pos_y = models.IntegerField(default=0,
                                      null=False,
                                      verbose_name="開始位置のY",
                                      help_text="開始位置のY")

    goal_pos_x = models.IntegerField(default=0,
                                      null=False,
                                      verbose_name="終了位置のX",
                                      help_text="終了位置のX")

    goal_pos_y = models.IntegerField(default=0,
                                      null=False,
                                      verbose_name="終了位置のY",
                                      help_text="終了位置のY")

    turn = models.IntegerField(default=5,
                               verbose_name="ターン数",
                               help_text="ターン数")

    step = models.IntegerField(default=50,
                               verbose_name="ステップ数",
                               help_text="ステップ数")

    maze_file_name = models.CharField(max_length=260,
                                      null=False,
                                      verbose_name="ステージファイル名",
                                      help_text="ステージファイル名")

    maze_img_file = models.CharField(max_length=260,
                                     null=False,
                                     verbose_name="イメージファイル名",
                                     help_text="イメージファイル名")

    level = models.IntegerField(default=1,
                                verbose_name="問題のレベル",
                                help_text="問題のレベル")

    def __str__(self):
        return self.maze_name


class ApiKeys(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=False,
                             verbose_name="ユーザ名",
                             help_text="ユーザ名")

    api_key = models.CharField(max_length=260,
                               null=False,
                               verbose_name="APIキー",
                               help_text="APIキー")

    last_login = models.DateTimeField(auto_now=True,
                                      null=True,
                                      verbose_name="最終アクセス時刻")

    def __str__(self):
        return self.api_key


class PracticeHistory(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=False,
                             verbose_name="ユーザ名",
                             help_text="ユーザ名")

    token = models.CharField(max_length=260,
                             null=False,
                             verbose_name="トークン",
                             help_text="トークン")

    maze = models.ForeignKey(Maze,
                             on_delete=models.CASCADE,
                             null=False,
                             verbose_name="迷路",
                             help_text="迷路")

    turn = models.IntegerField(default=0,
                               verbose_name="ターン",
                               help_text="ターン")

    step = models.IntegerField(default=0,
                               verbose_name="ステップ",
                               help_text="ステップ")

    action = models.IntegerField(default=0,
                                 verbose_name="行動",
                                 help_text="行動")

    pos_x = models.IntegerField(default=0,
                                verbose_name="現在位置のX座標",
                                help_text="現在位置のX座標")

    pos_y = models.IntegerField(default=0,
                                verbose_name="現在位置のY座標",
                                help_text="現在位置のY座標")

    vec = models.IntegerField(default=0,
                              verbose_name="向き",
                              help_text="向き")


    action_date = models.DateTimeField(auto_now_add=True,
                                       null=True,
                                       verbose_name="操作時刻")
