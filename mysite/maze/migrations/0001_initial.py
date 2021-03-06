# Generated by Django 3.0.5 on 2020-05-03 13:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Maze',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maze_size_x', models.IntegerField(default=0, help_text='マップサイズのX幅', verbose_name='マップサイズのX幅')),
                ('maze_size_y', models.IntegerField(default=0, help_text='マップサイズのY幅', verbose_name='マップサイズのY幅')),
                ('start_pos_x', models.IntegerField(default=0, help_text='開始位置のX', verbose_name='開始位置のX')),
                ('start_pos_y', models.IntegerField(default=0, help_text='開始位置のY', verbose_name='開始位置のY')),
                ('goal_pos_x', models.IntegerField(default=0, help_text='終了位置のX', verbose_name='終了位置のX')),
                ('goal_pos_y', models.IntegerField(default=0, help_text='終了位置のY', verbose_name='終了位置のY')),
                ('turn', models.IntegerField(default=5, help_text='ターン数', verbose_name='ターン数')),
                ('step', models.IntegerField(default=50, help_text='ステップ数', verbose_name='ステップ数')),
                ('maze_file_name', models.CharField(help_text='ステージファイル名', max_length=260, verbose_name='ステージファイル名')),
                ('maze_img_file', models.CharField(help_text='イメージファイル名', max_length=260, verbose_name='イメージファイル名')),
            ],
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result_file_name', models.CharField(help_text='棋譜ファイル名', max_length=260, verbose_name='棋譜ファイル名')),
                ('stage', models.ForeignKey(help_text='迷路名', on_delete=django.db.models.deletion.CASCADE, to='maze.Maze', verbose_name='迷路名')),
                ('user', models.ForeignKey(help_text='ユーザ名', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザ名')),
            ],
        ),
    ]
