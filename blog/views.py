import os
import shutil
import json
import mimetypes
from random import shuffle
from PIL import Image, ImageDraw, ImageFont
from zipfile import ZipFile

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
from users.models import User
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader
from django.http import FileResponse



def home(request):
    current_user = request.user.groups.filter(name='орда').exists()
    context = {
        'posts': Post.objects.all(),
        'allow': current_user,
    }
    return render(request, 'blog/home.html', context)


def my_home(request):
    current_user = request.user.groups.filter(name='орда').exists()
    context = {
        'posts': Post.objects.filter(author_id=request.user.id),
        'allow': current_user,
    }
    return render(request, 'blog/home.html', context)


def rating(request):
    current_user = request.user.groups.filter(name='орда').exists()
    commands = [[0, "school 32", 4, 6, 40], [0, "school 43", 8, 2, 80], [0, "school 22", 7, 3, 70], [0, "school 67", 6, 4, 60]]
    commands.sort(key=lambda x: x[-1], reverse=True)
    count = 1
    for i in range(len(commands)):
        commands[i][0] = count
        count += 1
    context = {
        'posts': Post.objects.filter(author_id=request.user.id),
        'allow': current_user,
        'commands': commands,
    }
    return render(request, 'blog/rating.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def schedule(request, pk):
    posts = Post.objects.filter(id=pk)
    if os.path.exists(f"{posts[0].title}/команды_{posts[0].title}.txt"):
        com_file = open(f"{posts[0].title}/команды_{posts[0].title}.txt", "r", encoding="utf-8")
        if len(com_file.read()) == 0:
            com_file = open(f"{posts[0].title}/команды_{posts[0].title}.txt", "w", encoding="utf-8")
            if str(posts[0].content.replace("\n", "")) != "нет":
                com_file.write(str(posts[0].content.replace("\n", "")))
            com_file.close()
    else:
        if str(posts[0].content.replace("\n", "")) != "нет":
            com_file = open(f"{posts[0].title}/команды_{posts[0].title}.txt", "w", encoding="utf-8")
            com_file.write(str(posts[0].content.replace("\n", "")))
            com_file.close()
        else:
            com_file = open(f"{posts[0].title}/команды_{posts[0].title}.txt", "w", encoding="utf-8")
            com_file.close()

        
    com_file = open(f"{posts[0].title}/команды_{posts[0].title}.txt", "r", encoding="utf-8")
    com_file.seek(0)
    commands_dict = {}
    if com_file.read().lower() != "нет":
        com_file = open(f"{posts[0].title}/команды_{posts[0].title}.txt", "r", encoding="utf-8")
        com_file.seek(0)
        file = open(f"{posts[0].title}/{posts[0].title}_тур1.txt", "r", encoding="utf-8")
        if len(file.read()) == 0:
            file = open(f"{posts[0].title}/{posts[0].title}_тур1.txt", "w", encoding="utf-8")
            num = 1
            title = "КОМАНДЫ" + " " * 35 + "|СЧЁТ"
            file.write(title + "\n")
            file.write("-" * len(title) + "\n")
            commands = com_file.readlines()
            shuffle(commands)
            for command in commands:
                file.write(command.replace("\n", "").ljust(35) + "\n")
                commands_dict[command.replace("\n", "").strip()] = []
                if num % 2 == 0:
                    file.write("-" * len(title) + "\n")
                num += 1
            if num % 2 == 0:
                file.write("Пустышка".ljust(35) + "\n")
                file.write("-" * len(title) + "\n")
            file.close()
    com_file.close()
    file = open(f"{posts[0].title}/{posts[0].title}_тур1.txt", "r", encoding="utf-8")
    file_count = open(f"{posts[0].title}/{posts[0].title}_туры.txt", "r", encoding="utf-8")
    count_tour = file_count.read().strip()
    com_1 = []
    com2_1, com2_2 = [], []
    com3_1, com3_2, com3_3 = [], [], []
    com4_1, com4_2, com4_3, com4_4 = [], [], [], []
    com5_1, com5_2, com5_3, com5_4, com5_5 = [], [], [], [], []
    com6_1, com6_2, com6_3, com6_4, com6_5, com6_6 = [], [], [], [], [], []
    com7_1, com7_2, com7_3, com7_4, com7_5, com7_6, com7_7 = [], [], [], [], [], [], []
    com8_1, com8_2, com8_3, com8_4, com8_5, com8_6, com8_7, com8_8 = [], [], [], [], [], [], [], []
    com9_1, com9_2, com9_3, com9_4, com9_5, com9_6, com9_7, com9_8, com9_9 = [], [], [], [], [], [], [], [], []

    l = []
    for line in file.readlines()[2:]:
        line = line.replace("\n", "")
        if line.count('----------') > 0:
            com_1.append(l)
            l = []
        else:
            l.append(line)

    count_tour = int(count_tour)
    if count_tour > 1:
        file_res = open(f"{posts[0].title}/результат_{count_tour - 1}_{posts[0].title}.txt", "r", encoding="utf-8")
    else:
        file_res = open(f"{posts[0].title}/результат_{count_tour}_{posts[0].title}.txt", "r", encoding="utf-8")

    file_res.seek(0)
    com_d = {}
    for i in range(0, 10):
        com_d[i] = []
    for line in file_res.readlines():
        if len(line.replace("\n", "")) != 0:
            com = line.split(": ")[0]
            win = int(line.split(": ")[1])
            com_d[win].append(com)
    file_count.close()
    file_res.close()

    match count_tour:
        case 9:
            file = open(f"{posts[0].title}/{posts[0].title}_тур2.txt", "r", encoding="utf-8")

            com_2 = []
            for line in file.readlines():
                if line.count("-") < 3 and line.count("КОМАНДЫ") == 0:
                    com_2.append(line)

            for i in range(0, len(com_2) // 2 - 1, 2):
                com2_1.append([com_2[i], com_2[i + 1]])

            for i in range(len(com_2) // 2, len(com_2) - 1, 2):
                com2_2.append([com_2[i], com_2[i + 1]])
            file.close()
            file_res = open(f"{posts[0].title}/результат_2_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)
            file_res.close()
            file_count = open(f"{posts[0].title}/{posts[0].title}_счёт_3.txt", "r", encoding="utf-8")
            count_list = file_count.read().split()
            file_count.close()
            p = 0

            for i in range(0, len(com_d[2]) - 1, 2):
                com3_1.append([com_d[2][i] + " " + count_list[p], com_d[2][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[1]) - 1, 2):
                com3_2.append([com_d[1][i] + " " + count_list[p], com_d[1][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[0]) - 1, 2):
                com3_3.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2

            file_res = open(f"{posts[0].title}/результат_3_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            file_res.close()
            file_count = open(f"{posts[0].title}/{posts[0].title}_счёт_4.txt", "r", encoding="utf-8")
            count_list = file_count.read().split()
            p = 0

            for i in range(0, len(com_d[3]) - 1, 2):
                com4_1.append([com_d[3][i] + " " + count_list[p], com_d[3][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[2]) - 1, 2):
                com4_2.append([com_d[2][i] + " " + count_list[p], com_d[2][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[1]) - 1, 2):
                com4_3.append([com_d[1][i] + " " + count_list[p], com_d[1][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[0]) - 1, 2):
                com4_4.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2

            file_count.close()
            file_res = open(f"{posts[0].title}/результат_4_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            file_res.close()
            file_res = open(f"{posts[0].title}/результат_4_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            file_count = open(f"{posts[0].title}/{posts[0].title}_счёт_5.txt", "r", encoding="utf-8")
            count_list = file_count.read().split()
            p = 0

            for i in range(0, len(com_d[4]) - 1, 2):
                com5_1.append([com_d[4][i] + " " + count_list[p], com_d[4][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[3]) - 1, 2):
                com5_2.append([com_d[3][i] + " " + count_list[p], com_d[3][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[2]) - 1, 2):
                com5_3.append([com_d[2][i] + " " + count_list[p], com_d[2][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[1]) - 1, 2):
                com5_4.append([com_d[1][i] + " " + count_list[p], com_d[1][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[0]) - 1, 2):
                com5_5.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2

            file_res = open(f"{posts[0].title}/результат_5_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            file_count = open(f"{posts[0].title}/{posts[0].title}_счёт_6.txt", "r", encoding="utf-8")
            count_list = file_count.read().split()
            p = 0

            for i in range(0, len(com_d[4]) - 1, 2):
                com6_1.append([com_d[4][i] + " " + count_list[p], com_d[4][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[3]) - 1, 2):
                com6_2.append([com_d[3][i] + " " + count_list[p], com_d[3][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[2]) - 1, 2):
                com6_3.append([com_d[2][i] + " " + count_list[p], com_d[2][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[1]) - 1, 2):
                com6_4.append([com_d[1][i] + " " + count_list[p], com_d[1][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[0]) - 1, 2):
                com6_5.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2

            p -= 1
            for i in range(0, len(com_d[0]) - 1, 2):
                com6_6.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2

            file_res = open(f"{posts[0].title}/результат_6_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            file_count = open(f"{posts[0].title}/{posts[0].title}_счёт_7.txt", "r", encoding="utf-8")
            count_list = file_count.read().split()
            p = 0

            for i in range(0, len(com_d[4]) - 1, 2):
                com7_1.append([com_d[4][i] + " " + count_list[p], com_d[4][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[3]) - 1, 2):
                com7_2.append([com_d[3][i] + " " + count_list[p], com_d[3][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[2]) - 1, 2):
                com7_3.append([com_d[2][i] + " " + count_list[p], com_d[2][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[1]) - 1, 2):
                com7_4.append([com_d[1][i] + " " + count_list[p], com_d[1][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[0]) - 1, 2):
                com7_5.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[0]) - 1, 2):
                com7_6.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2

            p -= 1
            for i in range(0, len(com_d[0]) - 1, 2):
                com7_7.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2

            file_res = open(f"{posts[0].title}/результат_7_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            file_count = open(f"{posts[0].title}/{posts[0].title}_счёт_8.txt", "r", encoding="utf-8")
            count_list = file_count.read().split()
            p = 0

            for i in range(0, len(com_d[7]) - 1, 2):
                com8_1.append([com_d[7][i] + " " + count_list[p], com_d[7][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[6]) - 1, 2):
                com8_2.append([com_d[6][i] + " " + count_list[p], com_d[6][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[5]) - 1, 2):
                com8_3.append([com_d[5][i] + " " + count_list[p], com_d[5][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[4]) - 1, 2):
                com8_4.append([com_d[4][i] + " " + count_list[p], com_d[4][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[3]) - 1, 2):
                com8_5.append([com_d[3][i] + " " + count_list[p], com_d[3][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[2]) - 1, 2):
                com8_6.append([com_d[2][i] + " " + count_list[p], com_d[2][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[1]) - 1, 2):
                com8_7.append([com_d[1][i] + " " + count_list[p], com_d[1][i + 1] + " " + count_list[p + 1]])
                p += 2

            p -= 1
            for i in range(0, len(com_d[0]) - 1, 2):
                com8_8.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2

            file_res = open(f"{posts[0].title}/результат_8_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            fp = open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "r", encoding="utf-8")
            commands_dict = json.load(fp)

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[8]) - 1, 2):
                if com_d[8][i + 1] not in commands_dict[com_d[8][i]]:
                    com9_1.append([com_d[8][i], com_d[8][i + 1]])
                else:
                    empty_com_1.append(com_d[8][i])
                    empty_com_2.append(com_d[8][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com9_1.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[7]) - 1, 2):
                if com_d[7][i + 1] not in commands_dict[com_d[7][i]]:
                    com9_2.append([com_d[7][i], com_d[7][i + 1]])
                else:
                    empty_com_1.append(com_d[7][i])
                    empty_com_2.append(com_d[7][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com9_2.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[6]) - 1, 2):
                if com_d[6][i + 1] not in commands_dict[com_d[6][i]]:
                    com9_3.append([com_d[6][i], com_d[6][i + 1]])
                else:
                    empty_com_1.append(com_d[6][i])
                    empty_com_2.append(com_d[6][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com9_3.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[5]) - 1, 2):
                if com_d[5][i + 1] not in commands_dict[com_d[5][i]]:
                    com9_4.append([com_d[5][i], com_d[5][i + 1]])
                else:
                    empty_com_1.append(com_d[5][i])
                    empty_com_2.append(com_d[5][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com9_4.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[4]) - 1, 2):
                if com_d[4][i + 1] not in commands_dict[com_d[4][i]]:
                    com9_5.append([com_d[4][i], com_d[4][i + 1]])
                else:
                    empty_com_1.append(com_d[4][i])
                    empty_com_2.append(com_d[4][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com9_5.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[3]) - 1, 2):
                if com_d[3][i + 1] not in commands_dict[com_d[3][i]]:
                    com9_6.append([com_d[3][i], com_d[3][i + 1]])
                else:
                    empty_com_1.append(com_d[3][i])
                    empty_com_2.append(com_d[3][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com9_6.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[2]) - 1, 2):
                if com_d[2][i + 1] not in commands_dict[com_d[2][i]]:
                    com9_7.append([com_d[2][i], com_d[2][i + 1]])
                else:
                    empty_com_1.append(com_d[2][i])
                    empty_com_2.append(com_d[2][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com9_7.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[1]) - 1, 2):
                if com_d[1][i + 1] not in commands_dict[com_d[1][i]]:
                    com9_8.append([com_d[1][i], com_d[1][i + 1]])
                else:
                    empty_com_1.append(com_d[1][i])
                    empty_com_2.append(com_d[1][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com9_8.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[0]) - 1, 2):
                if com_d[0][i + 1] not in commands_dict[com_d[0][i]]:
                    com9_9.append([com_d[0][i], com_d[0][i + 1]])
                else:
                    empty_com_1.append(com_d[0][i])
                    empty_com_2.append(com_d[0][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com9_9.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            if len(com_d[0]) % 2 != 0:
                com9_9.append([com_d[0][-1], "Пустышка"])

            file = open(f"{posts[0].title}/{posts[0].title}_тур9.txt", "r", encoding="utf-8")
            if len(file.read()) == 0:
                file = open(f"{posts[0].title}/{posts[0].title}_тур9.txt", "w", encoding="utf-8")
                num = 1
                title = "КОМАНДЫ" + " " * 35 + "|СЧЁТ"
                file.write(title + "\n")
                file.write("-" * len(title) + "\n")
                for com in com9_1:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com9_2:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com9_3:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com9_4:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com9_5:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com9_6:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com9_7:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com9_8:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com9_9:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                file.close()


            file = open(f"{posts[0].title}/{posts[0].title}_тур9.txt", "r", encoding="utf-8")
            if len(file.read()) == 0:
                file = open(f"{posts[0].title}/{posts[0].title}_тур9.txt", "w", encoding="utf-8")
                num = 1
                title = "КОМАНДЫ" + " " * 35 + "|СЧЁТ"
                file.write(title + "\n")
                file.write("-" * len(title) + "\n")
                for com in com9_1:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com9_2:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com9_3:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com9_4:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com9_5:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com9_6:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com9_7:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com9_8:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com9_9:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                file.close()

            file_res = open(f"{posts[0].title}/результат_9_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            fp = open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "r", encoding="utf-8")
            commands_dict = json.load(fp)

            with open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "w", encoding="utf-8") as fp:
                s = json.dumps(commands_dict, ensure_ascii=False)
                fp.write(s)

            return render(request, 'blog/sсhedule.html',
                          {'title': 'Орда', 'name': posts[0].title, 'count_tour': int(count_tour),
                           'tour1': com_1,
                           'tour2_1': com2_1, 'tour2_2': com2_2,
                           'tour3_1': com3_1, 'tour3_2': com3_2, 'tour3_3': com3_3,
                           'tour4_1': com4_1, 'tour4_2': com4_2, 'tour4_3': com4_3, 'tour4_4': com4_4,
                           'tour5_1': com5_1, 'tour5_2': com5_2, 'tour5_3': com5_3, 'tour5_4': com5_4, 'tour5_5': com5_5,
                           'tour6_1': com6_1, 'tour6_2': com6_2, 'tour6_3': com6_3, 'tour6_4': com6_4, 'tour6_5': com6_5,
                           'tour6_6': com6_6,
                           'tour7_1': com7_1, 'tour7_2': com7_2, 'tour7_3': com7_3, 'tour7_4': com7_4, 'tour7_5': com7_5,
                           'tour7_6': com7_6, 'tour7_7': com7_7,
                           'tour8_1': com8_1, 'tour8_2': com8_2, 'tour8_3': com8_3, 'tour8_4': com8_4, 'tour8_5': com8_5,'tour8_6': com8_6, 'tour8_7': com8_7, 'tour8_8': com8_8,
                           'tour9_1': com9_1, 'tour9_2': com9_2, 'tour9_3': com9_3, 'tour9_4': com9_4, 'tour9_5': com9_5, 'tour9_6': com9_6, 'tour9_7': com9_7, 'tour9_8': com9_8, 'tour9_9': com9_9})

        case 8:
            file = open(f"{posts[0].title}/{posts[0].title}_тур2.txt", "r", encoding="utf-8")

            com_2 = []
            for line in file.readlines():
                if line.count("-") < 3 and line.count("КОМАНДЫ") == 0:
                    com_2.append(line)

            for i in range(0, len(com_2) // 2 - 1, 2):
                com2_1.append([com_2[i], com_2[i + 1]])

            for i in range(len(com_2) // 2, len(com_2) - 1, 2):
                com2_2.append([com_2[i], com_2[i + 1]])
            file.close()
            file_res = open(f"{posts[0].title}/результат_2_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)
            file_res.close()
            file_count = open(f"{posts[0].title}/{posts[0].title}_счёт_3.txt", "r", encoding="utf-8")
            count_list = file_count.read().split()
            file_count.close()
            p = 0

            for i in range(0, len(com_d[2]) - 1, 2):
                com3_1.append([com_d[2][i] + " " + count_list[p], com_d[2][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[1]) - 1, 2):
                com3_2.append([com_d[1][i] + " " + count_list[p], com_d[1][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[0]) - 1, 2):
                com3_3.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2

            file_res = open(f"{posts[0].title}/результат_3_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            file_res.close()
            file_count = open(f"{posts[0].title}/{posts[0].title}_счёт_4.txt", "r", encoding="utf-8")
            count_list = file_count.read().split()
            p = 0

            for i in range(0, len(com_d[3]) - 1, 2):
                com4_1.append([com_d[3][i] + " " + count_list[p], com_d[3][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[2]) - 1, 2):
                com4_2.append([com_d[2][i] + " " + count_list[p], com_d[2][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[1]) - 1, 2):
                com4_3.append([com_d[1][i] + " " + count_list[p], com_d[1][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[0]) - 1, 2):
                com4_4.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2

            file_count.close()
            file_res = open(f"{posts[0].title}/результат_4_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            file_res.close()
            file_res = open(f"{posts[0].title}/результат_4_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            file_count = open(f"{posts[0].title}/{posts[0].title}_счёт_5.txt", "r", encoding="utf-8")
            count_list = file_count.read().split()
            p = 0

            for i in range(0, len(com_d[4]) - 1, 2):
                com5_1.append([com_d[4][i] + " " + count_list[p], com_d[4][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[3]) - 1, 2):
                com5_2.append([com_d[3][i] + " " + count_list[p], com_d[3][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[2]) - 1, 2):
                com5_3.append([com_d[2][i] + " " + count_list[p], com_d[2][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[1]) - 1, 2):
                com5_4.append([com_d[1][i] + " " + count_list[p], com_d[1][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[0]) - 1, 2):
                com5_5.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2

            file_res = open(f"{posts[0].title}/результат_5_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            file_count = open(f"{posts[0].title}/{posts[0].title}_счёт_6.txt", "r", encoding="utf-8")
            count_list = file_count.read().split()
            p = 0

            for i in range(0, len(com_d[4]) - 1, 2):
                com6_1.append([com_d[4][i] + " " + count_list[p], com_d[4][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[3]) - 1, 2):
                com6_2.append([com_d[3][i] + " " + count_list[p], com_d[3][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[2]) - 1, 2):
                com6_3.append([com_d[2][i] + " " + count_list[p], com_d[2][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[1]) - 1, 2):
                com6_4.append([com_d[1][i] + " " + count_list[p], com_d[1][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[0]) - 1, 2):
                com6_5.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2

            p -= 1
            for i in range(0, len(com_d[0]) - 1, 2):
                com6_6.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2

            file_res = open(f"{posts[0].title}/результат_6_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            file_count = open(f"{posts[0].title}/{posts[0].title}_счёт_7.txt", "r", encoding="utf-8")
            count_list = file_count.read().split()
            p = 0

            for i in range(0, len(com_d[6]) - 1, 2):
                com7_1.append([com_d[6][i] + " " + count_list[p], com_d[6][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[5]) - 1, 2):
                com7_2.append([com_d[5][i] + " " + count_list[p], com_d[5][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[4]) - 1, 2):
                com7_3.append([com_d[4][i] + " " + count_list[p], com_d[4][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[3]) - 1, 2):
                com7_4.append([com_d[3][i] + " " + count_list[p], com_d[3][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[2]) - 1, 2):
                com7_5.append([com_d[2][i] + " " + count_list[p], com_d[2][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[1]) - 1, 2):
                com7_6.append([com_d[1][i] + " " + count_list[p], com_d[1][i + 1] + " " + count_list[p + 1]])
                p += 2

            p -= 1
            for i in range(0, len(com_d[0]) - 1, 2):
                com7_7.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2

            file_res = open(f"{posts[0].title}/результат_7_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)



            fp = open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "r", encoding="utf-8")
            commands_dict = json.load(fp)

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[7]) - 1, 2):
                if com_d[7][i + 1] not in commands_dict[com_d[7][i]]:
                    com8_1.append([com_d[7][i], com_d[7][i + 1]])
                else:
                    empty_com_1.append(com_d[7][i])
                    empty_com_2.append(com_d[7][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com8_1.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[6]) - 1, 2):
                if com_d[6][i + 1] not in commands_dict[com_d[6][i]]:
                    com8_2.append([com_d[6][i], com_d[6][i + 1]])
                else:
                    empty_com_1.append(com_d[6][i])
                    empty_com_2.append(com_d[6][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com8_2.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[5]) - 1, 2):
                if com_d[5][i + 1] not in commands_dict[com_d[5][i]]:
                    com8_3.append([com_d[5][i], com_d[5][i + 1]])
                else:
                    empty_com_1.append(com_d[5][i])
                    empty_com_2.append(com_d[5][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com8_3.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break


            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[4]) - 1, 2):
                if com_d[4][i + 1] not in commands_dict[com_d[4][i]]:
                    com8_4.append([com_d[4][i], com_d[4][i + 1]])
                else:
                    empty_com_1.append(com_d[4][i])
                    empty_com_2.append(com_d[4][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com8_4.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[3]) - 1, 2):
                if com_d[3][i + 1] not in commands_dict[com_d[3][i]]:
                    com8_5.append([com_d[3][i], com_d[3][i + 1]])
                else:
                    empty_com_1.append(com_d[3][i])
                    empty_com_2.append(com_d[3][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com8_5.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[2]) - 1, 2):
                if com_d[2][i + 1] not in commands_dict[com_d[2][i]]:
                    com8_6.append([com_d[2][i], com_d[2][i + 1]])
                else:
                    empty_com_1.append(com_d[2][i])
                    empty_com_2.append(com_d[2][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com8_6.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[1]) - 1, 2):
                if com_d[1][i + 1] not in commands_dict[com_d[1][i]]:
                    com8_7.append([com_d[1][i], com_d[1][i + 1]])
                else:
                    empty_com_1.append(com_d[1][i])
                    empty_com_2.append(com_d[1][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com8_7.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[0]) - 1, 2):
                if com_d[0][i + 1] not in commands_dict[com_d[0][i]]:
                    com8_8.append([com_d[0][i], com_d[0][i + 1]])
                else:
                    empty_com_1.append(com_d[0][i])
                    empty_com_2.append(com_d[0][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com8_8.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            if len(com_d[0]) % 2 != 0:
                com8_8.append([com_d[0][-1], "Пустышка"])

            file = open(f"{posts[0].title}/{posts[0].title}_тур8.txt", "r", encoding="utf-8")
            if len(file.read()) == 0:
                file = open(f"{posts[0].title}/{posts[0].title}_тур8.txt", "w", encoding="utf-8")
                num = 1
                title = "КОМАНДЫ" + " " * 35 + "|СЧЁТ"
                file.write(title + "\n")
                file.write("-" * len(title) + "\n")
                for com in com8_1:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com8_2:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com8_3:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com8_4:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com8_5:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com8_6:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com8_7:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com8_8:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                file.close()

            fp = open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "r", encoding="utf-8")
            commands_dict = json.load(fp)

            with open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "w", encoding="utf-8") as fp:
                s = json.dumps(commands_dict, ensure_ascii=False)
                fp.write(s)

            return render(request, 'blog/sсhedule.html',
                          {'title': 'Орда', 'name': posts[0].title, 'count_tour': int(count_tour),
                           'tour1': com_1,
                           'tour2_1': com2_1, 'tour2_2': com2_2,
                           'tour3_1': com3_1, 'tour3_2': com3_2, 'tour3_3': com3_3,
                           'tour4_1': com4_1, 'tour4_2': com4_2, 'tour4_3': com4_3, 'tour4_4': com4_4,
                           'tour5_1': com5_1, 'tour5_2': com5_2, 'tour5_3': com5_3, 'tour5_4': com5_4, 'tour5_5': com5_5,
                           'tour6_1': com6_1, 'tour6_2': com6_2, 'tour6_3': com6_3, 'tour6_4': com6_4, 'tour6_5': com6_5, 'tour6_6': com6_6,
                           'tour7_1': com7_1, 'tour7_2': com7_2, 'tour7_3': com7_3, 'tour7_4': com7_4, 'tour7_5': com7_5,'tour7_6': com7_6, 'tour7_7': com7_7,
                           'tour8_1': com8_1, 'tour8_2': com8_2, 'tour8_3': com8_3, 'tour8_4': com8_4, 'tour8_5': com8_5,'tour8_6': com8_6, 'tour8_7': com8_7, 'tour8_8': com8_8})


        case 7:
            file = open(f"{posts[0].title}/{posts[0].title}_тур2.txt", "r", encoding="utf-8")

            com_2 = []
            for line in file.readlines():
                if line.count("-") < 3 and line.count("КОМАНДЫ") == 0:
                    com_2.append(line)

            for i in range(0, len(com_2) // 2 - 1, 2):
                com2_1.append([com_2[i], com_2[i + 1]])

            for i in range(len(com_2) // 2, len(com_2) - 1, 2):
                com2_2.append([com_2[i], com_2[i + 1]])
            file.close()
            file_res = open(f"{posts[0].title}/результат_2_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)
            file_res.close()
            file_count = open(f"{posts[0].title}/{posts[0].title}_счёт_3.txt", "r", encoding="utf-8")
            count_list = file_count.read().split()
            file_count.close()
            p = 0

            for i in range(0, len(com_d[2]) - 1, 2):
                com3_1.append([com_d[2][i] + " " + count_list[p], com_d[2][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[1]) - 1, 2):
                com3_2.append([com_d[1][i] + " " + count_list[p], com_d[1][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[0]) - 1, 2):
                com3_3.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2

            file_res = open(f"{posts[0].title}/результат_3_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            file_res.close()
            file_count = open(f"{posts[0].title}/{posts[0].title}_счёт_4.txt", "r", encoding="utf-8")
            count_list = file_count.read().split()
            p = 0

            for i in range(0, len(com_d[3]) - 1, 2):
                com4_1.append([com_d[3][i] + " " + count_list[p], com_d[3][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[2]) - 1, 2):
                com4_2.append([com_d[2][i] + " " + count_list[p], com_d[2][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[1]) - 1, 2):
                com4_3.append([com_d[1][i] + " " + count_list[p], com_d[1][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[0]) - 1, 2):
                com4_4.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2

            file_count.close()
            file_res = open(f"{posts[0].title}/результат_4_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            file_res.close()
            file_res = open(f"{posts[0].title}/результат_4_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            file_count = open(f"{posts[0].title}/{posts[0].title}_счёт_5.txt", "r", encoding="utf-8")
            count_list = file_count.read().split()
            p = 0

            for i in range(0, len(com_d[4]) - 1, 2):
                com5_1.append([com_d[4][i] + " " + count_list[p], com_d[4][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[3]) - 1, 2):
                com5_2.append([com_d[3][i] + " " + count_list[p], com_d[3][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[2]) - 1, 2):
                com5_3.append([com_d[2][i] + " " + count_list[p], com_d[2][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[1]) - 1, 2):
                com5_4.append([com_d[1][i] + " " + count_list[p], com_d[1][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[0]) - 1, 2):
                com5_5.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2

            file_res = open(f"{posts[0].title}/результат_5_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)


            file_count = open(f"{posts[0].title}/{posts[0].title}_счёт_6.txt", "r", encoding="utf-8")
            count_list = file_count.read().split()
            p = 0

            for i in range(0, len(com_d[4]) - 1, 2):
                com6_1.append([com_d[4][i] + " " + count_list[p], com_d[4][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[3]) - 1, 2):
                com6_2.append([com_d[3][i] + " " + count_list[p], com_d[3][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[2]) - 1, 2):
                com6_3.append([com_d[2][i] + " " + count_list[p], com_d[2][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[1]) - 1, 2):
                com6_4.append([com_d[1][i] + " " + count_list[p], com_d[1][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[0]) - 1, 2):
                com6_5.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2

            p -= 1
            for i in range(0, len(com_d[0]) - 1, 2):
                com6_6.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2

            file_res = open(f"{posts[0].title}/результат_6_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            fp = open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "r", encoding="utf-8")
            commands_dict = json.load(fp)


            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[6]) - 1, 2):
                if com_d[6][i + 1] not in commands_dict[com_d[6][i]]:
                    com7_1.append([com_d[6][i], com_d[6][i + 1]])
                else:
                    empty_com_1.append(com_d[6][i])
                    empty_com_2.append(com_d[6][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com7_1.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[5]) - 1, 2):
                if com_d[5][i + 1] not in commands_dict[com_d[5][i]]:
                    com7_2.append([com_d[5][i], com_d[5][i + 1]])
                else:
                    empty_com_1.append(com_d[5][i])
                    empty_com_2.append(com_d[5][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com7_2.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[4]) - 1, 2):
                if com_d[4][i + 1] not in commands_dict[com_d[4][i]]:
                    com7_3.append([com_d[4][i], com_d[4][i + 1]])
                else:
                    empty_com_1.append(com_d[3][i])
                    empty_com_2.append(com_d[3][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com7_3.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break


            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[3]) - 1, 2):
                if com_d[3][i + 1] not in commands_dict[com_d[3][i]]:
                    com7_4.append([com_d[3][i], com_d[3][i + 1]])
                else:
                    empty_com_1.append(com_d[3][i])
                    empty_com_2.append(com_d[3][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com7_4.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[2]) - 1, 2):
                if com_d[2][i + 1] not in commands_dict[com_d[2][i]]:
                    com7_5.append([com_d[2][i], com_d[2][i + 1]])
                else:
                    empty_com_1.append(com_d[2][i])
                    empty_com_2.append(com_d[2][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com7_5.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[1]) - 1, 2):
                if com_d[1][i + 1] not in commands_dict[com_d[1][i]]:
                    com7_6.append([com_d[1][i], com_d[1][i + 1]])
                else:
                    empty_com_1.append(com_d[1][i])
                    empty_com_2.append(com_d[1][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com7_6.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[0]) - 1, 2):
                if com_d[0][i + 1] not in commands_dict[com_d[0][i]]:
                    com7_7.append([com_d[0][i], com_d[0][i + 1]])
                else:
                    empty_com_1.append(com_d[0][i])
                    empty_com_2.append(com_d[0][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com7_7.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            if len(com_d[0]) % 2 != 0:
                com7_7.append([com_d[0][-1], "Пустышка"])

            file = open(f"{posts[0].title}/{posts[0].title}_тур7.txt", "r", encoding="utf-8")
            if len(file.read()) == 0:
                file = open(f"{posts[0].title}/{posts[0].title}_тур7.txt", "w", encoding="utf-8")
                num = 1
                title = "КОМАНДЫ" + " " * 35 + "|СЧЁТ"
                file.write(title + "\n")
                file.write("-" * len(title) + "\n")
                for com in com7_1:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com7_2:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com7_3:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com7_4:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com7_5:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com7_6:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com7_7:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                file.close()

            fp = open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "r", encoding="utf-8")
            commands_dict = json.load(fp)

            with open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "w", encoding="utf-8") as fp:
                s = json.dumps(commands_dict, ensure_ascii=False)
                fp.write(s)

            return render(request, 'blog/sсhedule.html', {'title': 'Орда', 'name': posts[0].title, 'count_tour': int(count_tour),
                       'tour1': com_1,
                       'tour2_1': com2_1, 'tour2_2': com2_2,
                       'tour3_1': com3_1, 'tour3_2': com3_2, 'tour3_3': com3_3,
                       'tour4_1': com4_1, 'tour4_2': com4_2, 'tour4_3': com4_3, 'tour4_4': com4_4,
                       'tour5_1': com5_1, 'tour5_2': com5_2, 'tour5_3': com5_3, 'tour5_4': com5_4, 'tour5_5': com5_5,
                       'tour6_1': com6_1, 'tour6_2': com6_2, 'tour6_3': com6_3, 'tour6_4': com6_4, 'tour6_5': com6_5, 'tour6_6': com6_6,
                       'tour7_1': com7_1, 'tour7_2': com7_2, 'tour7_3': com7_3, 'tour7_4': com7_4, 'tour7_5': com7_5, 'tour7_6': com7_6, 'tour7_7': com7_7})
        case 6:
            file = open(f"{posts[0].title}/{posts[0].title}_тур2.txt", "r", encoding="utf-8")

            com_2 = []
            for line in file.readlines():
                if line.count("-") < 3 and line.count("КОМАНДЫ") == 0:
                    com_2.append(line)

            for i in range(0, len(com_2) // 2 - 1, 2):
                com2_1.append([com_2[i], com_2[i + 1]])

            for i in range(len(com_2) // 2, len(com_2) - 1, 2):
                com2_2.append([com_2[i], com_2[i + 1]])

            file_res = open(f"{posts[0].title}/результат_2_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            file_count = open(f"{posts[0].title}/{posts[0].title}_счёт_3.txt", "r", encoding="utf-8")
            count_list = file_count.read().split()
            p = 0

            for i in range(0, len(com_d[2]) - 1, 2):
                com3_1.append([com_d[2][i] + " " + count_list[p], com_d[2][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[1]) - 1, 2):
                com3_2.append([com_d[1][i] + " " + count_list[p], com_d[1][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[0]) - 1, 2):
                com3_3.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2

            file_res = open(f"{posts[0].title}/результат_3_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            file_count = open(f"{posts[0].title}/{posts[0].title}_счёт_4.txt", "r", encoding="utf-8")
            count_list = file_count.read().split()
            p = 0

            for i in range(0, len(com_d[3]) - 1, 2):
                com4_1.append([com_d[3][i] + " " + count_list[p], com_d[3][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[2]) - 1, 2):
                com4_2.append([com_d[2][i] + " " + count_list[p], com_d[2][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[1]) - 1, 2):
                com4_3.append([com_d[1][i] + " " + count_list[p], com_d[1][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[0]) - 1, 2):
                com4_4.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2

            file_res = open(f"{posts[0].title}/результат_4_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            file_count = open(f"{posts[0].title}/{posts[0].title}_счёт_5.txt", "r", encoding="utf-8")
            count_list = file_count.read().split()
            p = 0

            if len(com_d[4]) % 2 != 0:
                com_d[4].append("Пустышка")
            for i in range(0, len(com_d[4]) - 1, 2):
                com5_1.append([com_d[4][i] + " " + count_list[p], com_d[4][i + 1] + " " + count_list[p + 1]])
                p += 2

            if len(com_d[3]) % 2 != 0:
                com_d[3].append("Пустышка")
            for i in range(0, len(com_d[3]) - 1, 2):
                com5_2.append([com_d[3][i] + " " + count_list[p], com_d[3][i + 1] + " " + count_list[p + 1]])
                p += 2

            if len(com_d[2]) % 2 != 0:
                com_d[2].append("Пустышка")
            for i in range(0, len(com_d[2]) - 1, 2):
                com5_3.append([com_d[2][i] + " " + count_list[p], com_d[2][i + 1] + " " + count_list[p + 1]])
                p += 2

            if len(com_d[1]) % 2 != 0:
                com_d[1].append("Пустышка")
            for i in range(0, len(com_d[1]) - 1, 2):
                com5_4.append([com_d[1][i] + " " + count_list[p], com_d[1][i + 1] + " " + count_list[p + 1]])
                p += 2

            if len(com_d[0]) % 2 != 0:
                com_d[0].append("Пустышка")
            for i in range(0, len(com_d[0]) - 1, 2):
                com5_5.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2


            file_res = open(f"{posts[0].title}/результат_5_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)



            fp = open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "r", encoding="utf-8")
            commands_dict = json.load(fp)

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[5]) - 1, 2):
                if com_d[5][i + 1] not in commands_dict[com_d[5][i]]:
                    com6_1.append([com_d[5][i], com_d[5][i + 1]])
                else:
                    empty_com_1.append(com_d[5][i])
                    empty_com_2.append(com_d[5][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com6_1.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[4]) - 1, 2):
                if com_d[4][i + 1] not in commands_dict[com_d[4][i]]:
                    com6_2.append([com_d[4][i], com_d[4][i + 1]])
                else:
                    empty_com_1.append(com_d[4][i])
                    empty_com_2.append(com_d[4][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com6_2.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[3]) - 1, 2):
                if com_d[3][i + 1] not in commands_dict[com_d[3][i]]:
                    com6_3.append([com_d[3][i], com_d[3][i + 1]])
                else:
                    empty_com_1.append(com_d[3][i])
                    empty_com_2.append(com_d[3][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com6_3.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[2]) - 1, 2):
                if com_d[2][i + 1] not in commands_dict[com_d[2][i]]:
                    com6_4.append([com_d[2][i], com_d[2][i + 1]])
                else:
                    empty_com_1.append(com_d[2][i])
                    empty_com_2.append(com_d[2][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com6_4.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[1]) - 1, 2):
                if com_d[1][i + 1] not in commands_dict[com_d[1][i]]:
                    com6_5.append([com_d[1][i], com_d[1][i + 1]])
                else:
                    empty_com_1.append(com_d[1][i])
                    empty_com_2.append(com_d[1][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com6_5.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[0]) - 1, 2):
                if com_d[0][i + 1] not in commands_dict[com_d[0][i]]:
                    com6_6.append([com_d[0][i], com_d[0][i + 1]])
                else:
                    empty_com_1.append(com_d[0][i])
                    empty_com_2.append(com_d[0][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com6_6.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            if len(com_d[0]) % 2 != 0:
                com6_6.append([com_d[0][-1], "Пустышка"])

            file = open(f"{posts[0].title}/{posts[0].title}_тур6.txt", "r", encoding="utf-8")
            if len(file.read()) == 0:
                file = open(f"{posts[0].title}/{posts[0].title}_тур6.txt", "w", encoding="utf-8")
                num = 1
                title = "КОМАНДЫ" + " " * 35 + "|СЧЁТ"
                file.write(title + "\n")
                file.write("-" * len(title) + "\n")
                for com in com6_1:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com6_2:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com6_3:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com6_4:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com6_5:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com6_6:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                file.close()

            fp = open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "r", encoding="utf-8")
            commands_dict = json.load(fp)

            with open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "w", encoding="utf-8") as fp:
                s = json.dumps(commands_dict, ensure_ascii=False)
                fp.write(s)

            return render(request, 'blog/sсhedule.html',
                          {'title': 'Орда', 'name': posts[0].title, 'count_tour': int(count_tour),
                           'tour1': com_1,
                           'tour2_1': com2_1, 'tour2_2': com2_2,
                           'tour3_1': com3_1, 'tour3_2': com3_2, 'tour3_3': com3_3,
                           'tour4_1': com4_1, 'tour4_2': com4_2, 'tour4_3': com4_3, 'tour4_4': com4_4,
                           'tour5_1': com5_1, 'tour5_2': com5_2, 'tour5_3': com5_3, 'tour5_4': com5_4, 'tour5_5': com5_5,
                           'tour6_1': com6_1, 'tour6_2': com6_2, 'tour6_3': com6_3, 'tour6_4': com6_4, 'tour6_5': com6_5, 'tour6_6': com6_6})
        case 5:
            file = open(f"{posts[0].title}/{posts[0].title}_тур2.txt", "r", encoding="utf-8")

            com_2 = []
            for line in file.readlines():
                if line.count("-") < 3 and line.count("КОМАНДЫ") == 0:
                    com_2.append(line)

            for i in range(0, len(com_2) // 2 - 1, 2):
                com2_1.append([com_2[i], com_2[i + 1]])

            for i in range(len(com_2) // 2, len(com_2) - 1, 2):
                com2_2.append([com_2[i], com_2[i + 1]])

            file_res = open(f"{posts[0].title}/результат_2_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            file_count = open(f"{posts[0].title}/{posts[0].title}_счёт_3.txt", "r", encoding="utf-8")
            count_list = file_count.read().split()
            p = 0

            for i in range(0, len(com_d[2]) - 1, 2):
                com3_1.append([com_d[2][i] + " " + count_list[p], com_d[2][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[1]) - 1, 2):
                com3_2.append([com_d[1][i] + " " + count_list[p], com_d[1][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[0]) - 1, 2):
                com3_3.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2

            file_res = open(f"{posts[0].title}/результат_3_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            file_count = open(f"{posts[0].title}/{posts[0].title}_счёт_4.txt", "r", encoding="utf-8")
            count_list = file_count.read().split()
            p = 0

            for i in range(0, len(com_d[3]) - 1, 2):
                com4_1.append([com_d[3][i] + " " + count_list[p], com_d[3][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[2]) - 1, 2):
                com4_2.append([com_d[2][i] + " " + count_list[p], com_d[2][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[1]) - 1, 2):
                com4_3.append([com_d[1][i] + " " + count_list[p], com_d[1][i + 1] + " " + count_list[p + 1]])
                p += 2

            for i in range(0, len(com_d[0]) - 1, 2):
                com4_4.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p + 1]])
                p += 2


            file_res = open(f"{posts[0].title}/результат_4_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            fp = open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "r", encoding="utf-8")
            commands_dict = json.load(fp)

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[4]) - 1, 2):
                if com_d[4][i + 1] not in commands_dict[com_d[4][i]]:
                    com5_1.append([com_d[4][i], com_d[4][i + 1]])
                else:
                    empty_com_1.append(com_d[4][i])
                    empty_com_2.append(com_d[4][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com5_1.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[3]) - 1, 2):
                if com_d[3][i + 1] not in commands_dict[com_d[3][i]]:
                    com5_2.append([com_d[3][i], com_d[3][i + 1]])
                else:
                    empty_com_1.append(com_d[3][i])
                    empty_com_2.append(com_d[3][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com5_2.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[2]) - 1, 2):
                if com_d[2][i + 1] not in commands_dict[com_d[2][i]]:
                    com5_3.append([com_d[2][i], com_d[2][i + 1]])
                else:
                    empty_com_1.append(com_d[2][i])
                    empty_com_2.append(com_d[2][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com5_3.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[1]) - 1, 2):
                if com_d[1][i + 1] not in commands_dict[com_d[1][i]]:
                    com5_4.append([com_d[1][i], com_d[1][i + 1]])
                else:
                    empty_com_1.append(com_d[1][i])
                    empty_com_2.append(com_d[1][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com5_4.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[0]) - 1, 2):
                if com_d[0][i + 1] not in commands_dict[com_d[0][i]]:
                    com5_5.append([com_d[0][i], com_d[0][i + 1]])
                else:
                    empty_com_1.append(com_d[0][i])
                    empty_com_2.append(com_d[0][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com5_5.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            if len(com_d[0]) % 2 != 0:
                com5_5.append([com_d[0][-1], "Пустышка"])

            if len(com_d[1]) % 2 != 0:
                com5_4.append([com_d[1][-1], "Пустышка"])

            if len(com_d[2]) % 2 != 0:
                com5_3.append([com_d[2][-1], "Пустышка"])

            if len(com_d[3]) % 2 != 0:
                com5_2.append([com_d[3][-1], "Пустышка"])

            if len(com_d[4]) % 2 != 0:
                com5_1.append([com_d[4][-1], "Пустышка"])

            file = open(f"{posts[0].title}/{posts[0].title}_тур5.txt", "r", encoding="utf-8")
            if len(file.read()) == 0:
                file = open(f"{posts[0].title}/{posts[0].title}_тур5.txt", "w", encoding="utf-8")
                num = 1
                title = "КОМАНДЫ" + " " * 35 + "|СЧЁТ"
                file.write(title + "\n")
                file.write("-" * len(title) + "\n")
                for com in com5_1:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com5_2:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com5_3:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com5_4:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com5_5:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                file.close()

            fp = open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "r", encoding="utf-8")
            commands_dict = json.load(fp)

            with open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "w", encoding="utf-8") as fp:
                s = json.dumps(commands_dict, ensure_ascii=False)
                fp.write(s)

            return render(request, 'blog/sсhedule.html',
                          {'title': 'Орда', 'name': posts[0].title, 'count_tour': int(count_tour),
                           'tour1': com_1,
                           'tour2_1': com2_1, 'tour2_2': com2_2,
                           'tour3_1': com3_1, 'tour3_2': com3_2, 'tour3_3': com3_3,
                           'tour4_1': com4_1, 'tour4_2': com4_2, 'tour4_3': com4_3, 'tour4_4': com4_4,
                           'tour5_1': com5_1, 'tour5_2': com5_2, 'tour5_3': com5_3, 'tour5_4': com5_4, 'tour5_5': com5_5})
        case 4:
            file = open(f"{posts[0].title}/{posts[0].title}_тур2.txt", "r", encoding="utf-8")

            com_2 = []
            for line in file.readlines():
                if line.count("-") < 3 and line.count("КОМАНДЫ") == 0:
                    com_2.append(line)

            for i in range(0, len(com_2) // 2 - 1, 2):
                com2_1.append([com_2[i], com_2[i + 1]])

            for i in range(len(com_2) // 2, len(com_2) - 1, 2):
                com2_2.append([com_2[i], com_2[i + 1]])

            file_res = open(f"{posts[0].title}/результат_2_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            file_count = open(f"{posts[0].title}/{posts[0].title}_счёт_3.txt", "r", encoding="utf-8")
            count_list = file_count.read().split()
            p = 0

            if len(com_d[2]) % 2 != 0:
                com_d[2].append("Пустышка")
            for i in range(0, len(com_d[2]) - 1, 2):
                com3_1.append([com_d[2][i] + " " + count_list[p], com_d[2][i + 1] + " " + count_list[p+1]])
                p += 2

            if len(com_d[1]) % 2 != 0:
                com_d[1].append("Пустышка")
            for i in range(0, len(com_d[1]) - 1, 2):
                com3_2.append([com_d[1][i] + " " + count_list[p], com_d[1][i + 1] + " " + count_list[p+1]])
                p += 2

            if len(com_d[0]) % 2 != 0:
                com_d[0].append("Пустышка")
            for i in range(0, len(com_d[0]) - 1, 2):
                com3_3.append([com_d[0][i] + " " + count_list[p], com_d[0][i + 1] + " " + count_list[p+1]])
                p += 2

            file_res = open(f"{posts[0].title}/результат_3_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)

            fp = open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "r", encoding="utf-8")
            commands_dict = json.load(fp)

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[3]) - 1, 2):
                if com_d[3][i + 1] not in commands_dict[com_d[3][i]]:
                    com4_1.append([com_d[3][i], com_d[3][i + 1]])
                else:
                    empty_com_1.append(com_d[3][i])
                    empty_com_2.append(com_d[3][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com4_1.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[2]) - 1, 2):
                if com_d[2][i + 1] not in commands_dict[com_d[2][i]]:
                    com4_2.append([com_d[2][i], com_d[2][i + 1]])
                else:
                    empty_com_1.append(com_d[2][i])
                    empty_com_2.append(com_d[2][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com4_2.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[1]) - 1, 2):
                if com_d[1][i + 1] not in commands_dict[com_d[1][i]]:
                    com4_3.append([com_d[1][i], com_d[1][i + 1]])
                else:
                    empty_com_1.append(com_d[1][i])
                    empty_com_2.append(com_d[1][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com4_3.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[0]) - 1, 2):
                if com_d[0][i + 1] not in commands_dict[com_d[0][i]]:
                    com4_4.append([com_d[0][i], com_d[0][i + 1]])
                else:
                    empty_com_1.append(com_d[0][i])
                    empty_com_2.append(com_d[0][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com4_4.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            if len(com_d[0]) % 2 != 0:
                com4_4.append([com_d[0][-1], "Пустышка"])

            if len(com_d[1]) % 2 != 0:
                com4_3.append([com_d[1][-1], "Пустышка"])

            if len(com_d[2]) % 2 != 0:
                com4_2.append([com_d[2][-1], "Пустышка"])

            if len(com_d[3]) % 2 != 0:
                com4_1.append([com_d[3][-1], "Пустышка"])


            file = open(f"{posts[0].title}/{posts[0].title}_тур4.txt", "r", encoding="utf-8")
            if len(file.read()) == 0:
                file = open(f"{posts[0].title}/{posts[0].title}_тур4.txt", "w", encoding="utf-8")
                num = 1
                title = "КОМАНДЫ" + " " * 35 + "|СЧЁТ"
                file.write(title + "\n")
                file.write("-" * len(title) + "\n")

                for com in com4_1:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com4_2:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com4_3:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com4_4:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                file.close()

            fp = open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "r", encoding="utf-8")
            commands_dict = json.load(fp)

            for i in range(0, len(com4_1)):
                if com4_1[i][0][:45].replace("\n", "").strip() not in commands_dict[com4_1[i][1][:45].replace("\n", "").strip()]:
                    commands_dict[com4_1[i][1][:45].replace("\n", "").strip()].append(com4_1[i][0][:45].replace("\n", "").strip())
                if com4_1[i][1][:45].replace("\n", "").strip() not in commands_dict[com4_1[i][0][:45].replace("\n", "").strip()]:
                    commands_dict[com4_1[i][0][:45].replace("\n", "").strip()].append(com4_1[i][1][:45].replace("\n", "").strip())

            for i in range(0, len(com4_2)):
                if com4_2[i][0][:45].replace("\n", "").strip() not in commands_dict[com4_2[i][1][:45].replace("\n", "").strip()]:
                    commands_dict[com4_2[i][1][:45].replace("\n", "").strip()].append(com4_2[i][0][:45].replace("\n", "").strip())
                if com4_2[i][1][:45].replace("\n", "").strip() not in commands_dict[com4_2[i][0][:45].replace("\n", "").strip()]:
                    commands_dict[com4_2[i][0][:45].replace("\n", "").strip()].append(com4_2[i][1][:45].replace("\n", "").strip())

            for i in range(0, len(com4_3)):
                if com4_3[i][0][:45].replace("\n", "").strip() not in commands_dict[com4_3[i][1][:45].replace("\n", "").strip()]:
                    commands_dict[com4_3[i][1][:45].replace("\n", "").strip()].append(com4_3[i][0][:45].replace("\n", "").strip())
                if com4_3[i][1][:45].replace("\n", "").strip() not in commands_dict[com4_3[i][0][:45].replace("\n", "").strip()]:
                    commands_dict[com4_3[i][0][:45].replace("\n", "").strip()].append( com4_3[i][1][:45].replace("\n", "").strip())

            for i in range(0, len(com4_4)):
                if com4_4[i][0][:45].replace("\n", "").strip() not in commands_dict[com4_4[i][1][:45].replace("\n", "").strip()]:
                    commands_dict[com4_4[i][1][:45].replace("\n", "").strip()].append(com4_4[i][0][:45].replace("\n", "").strip())
                if com4_4[i][1][:45].replace("\n", "").strip() not in commands_dict[com4_4[i][0][:45].replace("\n", "").strip()]:
                    commands_dict[com4_4[i][0][:45].replace("\n", "").strip()].append( com4_4[i][1][:45].replace("\n", "").strip())

            with open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "w", encoding="utf-8") as fp:
                s = json.dumps(commands_dict, ensure_ascii=False)
                fp.write(s)

            return render(request, 'blog/sсhedule.html',
                          {'title': 'Орда', 'name': posts[0].title, 'count_tour': int(count_tour),
                           'tour1': com_1,
                           'tour2_1': com2_1, 'tour2_2': com2_2,
                           'tour3_1': com3_1, 'tour3_2': com3_2, 'tour3_3': com3_3,
                           'tour4_1': com4_1, 'tour4_2': com4_2, 'tour4_3': com4_3, 'tour4_4': com4_4})
        case 3:
            file_res = open(f"{posts[0].title}/результат_1_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)


            count_file = open(f"{posts[0].title}/{posts[0].title}_счёт_2.txt", "r", encoding="utf-8")
            count_list = count_file.read().split()
            j = 0
            com2_1 = []
            for i in range(0, len(com_d[1]) - 1, 2):
                com2_1.append([com_d[1][i] + " " + count_list[j], com_d[1][i+1] + " " + count_list[j+1]])
                j += 2

            com2_2 = []
            for i in range(0, len(com_d[0]) - 1, 2):
                com2_2.append([com_d[0][i] + " " + count_list[j], com_d[0][i+1] + " " + count_list[j+1]])
                j += 2


            file_res = open(f"{posts[0].title}/результат_{count_tour - 1}_{posts[0].title}.txt", "r", encoding="utf-8")
            file_res.seek(0)
            com_d = {}
            for i in range(0, 10):
                com_d[i] = []
            for line in file_res.readlines():
                if len(line.replace("\n", "")) != 0:
                    com = line.split(": ")[0]
                    win = int(line.split(": ")[1])
                    com_d[win].append(com)


            fp = open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "r", encoding="utf-8")
            commands_dict = json.load(fp)

            commands_dict["Пустышка"] = []

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[2]) - 1, 2):
                if com_d[2][i + 1] not in commands_dict[com_d[2][i]]:
                    com3_1.append([com_d[2][i], com_d[2][i + 1]])
                else:
                    empty_com_1.append(com_d[2][i])
                    empty_com_2.append(com_d[2][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com3_1.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[1]) - 1, 2):
                if com_d[1][i + 1] not in commands_dict[com_d[1][i]]:
                    com3_2.append([com_d[1][i], com_d[1][i + 1]])
                else:
                    empty_com_1.append(com_d[1][i])
                    empty_com_2.append(com_d[1][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com3_2.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[0]) - 1, 2):
                if com_d[0][i + 1] not in commands_dict[com_d[0][i]]:
                    com3_3.append([com_d[0][i], com_d[0][i + 1]])
                else:
                    empty_com_1.append(com_d[0][i])
                    empty_com_2.append(com_d[0][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com3_3.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            if len(com_d[0]) % 2 != 0:
                com3_3.append([com_d[0][-1], "Пустышка"])

            if len(com_d[1]) % 2 != 0:
                com3_2.append([com_d[1][-1], "Пустышка"])

            if len(com_d[2]) % 2 != 0:
                com3_1.append([com_d[2][-1], "Пустышка"])

            file = open(f"{posts[0].title}/{posts[0].title}_тур3.txt", "r", encoding="utf-8")
            if len(file.read()) == 0:
                file = open(f"{posts[0].title}/{posts[0].title}_тур3.txt", "w", encoding="utf-8")
                num = 1
                title = "КОМАНДЫ" + " " * 35 + "|СЧЁТ"
                file.write(title + "\n")
                file.write("-" * len(title) + "\n")
                shuffle(com3_1)
                shuffle(com3_2)
                shuffle(com3_3)
                for com in com3_1:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com3_2:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com3_3:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                file.close()

            fp = open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "r", encoding="utf-8")
            commands_dict = json.load(fp)

            commands_dict["Пустышка"] = []

            for i in range(0, len(com3_1)):
                if com3_1[i][0][:45].replace("\n", "").strip() not in commands_dict[com3_1[i][1][:45].replace("\n", "").strip()]:
                    commands_dict[com3_1[i][1][:45].replace("\n", "").strip()].append(com3_1[i][0][:45].replace("\n", "").strip())
                if com3_1[i][1][:45].replace("\n", "").strip() not in commands_dict[com3_1[i][0][:45].replace("\n", "").strip()]:
                    commands_dict[com3_1[i][0][:45].replace("\n", "").strip()].append(com3_1[i][1][:45].replace("\n", "").strip())

            for i in range(0, len(com3_2)):
                if com3_2[i][0][:45].replace("\n", "").strip() not in commands_dict[com3_2[i][1][:45].replace("\n", "").strip()]:
                    commands_dict[com3_2[i][1][:45].replace("\n", "").strip()].append(com3_2[i][0][:45].replace("\n", "").strip())
                if com3_2[i][1][:45].replace("\n", "").strip() not in commands_dict[com3_2[i][0][:45].replace("\n", "").strip()]:
                    commands_dict[com3_2[i][0][:45].replace("\n", "").strip()].append(com3_2[i][1][:45].replace("\n", "").strip())

            for i in range(0, len(com3_3)):
                if com3_3[i][0][:45].replace("\n", "").strip() not in commands_dict[com3_3[i][1][:45].replace("\n", "").strip()]:
                    commands_dict[com3_3[i][1][:45].replace("\n", "").strip()].append(com3_3[i][0][:45].replace("\n", "").strip())
                if com3_3[i][1][:45].replace("\n", "").strip() not in commands_dict[com3_3[i][0][:45].replace("\n", "").strip()]:
                    commands_dict[com3_3[i][0][:45].replace("\n", "").strip()].append( com3_3[i][1][:45].replace("\n", "").strip())

            with open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "w", encoding="utf-8") as fp:
                s = json.dumps(commands_dict, ensure_ascii=False)
                fp.write(s)

            # tour_shedule
            font_ = ImageFont.truetype("fonts/BebasNeueProExpandedExtraBoldIt.ttf", 40)
            font_c = ImageFont.truetype("fonts/BebasNeueProExpandedExtraBoldIt.ttf", 35)
            game_name = posts[0].title.split()[0]
            div_name = posts[0].title.split()[1]

            if posts[0].title.split()[1] == "МСКЛ":
                base_img = Image.open('shedule/back1.png')
                game_ = Image.open(f'shedule/{game_name}.png').resize((220, 220))
                Image.Image.paste(base_img, game_, (1650, 90), mask=game_)
                drawer = ImageDraw.Draw(base_img)

                height = 402

                file = open(f"{posts[0].title}/{posts[0].title}_тур3.txt", "r", encoding="utf-8")
                file_list = []
                for line in file.readlines()[2:]:
                    if line.count("----------"):
                        pass
                    else:
                        file_list.append(line.replace("\n", "").strip())

                # shuffle(file_list)

                file = open(f"{posts[0].title}/{posts[0].title}_тур3.txt", "w", encoding="utf-8")
                num = 1
                title = "КОМАНДЫ" + " " * 35 + "|СЧЁТ\n"
                file.write(title)
                file.write("-" * len(title) + "\n")
                for command in file_list:
                    file.write(command.replace("\n", "").ljust(35) + "\n")
                    if num % 2 == 0:
                        file.write("-" * len(title) + "\n")
                    num += 1

                file = open(f"{posts[0].title}/{posts[0].title}_тур3.txt", "r", encoding="utf-8")
                file.seek(0)
                c = ((len(file.readlines()) - 23) // 3)
                count_photo = 0
                while c > 0:
                    count_photo += 1
                    c -= 11

                file.seek(0)
                other = 0
                for line in file.readlines():
                    if line.count("----------------------------------") > 0:
                        other += 1
                file.seek(0)
                file.seek(0)
                file.readline()
                file.readline()

                for _ in range(7):
                    line = file.readline()
                    team_1 = line[:45].strip()
                    total_1 = line[45:].strip()
                    line = file.readline()
                    team_2 = line[:45].strip()
                    total_2 = line[45:].strip()
                    file.readline()
                    drawer.text((150, height), team_1, font=font_c, fill='white')
                    drawer.text((1180, height), team_2, font=font_c, fill='white')
                    height += 90

                base_img.save(f'{posts[0].title}/tour_shedule_3.png', quality=100)

                for i in range(1, count_photo + 1):
                    height = 65
                    base_img_copy = Image.open('shedule/back2.png')
                    drawer = ImageDraw.Draw(base_img_copy)
                    for _ in range(11):
                        line = file.readline()
                        team_1 = line[:45].strip()
                        line = file.readline()
                        team_2 = line[:45].strip()
                        file.readline()
                        drawer.text((120, height), team_1, font=font_c, fill='white')
                        drawer.text((1180, height), team_2, font=font_c, fill='white')
                        height += 90.5
                    base_img_copy.save(f'{posts[0].title}/tour_shedule_3_{i}.png', quality=100)
                    height = 63

            else:

                base_img = Image.open('shedule/shedule.png')
                div = Image.open(f'shedule/{div_name}.png').resize((250, 278))
                Image.Image.paste(base_img, div, (1570, 76), mask=div)
                game_ = Image.open(f'shedule/{game_name}.png').resize((220, 220))
                Image.Image.paste(base_img, game_, (1274, 90), mask=game_)
                drawer = ImageDraw.Draw(base_img)
                tour_ = 2
                drawer.text((55, 65), str(tour_) + " ТУР", font=font_, fill='white')
                drawer.text((55, 98), "", font=font_, fill='white')

                height = 415

                file = open(f"{posts[0].title}/{posts[0].title}_тур3.txt", "r", encoding="utf-8")
                file.seek(0)
                c = ((len(file.readlines()) - 2) // 3)
                count_photo = 0
                while c > 0:
                    count_photo += 1
                    c -= 5

                file.seek(0)
                other = 0
                for line in file.readlines():
                    if line.count("----------------------------------") > 0:
                        other += 1
                file.seek(0)
                file.seek(0)
                file.readline()
                file.readline()

                base_img.save(f'{posts[0].title}/tour_shedule_3.png', quality=100)

                for i in range(1, count_photo + 1):
                    base_img_copy = Image.open(f'{posts[0].title}/tour_shedule_3.png')
                    drawer = ImageDraw.Draw(base_img_copy)
                    for _ in range(5):
                        line = file.readline()
                        team_1 = line[:45].strip()
                        total_1 = line[45:].strip()
                        line = file.readline()
                        team_2 = line[:45].strip()
                        total_2 = line[45:].strip()
                        file.readline()
                        drawer.text((150, height), team_1, font=font_c, fill='white')
                        drawer.text((1210, height), team_2, font=font_c, fill='white')
                        height += 134
                    base_img_copy.save(f'{posts[0].title}/tour_shedule_3_{i}.png', quality=100)
                    height = 415
                # ------ end ------

            return render(request, 'blog/sсhedule.html',
                          {'title': 'Орда', 'name': posts[0].title, 'count_tour': int(count_tour),
                           'tour1': com_1,
                           'tour2_1': com2_1, 'tour2_2': com2_2,
                           'tour3_1': com3_1, 'tour3_2': com3_2, 'tour3_3': com3_3})
        case 2:

            fp = open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "r", encoding="utf-8")
            commands_dict = json.load(fp)

            commands_dict["Пустышка"] = []

            empty_com_1 = []
            empty_com_2 = []
            for i in range(0, len(com_d[1]) - 1, 2):
                if com_d[1][i+1] not in commands_dict[com_d[1][i]]:
                    com2_1.append([com_d[1][i], com_d[1][i + 1]])
                else:
                    empty_com_1.append(com_d[1][i])
                    empty_com_2.append(com_d[1][i + 1])

            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com2_1.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break

            # ------
            empty_com_1 = []
            empty_com_2 = []

            for i in range(0, len(com_d[0]) - 1, 2):
                if com_d[0][i + 1] not in commands_dict[com_d[0][i]]:
                    com2_2.append([com_d[0][i], com_d[0][i + 1]])
                else:
                    empty_com_1.append(com_d[0][i])
                    empty_com_2.append(com_d[0][i + 1])


            for i in range(0, len(empty_com_1)):
                for c in empty_com_2:
                    if c not in empty_com_1[i]:
                        com2_2.append((empty_com_1[i], c))
                        empty_com_2.remove(c)
                        break


            if len(com_d[0]) % 2 != 0:
                com2_2.append([com_d[0][-1], "Пустышка"])

            if len(com_d[1]) % 2 != 0:
                com2_1.append([com_d[1][-1], "Пустышка"])

            file = open(f"{posts[0].title}/{posts[0].title}_тур2.txt", "r", encoding="utf-8")
            if len(file.read()) == 0:
                file.close()
                file = open(f"{posts[0].title}/{posts[0].title}_тур2.txt", "w", encoding="utf-8")
                num = 1
                title = "КОМАНДЫ" + " " * 35 + "|СЧЁТ"
                file.write(title + "\n")
                file.write("-" * len(title) + "\n")

                shuffle(com2_1)
                shuffle(com2_2)
                for com in com2_1:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")
                for com in com2_2:
                    file.write(com[0].replace("\n", "").ljust(37) + "\n")
                    file.write(com[1].replace("\n", "").ljust(37) + "\n")
                    file.write("-" * len(title) + "\n")


            fp = open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "r", encoding="utf-8")
            commands_dict = json.load(fp)
            commands_dict["Пустышка"] = []
            fp.close()

            for i in range(0, len(com2_1)):
                if com2_1[i][0][:45].replace("\n", "").strip() not in commands_dict[com2_1[i][1][:45].replace("\n", "").strip()]:
                    commands_dict[com2_1[i][1][:45].replace("\n", "").strip()].append(com2_1[i][0][:45].replace("\n", "").strip())
                if com2_1[i][1][:45].replace("\n", "").strip() not in commands_dict[com2_1[i][0][:45].replace("\n", "").strip()]:
                    commands_dict[com2_1[i][0][:45].replace("\n", "").strip()].append(com2_1[i][1][:45].replace("\n", "").strip())

            for i in range(0, len(com2_2)):
                if com2_2[i][0][:45].replace("\n", "").strip() not in commands_dict[com2_2[i][1][:45].replace("\n", "").strip()]:
                    commands_dict[com2_2[i][1][:45].replace("\n", "").strip()].append(com2_2[i][0][:45].replace("\n", "").strip())
                if com2_2[i][1][:45].replace("\n", "").strip() not in commands_dict[com2_2[i][0][:45].replace("\n", "").strip()]:
                    commands_dict[com2_2[i][0][:45].replace("\n", "").strip()].append(com2_2[i][1][:45].replace("\n", "").strip())


            with open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "w", encoding="utf-8") as fp:
                s = json.dumps(commands_dict, ensure_ascii=False)
                fp.write(s)

                # tour_shedule
                font_ = ImageFont.truetype("fonts/BebasNeueProExpandedExtraBoldIt.ttf", 40)
                font_c = ImageFont.truetype("fonts/BebasNeueProExpandedExtraBoldIt.ttf", 35)
                game_name = posts[0].title.split()[0]
                div_name = posts[0].title.split()[1]

                if posts[0].title.split()[1] == "МСКЛ":
                    base_img = Image.open('shedule/back1.png')
                    game_ = Image.open(f'shedule/{game_name}.png').resize((220, 220))
                    Image.Image.paste(base_img, game_, (1650, 90), mask=game_)
                    drawer = ImageDraw.Draw(base_img)

                    height = 402

                    file = open(f"{posts[0].title}/{posts[0].title}_тур2.txt", "r", encoding="utf-8")
                    file_list = []
                    for line in file.readlines()[2:]:
                        if line.count("----------"):
                            pass
                        else:
                            file_list.append(line.replace("\n", "").strip())

                    # shuffle(file_list)

                    file = open(f"{posts[0].title}/{posts[0].title}_тур2.txt", "w", encoding="utf-8")
                    num = 1
                    title = "КОМАНДЫ" + " " * 35 + "|СЧЁТ\n"
                    file.write(title)
                    file.write("-" * len(title) + "\n")
                    for command in file_list:
                        file.write(command.replace("\n", "").ljust(35) + "\n")
                        if num % 2 == 0:
                            file.write("-" * len(title) + "\n")
                        num += 1

                    file = open(f"{posts[0].title}/{posts[0].title}_тур2.txt", "r", encoding="utf-8")
                    file.seek(0)
                    c = ((len(file.readlines()) - 23) // 3)
                    count_photo = 0
                    while c > 0:
                        count_photo += 1
                        c -= 11

                    file.seek(0)
                    other = 0
                    for line in file.readlines():
                        if line.count("----------------------------------") > 0:
                            other += 1
                    file.seek(0)
                    file.seek(0)
                    file.readline()
                    file.readline()

                    for _ in range(7):
                        line = file.readline()
                        team_1 = line[:45].strip()
                        total_1 = line[45:].strip()
                        line = file.readline()
                        team_2 = line[:45].strip()
                        total_2 = line[45:].strip()
                        file.readline()
                        drawer.text((150, height), team_1, font=font_c, fill='white')
                        drawer.text((1180, height), team_2, font=font_c, fill='white')
                        height += 90

                    base_img.save(f'{posts[0].title}/tour_shedule_2.png', quality=100)

                    for i in range(1, count_photo + 1):
                        height = 65
                        base_img_copy = Image.open('shedule/back2.png')
                        drawer = ImageDraw.Draw(base_img_copy)
                        for _ in range(11):
                            line = file.readline()
                            team_1 = line[:45].strip()
                            line = file.readline()
                            team_2 = line[:45].strip()
                            file.readline()
                            drawer.text((120, height), team_1, font=font_c, fill='white')
                            drawer.text((1180, height), team_2, font=font_c, fill='white')
                            height += 90.5
                        base_img_copy.save(f'{posts[0].title}/tour_shedule_2_{i}.png', quality=100)
                        height = 63

                else:

                    base_img = Image.open('shedule/shedule.png')
                    div = Image.open(f'shedule/{div_name}.png').resize((250, 278))
                    Image.Image.paste(base_img, div, (1570, 76), mask=div)
                    game_ = Image.open(f'shedule/{game_name}.png').resize((220, 220))
                    Image.Image.paste(base_img, game_, (1274, 90), mask=game_)
                    drawer = ImageDraw.Draw(base_img)
                    tour_ = 2
                    drawer.text((55, 65), str(tour_) + " ТУР", font=font_, fill='white')
                    drawer.text((55, 98), "", font=font_, fill='white')

                    height = 415

                    file = open(f"{posts[0].title}/{posts[0].title}_тур2.txt", "r", encoding="utf-8")
                    file.seek(0)
                    c = ((len(file.readlines()) - 2) // 3)
                    count_photo = 0
                    while c > 0:
                        count_photo += 1
                        c -= 5

                    file.seek(0)
                    other = 0
                    for line in file.readlines():
                        if line.count("----------------------------------") > 0:
                            other += 1
                    file.seek(0)
                    file.seek(0)
                    file.readline()
                    file.readline()

                    base_img.save(f'{posts[0].title}/tour_shedule_2.png', quality=100)


                    for i in range(1, count_photo + 1):
                        base_img_copy = Image.open(f'{posts[0].title}/tour_shedule_2.png')
                        drawer = ImageDraw.Draw(base_img_copy)
                        for _ in range(5):
                            line = file.readline()
                            team_1 = line[:45].strip()
                            total_1 = line[45:].strip()
                            line = file.readline()
                            team_2 = line[:45].strip()
                            total_2 = line[45:].strip()
                            file.readline()
                            drawer.text((150, height), team_1, font=font_c, fill='white')
                            drawer.text((1210, height), team_2, font=font_c, fill='white')
                            height += 134
                        base_img_copy.save(f'{posts[0].title}/tour_shedule_2_{i}.png', quality=100)
                        height = 415
                    # ------ end ------

            return render(request, 'blog/sсhedule.html',
                          {'title': 'Орда', 'name': posts[0].title, 'count_tour': int(count_tour),
                           'tour1': com_1,
                           'tour2_1': com2_1, 'tour2_2': com2_2})
        case 1:
            if os.path.exists(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json"):
                fp = open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "r", encoding="utf-8")
                commands_dict = json.load(fp)

            commands_dict["Пустышка"] = []


            # for i in range(0, len(com_1)):
            #     if com_1[i][1][:45].strip() not in commands_dict[com_1[i][0][:45].strip()]:
            #         commands_dict[com_1[i][0][:45].strip()].append(com_1[i][1][:45].replace("\n", "").strip())
            #     if com_1[i][0][:45].strip() not in commands_dict[com_1[i][1][:45].strip()]:
            #         commands_dict[com_1[i][1][:45].strip()].append(com_1[i][0][:45].strip())

            for i in range(0, len(com_1)):
                commands_dict[com_1[i][0][:45].strip()] = [com_1[i][1][:45].strip()]
                commands_dict[com_1[i][1][:45].strip()] = [com_1[i][0][:45].strip()]

            with open(f"{posts[0].title}/пересечение_команд_{posts[0].title}.json", "w", encoding="utf-8") as fp:
                s = json.dumps(commands_dict, ensure_ascii=False)
                fp.write(s)

                # tour_shedule
                if posts[0].title.split()[1] == "МСКЛ":
                    pass
                else:
                    font_ = ImageFont.truetype("fonts/BebasNeueProExpandedExtraBoldIt.ttf", 40)
                    font_c = ImageFont.truetype("fonts/BebasNeueProExpandedExtraBoldIt.ttf", 35)
                    game_name = posts[0].title.split()[0]
                    div_name = posts[0].title.split()[1]

                    base_img = Image.open('shedule/shedule.png')
                    div = Image.open(f'shedule/{div_name}.png').resize((250, 278))
                    Image.Image.paste(base_img, div, (1570, 76), mask=div)
                    game_ = Image.open(f'shedule/{game_name}.png').resize((220, 220))
                    Image.Image.paste(base_img, game_, (1274, 90), mask=game_)
                    drawer = ImageDraw.Draw(base_img)
                    tour_ = 1
                    drawer.text((55, 65), str(tour_) + " ТУР", font=font_, fill='white')
                    drawer.text((55, 98), "", font=font_, fill='white')

                    height = 415

                    file = open(f"{posts[0].title}/{posts[0].title}_тур1.txt", "r", encoding="utf-8")
                    file.seek(0)
                    c = ((len(file.readlines()) - 2) // 3)
                    count_photo = 0
                    while c > 0:
                        count_photo += 1
                        c -= 5

                    file.seek(0)
                    other = 0
                    for line in file.readlines():
                        if line.count("----------------------------------") > 0:
                            other += 1
                    file.seek(0)
                    file.seek(0)
                    file.readline()
                    file.readline()

                    base_img.save(f'{posts[0].title}/tour_shedule_1.png', quality=100)

                    for i in range(1, count_photo + 1):
                        base_img_copy = Image.open(f'{posts[0].title}/tour_shedule_1.png')
                        drawer = ImageDraw.Draw(base_img_copy)
                        for _ in range(5):
                            line = file.readline()
                            team_1 = line[:45].strip()
                            total_1 = line[45:].strip()
                            line = file.readline()
                            team_2 = line[:45].strip()
                            total_2 = line[45:].strip()
                            file.readline()
                            drawer.text((150, height), team_1, font=font_c, fill='white')
                            drawer.text((1210, height), team_2, font=font_c, fill='white')
                            height += 134
                        base_img_copy.save(f'{posts[0].title}/tour_shedule_1_{i}.png', quality=100)
                        height = 415
                    # ------ end ------

            return render(request, 'blog/sсhedule.html',
                          {'title': 'Орда', 'name': posts[0].title, 'count_tour': int(count_tour),
                           'tour1': com_1})
    file_res.close()
    file_count.close()
    file.close()



def save_tour_1(request):
    if request.method == 'GET':
        game = request.GET.get("name")
        game_name, div_name = game.split()
        checkbox = list(request.GET.get("data"))
        com_add = request.GET.get("com").split("\n")
        com_del = request.GET.get("del").split("\n")

        file = open(f"{game}/{game}_счёт_1.txt", "w", encoding="utf-8")
        file.write(" ".join(checkbox))
        file.close()
        file = open(f"{game}/{game}_тур1.txt", "r", encoding="utf-8")
        file_list = []
        i = 0


        for line in file.readlines():
            if line.count("КОМАНДЫ") or line.count("---------------") or line.count(" ") > 40 or line.strip() in com_del:
                file_list.append(line)
            else:
                new_line = line.replace("\n", "")
                # l1 = new_line[:len(line) // 2]
                # l2 = new_line[len(line) // 2:].replace("1", "").replace("0", "")
                l1 = new_line[:45]
                new_line = l1 + " " * 20 + checkbox[i] + "\n"
                file_list.append(new_line)
                i += 1

        file.close()
        file = open(f"{game}/{game}_тур1.txt", "w", encoding="utf-8")
        for el in file_list:
            file.write(el)
        file.close()

        # init dict with commands
        commands_file = open(f"{game}/команды_{game}.txt", "r", encoding="utf-8")
        com_dict = {}
        for com in commands_file.readlines():
            com_dict[com.replace("\n", "")] = 0

        com_dict["Пустышка"] = 0
        # count win
        for el in file_list[1:]:
            if el.count("-") < 5:
                com = el[:45].strip()
                score = el[45:].strip()
                com_dict[com] += int(score)

        # save results from 1 tour
        res = open(f"{game}/результат_1_{game}.txt", "w", encoding="utf-8")
        com_file = open(f"{game}/команды_{game}.txt", "a", encoding="utf-8")
        for i in range(0, 10):
            k = 0
            for pair in com_dict.items():
                if pair[1] == i and pair[0] != "Пустышка":
                    res.write(pair[0] + ": " + str(i) + "\n")
                    k += 1
            if k % 2 != 0 and i != 0:
                res.write("Пустышка" + ": " + str(i) + "\n")
            res.write("\n")

        # del commands
        res = open(f"{game}/результат_1_{game}.txt", "r", encoding="utf-8")
        new_res = []

        for c in res.readlines():
            if c.split(": ")[0] not in com_del:
                new_res.append(c)
        res.close()

        res = open(f"{game}/результат_1_{game}.txt", "w", encoding="utf-8")

        for c in new_res:
            res.write(f"{c}")

        res.close()
        # end

        fp = open(f"{game}/пересечение_команд_{game}.json", "r", encoding="utf-8")
        commands_dict = json.load(fp)

        commands_dict["Пустышка"] = []

        add_com_file = open(f"{game}/{game}_1_доб.txt", "w", encoding="utf-8")

        if com_add[0] != "":
            # for c in com_add:
            #     if list(c).count(" ") < 3:
            #         res.write(f"{c}: 0\n")
            #         com_file.write(f"\n{c}")
            #         commands_dict[c] = []
            #         add_com_file.write(c + "\n")

            # ADD NEW

            res = open(f"{game}/результат_1_{game}.txt", "a", encoding="utf-8")
            res.write("\n")
            com_file_list = []
            for i in range(0, len(com_add), 2):
                    com_1 = com_add[i][:len(com_add[i])-2].strip()
                    count_1 = int(com_add[i][len(com_add[i])-2:].strip())
                    com_2 = com_add[i+1][:len(com_add[i+1]) - 2].strip()
                    count_2 = int(com_add[i+1][len(com_add[i+1]) - 2:].strip())
                    res.write(f"{com_1}: {count_1}\n")
                    res.write(f"{com_2}: {count_2}\n")
                    com_file_list.append(com_1)
                    com_file_list.append(com_2)
                    commands_dict[com_1] = [com_2]
                    commands_dict[com_2] = [com_1]
                    add_com_file.write(com_1 + "\n")
                    add_com_file.write(com_2 + "\n")
            com_file.write("\n".join(com_file_list))
        with open(f"{game}/пересечение_команд_{game}.json", "w", encoding="utf-8") as fp:
                s = json.dumps(commands_dict, ensure_ascii=False)
                fp.write(s)

        res.close()
        # new tour
        file_count = open(f"{game}/{game}_туры.txt", "w", encoding="utf-8")
        file_count.write("2")
        file_count.close()

         # generate shedule (photo)
        font_ = ImageFont.truetype("fonts/BebasNeueProExpandedExtraBoldIt.ttf", 40)
        font_c = ImageFont.truetype("fonts/BebasNeueProExpandedExtraBoldIt.ttf", 35)

        if div_name == "МСКЛ":
            base_img = Image.open('shedule/back1.png')
            game_ = Image.open(f'shedule/{game_name}.png').resize((220, 220))
            Image.Image.paste(base_img, game_, (1650, 90), mask=game_)
            drawer = ImageDraw.Draw(base_img)

            height = 402

            file = open(f"{game}/{game}_тур1.txt", "r", encoding="utf-8")
            file_list = []
            for line in file.readlines()[2:]:
                if line.count("----------"):
                    pass
                else:
                    file_list.append(line.replace("\n", "").strip())

            shuffle(file_list)

            file = open(f"{game}/{game}_тур1.txt", "w", encoding="utf-8")
            num = 1
            title = "КОМАНДЫ" + " " * 35 + "|СЧЁТ\n"
            file.write(title)
            file.write("-" * len(title) + "\n")
            for command in file_list:
                file.write(command.replace("\n", "").ljust(35) + "\n")
                if num % 2 == 0:
                    file.write("-" * len(title) + "\n")
                num += 1

            file = open(f"{game}/{game}_тур1.txt", "r", encoding="utf-8")
            file.seek(0)
            c = ((len(file.readlines()) - 23) // 3)
            count_photo = 0
            while c > 0:
                count_photo += 1
                c -= 11

            file.seek(0)
            other = 0
            for line in file.readlines():
                if line.count("----------------------------------") > 0:
                    other += 1
            file.seek(0)
            file.seek(0)
            file.readline()
            file.readline()

            for _ in range(7):
                line = file.readline()
                team_1 = line[:45].strip()
                total_1 = line[45:].strip()
                line = file.readline()
                team_2 = line[:45].strip()
                total_2 = line[45:].strip()
                file.readline()
                drawer.text((150, height), team_1, font=font_c, fill='white')
                drawer.text((1180, height), team_2, font=font_c, fill='white')
                height += 90

            base_img.save(f'{game}/shedule_1.png', quality=100)

            for i in range(1, count_photo + 1):
                height = 65
                base_img_copy = Image.open('shedule/back2.png')
                drawer = ImageDraw.Draw(base_img_copy)
                for _ in range(11):
                    line = file.readline()
                    team_1 = line[:45].strip()
                    line = file.readline()
                    team_2 = line[:45].strip()
                    file.readline()
                    drawer.text((120, height), team_1, font=font_c, fill='white')
                    drawer.text((1180, height), team_2, font=font_c, fill='white')
                    height += 90.5
                base_img_copy.save(f'{game}/shedule_1_{i}.png', quality=100)
                height = 63

        else:
            base_img = Image.open('shedule/base.png')
            div = Image.open(f'shedule/{div_name}.png').resize((250, 278))
            Image.Image.paste(base_img, div, (1570, 76), mask=div)
            game_ = Image.open(f'shedule/{game_name}.png').resize((220, 220))
            Image.Image.paste(base_img, game_, (1274, 90), mask=game_)
            drawer = ImageDraw.Draw(base_img)
            tour_ = 1
            drawer.text((55, 65), str(tour_) + " ТУР", font=font_, fill='white')
            drawer.text((55, 98), "", font=font_, fill='white')

            height = 415


            file = open(f"{game}/{game}_тур1.txt", "r", encoding="utf-8")
            c = ((len(file.readlines()) - 2) // 3)
            count_photo = 0
            while c > 0:
                count_photo += 1
                c -= 5

            file.seek(0)
            other = 0
            for line in file.readlines():
                if line.count("----------------------------------") > 0:
                    other += 1
            file.seek(0)
            file.seek(0)
            file.readline()
            file.readline()

            base_img.save(f'{game}/shedule_1.png', quality=100)

            for i in range(1, count_photo + 1):
                base_img_copy = Image.open(f'{game}/shedule_1.png')
                drawer = ImageDraw.Draw(base_img_copy)
                for _ in range(5):
                    line = file.readline()
                    team_1 = line[:45].strip()
                    total_1 = line[45:].strip()
                    line = file.readline()
                    team_2 = line[:45].strip()
                    total_2 = line[45:].strip()
                    file.readline()
                    drawer.text((120, height), team_1, font=font_c, fill='white')
                    drawer.text((1180, height), team_2, font=font_c, fill='white')
                    drawer.text((820, height), total_1, font=font_c, fill='white')
                    drawer.text((1085, height), total_2, font=font_c, fill='white')
                    height += 134
                base_img_copy.save(f'{game}/shedule_1_{i}.png', quality=100)
                height = 415
            # ------ end ------




        data = {"message": "ok"}
        return JsonResponse(data)


def reset_1(request):
    if request.method == 'GET':
        game = request.GET.get("name")
        file_count = open(f"{game}/{game}_туры.txt", "w", encoding="utf-8")
        file_count.write("1")
        file_count.close()

        add_com_list = []
        for i in range(1, 8):
            if os.path.exists(f"{game}/{game}_{i}_доб.txt"):
                add_com_list += [c.replace("\n", "") for c in
                                 open(f"{game}/{game}_{i}_доб.txt", "r", encoding="utf-8").readlines()]
        com_list = [c.replace("\n", "") for c in open(f"{game}/команды_{game}.txt", "r", encoding="utf-8").readlines()]
        com_list_new = []

        for c in com_list:
            if c not in add_com_list:
                com_list_new.append(c)

        com_file = open(f"{game}/команды_{game}.txt", "w", encoding="utf-8")
        for i in range(len(com_list_new)):
            if i == 0:
                com_file.write(com_list_new[i])
            else:
                com_file.write("\n" + com_list_new[i])

        f = open(f"{game}/{game}_тур2.txt", "w", encoding="utf-8")


        fp = open(f"{game}/пересечение_команд_{game}.json", "r", encoding="utf-8")
        commands_dict = json.load(fp)

        for key in commands_dict.keys():
            if key != "Пустышка" and len(commands_dict[key]) != 0:
                commands_dict[key] = [commands_dict[key][0]]


        with open(f"{game}/пересечение_команд_{game}.json", "w", encoding="utf-8") as fp:
            s = json.dumps(commands_dict, ensure_ascii=False)
            fp.write(s)


        data = {"message": "ok"}
        return JsonResponse(data)


def save_tour_2(request):
    if request.method == 'GET':
        checkbox = list(request.GET.get("data"))
        game = request.GET.get("name")
        game_name, div_name = game.split()
        com_del = request.GET.get("del").split("\n")
       
        file = open(f"{game}/{game}_счёт_2.txt", "w", encoding="utf-8")
        file.write(" ".join(checkbox))
        file.close()
        file = open(f"{game}/{game}_тур2.txt", "r", encoding="utf-8")
        file_list = []
        i = 0

        for line in file.readlines():
            if line.count("КОМАНДЫ") or line.count("---------------") or line.count(" ") > 40:
                file_list.append(line)
            else:
                new_line = line.replace("\n", "")
                # l1 = new_line[:len(line) // 2]
                # l2 = new_line[len(line) // 2:].replace("1", "").replace("0", "")
                l1 = new_line[:45]
                new_line = l1 + " " * 20 + checkbox[i] + "\n"
                file_list.append(new_line)
                i += 1

        file.close()

        file = open(f"{game}/{game}_тур2.txt", "w", encoding="utf-8")
        for el in file_list:
            file.write(el)
        file.close()

        # # init dict with commands

        file_res = open(f"{game}/результат_1_{game}.txt", "r", encoding="utf-8")
        com_dict = {}
        for line in file_res.readlines():
            if line.count(": ") > 0:
                com_dict[line.split(": ")[0]] = int(line.split(": ")[1])

        com_dict["Пустышка"] = 0
        # count win
        for el in file_list[1:]:
            if el.count("-") < 5:
                com = el[:45].strip()
                score = el[45:].strip()
                com_dict[com] += int(score)

        # save results from 2 tour
        res = open(f"{game}/результат_2_{game}.txt", "w", encoding="utf-8")
        for i in range(0, 10):
            k = 0
            for pair in com_dict.items():
                if pair[1] == i and pair[0] != "Пустышка":
                    res.write(pair[0] + ": " + str(i) + "\n")
                    k += 1
            if k % 2 != 0 and i != 0:
                res.write("Пустышка" + ": " + str(i) + "\n")
            res.write("\n")
        res.close()

        # del commands
        res = open(f"{game}/результат_2_{game}.txt", "r", encoding="utf-8")
        new_res = []

        for c in res.readlines():
            if c.split(": ")[0] not in com_del:
                new_res.append(c)
        res.close()

        res = open(f"{game}/результат_2_{game}.txt", "w", encoding="utf-8")

        for c in new_res:
            res.write(f"{c}")

        res.close()
        # end

        fp = open(f"{game}/пересечение_команд_{game}.json", "r", encoding="utf-8")
        commands_dict = json.load(fp)

        commands_dict["Пустышка"] = []

        res = open(f"{game}/результат_2_{game}.txt", "a", encoding="utf-8")
        com_file = open(f"{game}/команды_{game}.txt", "a", encoding="utf-8")
        com_add = request.GET.get("com").split("\n")

        add_com_file = open(f"{game}/{game}_2_доб.txt", "w", encoding="utf-8")

        if com_add[0] != "":
            for c in com_add:
                if list(c).count(" ") < 3:
                    res.write(f"{c[:len(c)-2]}: {c[len(c)-1:]}\n")
                    com_file.write(f"\n{c[:len(c)-2]}")
                    commands_dict[c[:len(c)-2]] = []
                    add_com_file.write(c[:len(c)-2] + "\n")

        with open(f"{game}/пересечение_команд_{game}.json", "w", encoding="utf-8") as fp:
                s = json.dumps(commands_dict, ensure_ascii=False)
                fp.write(s)


        # new tour
        file_count = open(f"{game}/{game}_туры.txt", "w", encoding="utf-8")
        file_count.write("3")
        file_count.close()



        if div_name != "МСКЛ":
            # generate shedule (photo)
            font_ = ImageFont.truetype("fonts/BebasNeueProExpandedExtraBoldIt.ttf", 40)
            font_c = ImageFont.truetype("fonts/BebasNeueProExpandedExtraBoldIt.ttf", 35)
            base_img = Image.open('shedule/base.png')
            div = Image.open(f'shedule/{div_name}.png').resize((250, 278))
            Image.Image.paste(base_img, div, (1570, 76), mask=div)
            game_ = Image.open(f'shedule/{game_name}.png').resize((220, 220))
            Image.Image.paste(base_img, game_, (1274, 90), mask=game_)
            drawer = ImageDraw.Draw(base_img)
            drawer.text((55, 65), "2 ТУР", font=font_, fill='white')
            drawer.text((55, 98), "", font=font_, fill='white')

            height = 415

            file = open(f"{game}/{game}_тур2.txt", "r", encoding="utf-8")
            c = ((len(file.readlines()) - 2) // 3)
            count_photo = 0
            while c > 0:
                count_photo += 1
                c -= 5

            file.seek(0)
            other = 0
            for line in file.readlines():
                if line.count("----------------------------------") > 0:
                    other += 1
            file.seek(0)
            file.seek(0)
            file.readline()
            file.readline()

            base_img.save(f'{game}/shedule_2.png', quality=100)

            for i in range(1, count_photo + 1):
                base_img_copy = Image.open(f'{game}/shedule_2.png')
                drawer = ImageDraw.Draw(base_img_copy)
                for _ in range(5):
                    line = file.readline()
                    team_1 = line[:45].strip()
                    total_1 = line[45:].strip()
                    line = file.readline()
                    team_2 = line[:45].strip()
                    total_2 = line[45:].strip()
                    file.readline()
                    drawer.text((120, height), team_1, font=font_c, fill='white')
                    drawer.text((1180, height), team_2, font=font_c, fill='white')
                    drawer.text((820, height), total_1, font=font_c, fill='white')
                    drawer.text((1085, height), total_2, font=font_c, fill='white')
                    height += 134
                base_img_copy.save(f'{game}/shedule_2_{i}.png', quality=100)
                height = 415
            # ------ end ------

        data = {"message": "ok"}
        return JsonResponse(data)


def reset_2(request):
    if request.method == 'GET':
        game = request.GET.get("name")
        file_count = open(f"{game}/{game}_туры.txt", "w", encoding="utf-8")
        file_count.write("2")
        file_count.close()

        add_com_list = []
        for i in range(2, 8):
            if os.path.exists(f"{game}/{game}_{i}_доб.txt"):
                add_com_list += [c.replace("\n", "") for c in
                                 open(f"{game}/{game}_{i}_доб.txt", "r", encoding="utf-8").readlines()]
        com_list = [c.replace("\n", "") for c in open(f"{game}/команды_{game}.txt", "r", encoding="utf-8").readlines()]
        com_list_new = []

        for c in com_list:
            if c not in add_com_list:
                com_list_new.append(c)

        com_file = open(f"{game}/команды_{game}.txt", "w", encoding="utf-8")
        for i in range(len(com_list_new)):
            if i == 0:
                com_file.write(com_list_new[i])
            else:
                com_file.write("\n" + com_list_new[i])

        f = open(f"{game}/{game}_тур3.txt", "w", encoding="utf-8")


        fp = open(f"{game}/пересечение_команд_{game}.json", "r", encoding="utf-8")
        commands_dict = json.load(fp)

        for key in commands_dict.keys():
            if key != "Пустышка":
                commands_dict[key] = [commands_dict[key][0]]


        with open(f"{game}/пересечение_команд_{game}.json", "w", encoding="utf-8") as fp:
            s = json.dumps(commands_dict, ensure_ascii=False)
            fp.write(s)



        data = {"message": "ok"}
        return JsonResponse(data)


def save_tour_3(request):
    if request.method == 'GET':
        checkbox = list(request.GET.get("data"))
        game = request.GET.get("name")
        com_del = request.GET.get("del").split("\n")
        game_name, div_name = game.split()
        file = open(f"{game}/{game}_счёт_3.txt", "w", encoding="utf-8")
        file.write(" ".join(checkbox))
        file.close()
        file = open(f"{game}/{game}_тур3.txt", "r", encoding="utf-8")
        file_list = []
        i = 0

        for line in file.readlines():
            if line.count("КОМАНДЫ") or line.count("---------------") or line.count(" ") > 40:
                file_list.append(line)
            else:
                new_line = line.replace("\n", "")
                # l1 = new_line[:len(line) // 2]
                # l2 = new_line[len(line) // 2:].replace("1", "").replace("0", "")
                l1 = new_line[:45]
                new_line = l1 + " " * 20 + checkbox[i] + "\n"
                file_list.append(new_line)
                i += 1

        file.close()

        file = open(f"{game}/{game}_тур3.txt", "w", encoding="utf-8")
        for el in file_list:
            file.write(el)
        file.close()

        # init dict with commands

        file_res = open(f"{game}/результат_2_{game}.txt", "r", encoding="utf-8")
        com_dict = {}
        for line in file_res.readlines():
            if line.count(": ") > 0:
                com_dict[line.split(": ")[0]] = int(line.split(": ")[1])

        # count win
        for el in file_list[1:]:
            if el.count("-") < 5:
                com = el[:45].strip()
                score = el[45:].strip()
                if com != "Пустышка":
                    com_dict[com] += int(score)

        # save results from 3 tour
        res = open(f"{game}/результат_3_{game}.txt", "w", encoding="utf-8")
        for i in range(0, 10):
            k = 0
            for pair in com_dict.items():
                if pair[1] == i and pair[0] != "Пустышка":
                    res.write(pair[0] + ": " + str(i) + "\n")
                    k += 1
            if k % 2 != 0 and i != 0:
                res.write("Пустышка" + ": " + str(i) + "\n")
            res.write("\n")
        res.close()

        # del commands
        res = open(f"{game}/результат_3_{game}.txt", "r", encoding="utf-8")
        new_res = []

        for c in res.readlines():
            if c.split(": ")[0] not in com_del:
                new_res.append(c)
        res.close()

        res = open(f"{game}/результат_3_{game}.txt", "w", encoding="utf-8")

        for c in new_res:
            res.write(f"{c}")

        res.close()
        # end

        fp = open(f"{game}/пересечение_команд_{game}.json", "r", encoding="utf-8")
        commands_dict = json.load(fp)

        commands_dict["Пустышка"] = []

        res = open(f"{game}/результат_3_{game}.txt", "a", encoding="utf-8")
        com_file = open(f"{game}/команды_{game}.txt", "a", encoding="utf-8")
        com_add = request.GET.get("com").split("\n")

        add_com_file = open(f"{game}/{game}_3_доб.txt", "w", encoding="utf-8")


        if com_add[0] != "":
            for c in com_add:
                if list(c).count(" ") < 3:
                    res.write(f"{c[:len(c) - 2]}: {c[len(c) - 1:]}\n")
                    com_file.write(f"\n{c[:len(c) - 2]}")
                    commands_dict[c[:len(c) - 2]] = []
                    add_com_file.write(c[:len(c) - 2] + "\n")


        with open(f"{game}/пересечение_команд_{game}.json", "w", encoding="utf-8") as fp:
                s = json.dumps(commands_dict, ensure_ascii=False)
                fp.write(s)


        # new tour
        file_count = open(f"{game}/{game}_туры.txt", "w", encoding="utf-8")
        file_count.write("4")
        file_count.close()

        if div_name != "МСКЛ":
            # generate shedule (photo)
            font_ = ImageFont.truetype("fonts/BebasNeueProExpandedExtraBoldIt.ttf", 40)
            font_c = ImageFont.truetype("fonts/BebasNeueProExpandedExtraBoldIt.ttf", 35)
            base_img = Image.open('shedule/base.png')
            div = Image.open(f'shedule/{div_name}.png').resize((250, 278))
            Image.Image.paste(base_img, div, (1570, 76), mask=div)
            game_ = Image.open(f'shedule/{game_name}.png').resize((220, 220))
            Image.Image.paste(base_img, game_, (1274, 90), mask=game_)
            drawer = ImageDraw.Draw(base_img)
            drawer.text((55, 65), "3 ТУР", font=font_, fill='white')
            drawer.text((55, 98), "", font=font_, fill='white')

            height = 415

            file = open(f"{game}/{game}_тур3.txt", "r", encoding="utf-8")
            c = ((len(file.readlines()) - 2) // 3)
            count_photo = 0
            while c > 0:
                count_photo += 1
                c -= 5

            file.seek(0)
            other = 0
            for line in file.readlines():
                if line.count("----------------------------------") > 0:
                    other += 1
            file.seek(0)
            file.seek(0)
            file.readline()
            file.readline()

            base_img.save(f'{game}/shedule_3.png', quality=100)

            for i in range(1, count_photo + 1):
                base_img_copy = Image.open(f'{game}/shedule_3.png')
                drawer = ImageDraw.Draw(base_img_copy)
                for _ in range(5):
                    line = file.readline()
                    team_1 = line[:45].strip()
                    total_1 = line[45:].strip()
                    line = file.readline()
                    team_2 = line[:45].strip()
                    total_2 = line[45:].strip()
                    file.readline()
                    drawer.text((120, height), team_1, font=font_c, fill='white')
                    drawer.text((1180, height), team_2, font=font_c, fill='white')
                    drawer.text((820, height), total_1, font=font_c, fill='white')
                    drawer.text((1085, height), total_2, font=font_c, fill='white')
                    height += 134
                base_img_copy.save(f'{game}/shedule_3_{i}.png', quality=100)
                height = 415
            # ------ end ------


        data = {"message": "ok"}
        return JsonResponse(data)


def reset_3(request):
    if request.method == 'GET':
        game = request.GET.get("name")
        file_count = open(f"{game}/{game}_туры.txt", "w", encoding="utf-8")
        file_count.write("3")
        file_count.close()

        add_com_list = []
        for i in range(3, 8):
            if os.path.exists(f"{game}/{game}_{i}_доб.txt"):
                add_com_list += [c.replace("\n", "") for c in
                                 open(f"{game}/{game}_{i}_доб.txt", "r", encoding="utf-8").readlines()]
        com_list = [c.replace("\n", "") for c in open(f"{game}/команды_{game}.txt", "r", encoding="utf-8").readlines()]
        com_list_new = []

        for c in com_list:
            if c not in add_com_list:
                com_list_new.append(c)

        com_file = open(f"{game}/команды_{game}.txt", "w", encoding="utf-8")
        for i in range(len(com_list_new)):
            if i == 0:
                com_file.write(com_list_new[i])
            else:
                com_file.write("\n" + com_list_new[i])

        f = open(f"{game}/{game}_тур4.txt", "w", encoding="utf-8")



        fp = open(f"{game}/пересечение_команд_{game}.json", "r", encoding="utf-8")
        commands_dict = json.load(fp)

        for key in commands_dict.keys():
            commands_dict[key] = commands_dict[key][0:3]

        with open(f"{game}/пересечение_команд_{game}.json", "w", encoding="utf-8") as fp:
            s = json.dumps(commands_dict, ensure_ascii=False)
            fp.write(s)

        data = {"message": "ok"}
        return JsonResponse(data)


def save_tour_4(request):
    if request.method == 'GET':
        checkbox = list(request.GET.get("data"))
        game = request.GET.get("name")
        game_name, div_name = game.split()
        file = open(f"{game}/{game}_счёт_4.txt", "w", encoding="utf-8")
        file.write(" ".join(checkbox))
        file.close()
        file = open(f"{game}/{game}_тур4.txt", "r", encoding="utf-8")
        file_list = []
        i = 0


        for line in file.readlines():
            if line.count("КОМАНДЫ") or line.count("---------------") or line.count(" ") > 40:
                file_list.append(line)
            else:
                new_line = line.replace("\n", "")
                # l1 = new_line[:len(line) // 2]
                # l2 = new_line[len(line) // 2:].replace("1", "").replace("0", "")
                l1 = new_line[:45]
                new_line = l1 + " " * 20 + checkbox[i] + "\n"
                file_list.append(new_line)
                i += 1

        file.close()

        file = open(f"{game}/{game}_тур4.txt", "w", encoding="utf-8")
        for el in file_list:
            file.write(el)
        file.close()

        # init dict with commands

        file_res = open(f"{game}/результат_3_{game}.txt", "r", encoding="utf-8")
        com_dict = {}
        for line in file_res.readlines():
            if line.count(": ") > 0:
                com_dict[line.split(": ")[0]] = int(line.split(": ")[1])

        # count win
        for el in file_list[1:]:
            if el.count("-") < 5:
                com = el[:45].strip()
                score = el[45:].strip()
                com_dict[com] += int(score)

        # save results from 3 tour
        res = open(f"{game}/результат_4_{game}.txt", "w", encoding="utf-8")
        for i in range(0, 10):
            k = 0
            for pair in com_dict.items():
                if pair[1] == i and pair[0] != "Пустышка":
                    res.write(pair[0] + ": " + str(i) + "\n")
                    k += 1
            if k % 2 != 0 and i != 0:
                res.write("Пустышка" + ": " + str(i) + "\n")
            res.write("\n")
        res.close()



        fp = open(f"{game}/пересечение_команд_{game}.json", "r", encoding="utf-8")
        commands_dict = json.load(fp)

        commands_dict["Пустышка"] = []

        res = open(f"{game}/результат_4_{game}.txt", "a", encoding="utf-8")
        com_file = open(f"{game}/команды_{game}.txt", "a", encoding="utf-8")
        com_add = request.GET.get("com").split("\n")

        add_com_file = open(f"{game}/{game}_4_доб.txt", "w", encoding="utf-8")

        if com_add[0] != "":
            for c in com_add:
                if list(c).count(" ") < 3:
                    res.write(f"{c[:len(c) - 2]}: {c[len(c) - 1:]}\n")
                    com_file.write(f"\n{c[:len(c) - 2]}")
                    commands_dict[c[:len(c) - 2]] = []
                    add_com_file.write(c[:len(c) - 2] + "\n")

        with open(f"{game}/пересечение_команд_{game}.json", "w", encoding="utf-8") as fp:
                s = json.dumps(commands_dict, ensure_ascii=False)
                fp.write(s)


        # new tour
        file_count = open(f"{game}/{game}_туры.txt", "w", encoding="utf-8")
        file_count.write("5")
        file_count.close()

        if div_name != "МСКЛ":
            # generate shedule (photo)
            font_ = ImageFont.truetype("fonts/BebasNeueProExpandedExtraBoldIt.ttf", 40)
            font_c = ImageFont.truetype("fonts/BebasNeueProExpandedExtraBoldIt.ttf", 35)
            base_img = Image.open('shedule/base.png')
            div = Image.open(f'shedule/{div_name}.png').resize((250, 278))
            Image.Image.paste(base_img, div, (1570, 76), mask=div)
            game_ = Image.open(f'shedule/{game_name}.png').resize((220, 220))
            Image.Image.paste(base_img, game_, (1274, 90), mask=game_)
            drawer = ImageDraw.Draw(base_img)
            tour_ = 1
            drawer.text((55, 65), "4 ТУР", font=font_, fill='white')
            drawer.text((55, 98), "", font=font_, fill='white')

            height = 415

            file = open(f"{game}/{game}_тур4.txt", "r", encoding="utf-8")
            c = ((len(file.readlines()) - 2) // 3)
            count_photo = 0
            while c > 0:
                count_photo += 1
                c -= 5

            file.seek(0)
            other = 0
            for line in file.readlines():
                if line.count("----------------------------------") > 0:
                    other += 1
            file.seek(0)
            file.seek(0)
            file.readline()
            file.readline()

            base_img.save(f'{game}/shedule_4.png', quality=100)

            for i in range(1, count_photo + 1):
                base_img_copy = Image.open(f'{game}/shedule_4.png')
                drawer = ImageDraw.Draw(base_img_copy)
                for _ in range(5):
                    line = file.readline()
                    team_1 = line[:45].strip()
                    total_1 = line[45:].strip()
                    line = file.readline()
                    team_2 = line[:45].strip()
                    total_2 = line[45:].strip()
                    file.readline()
                    drawer.text((120, height), team_1, font=font_c, fill='white')
                    drawer.text((1180, height), team_2, font=font_c, fill='white')
                    drawer.text((820, height), total_1, font=font_c, fill='white')
                    drawer.text((1085, height), total_2, font=font_c, fill='white')
                    height += 134
                base_img_copy.save(f'{game}/shedule_4_{i}.png', quality=100)
                height = 415
            # ------ end ------


        data = {"message": "ok"}
        return JsonResponse(data)


def reset_4(request):
    if request.method == 'GET':
        game = request.GET.get("name")
        file_count = open(f"{game}/{game}_туры.txt", "w", encoding="utf-8")
        file_count.write("4")
        file_count.close()

        add_com_list = []
        for i in range(4, 8):
            if os.path.exists(f"{game}/{game}_{i}_доб.txt"):
                add_com_list += [c.replace("\n", "") for c in
                                 open(f"{game}/{game}_{i}_доб.txt", "r", encoding="utf-8").readlines()]
        com_list = [c.replace("\n", "") for c in open(f"{game}/команды_{game}.txt", "r", encoding="utf-8").readlines()]
        com_list_new = []

        for c in com_list:
            if c not in add_com_list:
                com_list_new.append(c)

        com_file = open(f"{game}/команды_{game}.txt", "w", encoding="utf-8")
        for i in range(len(com_list_new)):
            if i == 0:
                com_file.write(com_list_new[i])
            else:
                com_file.write("\n" + com_list_new[i])

        f = open(f"{game}/{game}_тур5.txt", "w", encoding="utf-8")



        fp = open(f"{game}/пересечение_команд_{game}.json", "r", encoding="utf-8")
        commands_dict = json.load(fp)

        for key in commands_dict.keys():
            commands_dict[key] = commands_dict[key][0:4]

        with open(f"{game}/пересечение_команд_{game}.json", "w", encoding="utf-8") as fp:
            s = json.dumps(commands_dict, ensure_ascii=False)
            fp.write(s)


        data = {"message": "ok"}
        return JsonResponse(data)



def save_tour_5(request):
    if request.method == 'GET':
        checkbox = list(request.GET.get("data"))
        game = request.GET.get("name")
        game_name, div_name = game.split()
        file = open(f"{game}/{game}_счёт_5.txt", "w", encoding="utf-8")
        file.write(" ".join(checkbox))
        file.close()
        file = open(f"{game}/{game}_тур5.txt", "r", encoding="utf-8")
        file_list = []
        i = 0


        for line in file.readlines():
            if line.count("КОМАНДЫ") or line.count("---------------") or line.count(" ") > 40:
                file_list.append(line)
            else:
                new_line = line.replace("\n", "")
                # l1 = new_line[:len(line) // 2]
                # l2 = new_line[len(line) // 2:].replace("1", "").replace("0", "")
                l1 = new_line[:45]
                new_line = l1 + " " * 20 + checkbox[i] + "\n"
                file_list.append(new_line)
                i += 1

        file.close()

        file = open(f"{game}/{game}_тур5.txt", "w", encoding="utf-8")
        for el in file_list:
            file.write(el)
        file.close()

        # init dict with commands

        file_res = open(f"{game}/результат_4_{game}.txt", "r", encoding="utf-8")
        com_dict = {}
        for line in file_res.readlines():
            if line.count(": ") > 0:
                com_dict[line.split(": ")[0]] = int(line.split(": ")[1])

        # count win
        for el in file_list[1:]:
            if el.count("-") < 5:
                com = el[:45].strip()
                score = el[45:].strip()
                com_dict[com] += int(score)

        # save results from 3 tour
        res = open(f"{game}/результат_5_{game}.txt", "w", encoding="utf-8")
        for i in range(0, 10):
            k = 0
            for pair in com_dict.items():
                if pair[1] == i and pair[0] != "Пустышка":
                    res.write(pair[0] + ": " + str(i) + "\n")
                    k += 1
            if k % 2 != 0 and i != 0:
                res.write("Пустышка" + ": " + str(i) + "\n")
            res.write("\n")
        res.close()

        # del commands
        res = open(f"{game}/результат_5_{game}.txt", "r", encoding="utf-8")
        new_res = []

        for c in res.readlines():
            if c.split(": ")[0] not in com_del:
                new_res.append(c)
        res.close()

        res = open(f"{game}/результат_5_{game}.txt", "w", encoding="utf-8")

        for c in new_res:
            res.write(f"{c}")

        res.close()
        # end

        fp = open(f"{game}/пересечение_команд_{game}.json", "r", encoding="utf-8")
        commands_dict = json.load(fp)

        commands_dict["Пустышка"] = []

        res = open(f"{game}/результат_5_{game}.txt", "a", encoding="utf-8")
        com_file = open(f"{game}/команды_{game}.txt", "a", encoding="utf-8")
        com_add = request.GET.get("com").split("\n")

        add_com_file = open(f"{game}/{game}_5_доб.txt", "w", encoding="utf-8")

        if com_add[0] != "":
            for c in com_add:
                if list(c).count(" ") < 3:
                    res.write(f"{c[:len(c) - 2]}: {c[len(c) - 1:]}\n")
                    com_file.write(f"\n{c[:len(c) - 2]}")
                    commands_dict[c[:len(c) - 2]] = []
                    add_com_file.write(c[:len(c) - 2] + "\n")

        with open(f"{game}/пересечение_команд_{game}.json", "w", encoding="utf-8") as fp:
                s = json.dumps(commands_dict, ensure_ascii=False)
                fp.write(s)


        # new tour
        file_count = open(f"{game}/{game}_туры.txt", "w", encoding="utf-8")
        file_count.write("6")
        file_count.close()

        # generate shedule (photo)
        font_ = ImageFont.truetype("fonts/BebasNeueProExpandedExtraBoldIt.ttf", 40)
        font_c = ImageFont.truetype("fonts/BebasNeueProExpandedExtraBoldIt.ttf", 35)
        base_img = Image.open('shedule/base.png')
        div = Image.open(f'shedule/{div_name}.png').resize((250, 278))
        Image.Image.paste(base_img, div, (1570, 76), mask=div)
        game_ = Image.open(f'shedule/{game_name}.png').resize((220, 220))
        Image.Image.paste(base_img, game_, (1274, 90), mask=game_)
        drawer = ImageDraw.Draw(base_img)
        tour_ = 1
        drawer.text((55, 65), "5 ТУР", font=font_, fill='white')
        drawer.text((55, 98), "", font=font_, fill='white')

        height = 415

        file = open(f"{game}/{game}_тур5.txt", "r", encoding="utf-8")
        c = ((len(file.readlines()) - 2) // 3)
        count_photo = 0
        while c > 0:
            count_photo += 1
            c -= 5

        file.seek(0)
        other = 0
        for line in file.readlines():
            if line.count("----------------------------------") > 0:
                other += 1
        file.seek(0)
        file.seek(0)
        file.readline()
        file.readline()

        base_img.save(f'{game}/shedule_5.png', quality=100)

        for i in range(1, count_photo + 1):
            base_img_copy = Image.open(f'{game}/shedule_5.png')
            drawer = ImageDraw.Draw(base_img_copy)
            for _ in range(5):
                line = file.readline()
                team_1 = line[:45].strip()
                total_1 = line[45:].strip()
                line = file.readline()
                team_2 = line[:45].strip()
                total_2 = line[45:].strip()
                file.readline()
                drawer.text((120, height), team_1, font=font_c, fill='white')
                drawer.text((1180, height), team_2, font=font_c, fill='white')
                drawer.text((820, height), total_1, font=font_c, fill='white')
                drawer.text((1085, height), total_2, font=font_c, fill='white')
                height += 134
            base_img_copy.save(f'{game}/shedule_5_{i}.png', quality=100)
            height = 415
        # ------ end ------


        data = {"message": "ok"}
        return JsonResponse(data)


def reset_5(request):
    if request.method == 'GET':
        game = request.GET.get("name")
        file_count = open(f"{game}/{game}_туры.txt", "w", encoding="utf-8")
        file_count.write("5")
        file_count.close()

        add_com_list = []
        for i in range(5, 8):
            if os.path.exists(f"{game}/{game}_{i}_доб.txt"):
                add_com_list += [c.replace("\n", "") for c in
                                 open(f"{game}/{game}_{i}_доб.txt", "r", encoding="utf-8").readlines()]
        com_list = [c.replace("\n", "") for c in open(f"{game}/команды_{game}.txt", "r", encoding="utf-8").readlines()]
        com_list_new = []

        for c in com_list:
            if c not in add_com_list:
                com_list_new.append(c)

        com_file = open(f"{game}/команды_{game}.txt", "w", encoding="utf-8")
        for i in range(len(com_list_new)):
            if i == 0:
                com_file.write(com_list_new[i])
            else:
                com_file.write("\n" + com_list_new[i])

        f = open(f"{game}/{game}_тур6.txt", "w", encoding="utf-8")


        fp = open(f"{game}/пересечение_команд_{game}.json", "r", encoding="utf-8")
        commands_dict = json.load(fp)

        for key in commands_dict.keys():
            commands_dict[key] = commands_dict[key][0:5]

        with open(f"{game}/пересечение_команд_{game}.json", "w", encoding="utf-8") as fp:
            s = json.dumps(commands_dict, ensure_ascii=False)
            fp.write(s)


        data = {"message": "ok"}
        return JsonResponse(data)


def save_tour_6(request):
    if request.method == 'GET':
        checkbox = list(request.GET.get("data"))
        game = request.GET.get("name")
        game_name, div_name = game.split()
        file = open(f"{game}/{game}_счёт_6.txt", "w", encoding="utf-8")
        file.write(" ".join(checkbox))
        file.close()
        file = open(f"{game}/{game}_тур6.txt", "r", encoding="utf-8")
        file_list = []
        i = 0

        for line in file.readlines():
            if line.count("КОМАНДЫ") or line.count("---------------") or line.count(" ") > 40:
                file_list.append(line)
            else:
                new_line = line.replace("\n", "")
                # l1 = new_line[:len(line) // 2]
                # l2 = new_line[len(line) // 2:].replace("1", "").replace("0", "")
                l1 = new_line[:45]
                new_line = l1 + " " * 20 + checkbox[i] + "\n"
                file_list.append(new_line)
                i += 1

        file.close()

        file = open(f"{game}/{game}_тур6.txt", "w", encoding="utf-8")
        for el in file_list:
            file.write(el)
        file.close()

        # init dict with commands

        file_res = open(f"{game}/результат_5_{game}.txt", "r", encoding="utf-8")
        com_dict = {}
        for line in file_res.readlines():
            if line.count(": ") > 0:
                com_dict[line.split(": ")[0]] = int(line.split(": ")[1])

        # count win
        for el in file_list[1:]:
            if el.count("-") < 5:
                com = el[:45].strip()
                score = el[45:].strip()
                com_dict[com] += int(score)

        # save results from 3 tour
        res = open(f"{game}/результат_6_{game}.txt", "w", encoding="utf-8")
        for i in range(0, 10):
            k = 0
            for pair in com_dict.items():
                if pair[1] == i and pair[0] != "Пустышка":
                    res.write(pair[0] + ": " + str(i) + "\n")
                    k += 1
            if k % 2 != 0 and i != 0:
                res.write("Пустышка" + ": " + str(i) + "\n")
            res.write("\n")
        res.close()



        fp = open(f"{game}/пересечение_команд_{game}.json", "r", encoding="utf-8")
        commands_dict = json.load(fp)

        commands_dict["Пустышка"] = []

        res = open(f"{game}/результат_6_{game}.txt", "a", encoding="utf-8")
        com_file = open(f"{game}/команды_{game}.txt", "a", encoding="utf-8")
        com_add = request.GET.get("com").split("\n")

        add_com_file = open(f"{game}/{game}_6_доб.txt", "w", encoding="utf-8")

        if com_add[0] != "":
            for c in com_add:
                if list(c).count(" ") < 3:
                    res.write(f"{c[:len(c) - 2]}: {c[len(c) - 1:]}\n")
                    com_file.write(f"\n{c[:len(c) - 2]}")
                    commands_dict[c[:len(c) - 2]] = []
                    add_com_file.write(c[:len(c) - 2] + "\n")

        with open(f"{game}/пересечение_команд_{game}.json", "w", encoding="utf-8") as fp:
                s = json.dumps(commands_dict, ensure_ascii=False)
                fp.write(s)


        # new tour
        file_count = open(f"{game}/{game}_туры.txt", "w", encoding="utf-8")
        file_count.write("7")
        file_count.close()

        # generate shedule (photo)
        font_ = ImageFont.truetype("fonts/BebasNeueProExpandedExtraBoldIt.ttf", 40)
        font_c = ImageFont.truetype("fonts/BebasNeueProExpandedExtraBoldIt.ttf", 35)
        base_img = Image.open('shedule/base.png')
        div = Image.open(f'shedule/{div_name}.png').resize((250, 278))
        Image.Image.paste(base_img, div, (1570, 76), mask=div)
        game_ = Image.open(f'shedule/{game_name}.png').resize((220, 220))
        Image.Image.paste(base_img, game_, (1274, 90), mask=game_)
        drawer = ImageDraw.Draw(base_img)
        tour_ = 1
        drawer.text((55, 65), "6 ТУР", font=font_, fill='white')
        drawer.text((55, 98), "", font=font_, fill='white')

        height = 415

        file = open(f"{game}/{game}_тур6.txt", "r", encoding="utf-8")
        c = ((len(file.readlines()) - 2) // 3)
        count_photo = 0
        while c > 0:
            count_photo += 1
            c -= 5

        file.seek(0)
        other = 0
        for line in file.readlines():
            if line.count("----------------------------------") > 0:
                other += 1
        file.seek(0)
        file.seek(0)
        file.readline()
        file.readline()

        base_img.save(f'{game}/shedule_6.png', quality=100)

        for i in range(1, count_photo + 1):
            base_img_copy = Image.open(f'{game}/shedule_6.png')
            drawer = ImageDraw.Draw(base_img_copy)
            for _ in range(5):
                line = file.readline()
                team_1 = line[:45].strip()
                total_1 = line[45:].strip()
                line = file.readline()
                team_2 = line[:45].strip()
                total_2 = line[45:].strip()
                file.readline()
                drawer.text((120, height), team_1, font=font_c, fill='white')
                drawer.text((1180, height), team_2, font=font_c, fill='white')
                drawer.text((820, height), total_1, font=font_c, fill='white')
                drawer.text((1085, height), total_2, font=font_c, fill='white')
                height += 134
            base_img_copy.save(f'{game}/shedule_6_{i}.png', quality=100)
            height = 415
        # ------ end ------


        data = {"message": "ok"}
        return JsonResponse(data)


def reset_6(request):
    if request.method == 'GET':
        game = request.GET.get("name")
        file_count = open(f"{game}/{game}_туры.txt", "w", encoding="utf-8")
        file_count.write("6")
        file_count.close()

        add_com_list = []
        for i in range(6, 8):
            if os.path.exists(f"{game}/{game}_{i}_доб.txt"):
                add_com_list += [c.replace("\n", "") for c in
                                 open(f"{game}/{game}_{i}_доб.txt", "r", encoding="utf-8").readlines()]
        com_list = [c.replace("\n", "") for c in open(f"{game}/команды_{game}.txt", "r", encoding="utf-8").readlines()]
        com_list_new = []

        for c in com_list:
            if c not in add_com_list:
                com_list_new.append(c)

        com_file = open(f"{game}/команды_{game}.txt", "w", encoding="utf-8")
        for i in range(len(com_list_new)):
            if i == 0:
                com_file.write(com_list_new[i])
            else:
                com_file.write("\n" + com_list_new[i])

        f = open(f"{game}/{game}_тур7.txt", "w", encoding="utf-8")


        fp = open(f"{game}/пересечение_команд_{game}.json", "r", encoding="utf-8")
        commands_dict = json.load(fp)

        for key in commands_dict.keys():
            commands_dict[key] = commands_dict[key][0:6]

        with open(f"{game}/пересечение_команд_{game}.json", "w", encoding="utf-8") as fp:
            s = json.dumps(commands_dict, ensure_ascii=False)
            fp.write(s)


        data = {"message": "ok"}
        return JsonResponse(data)


def save_tour_7(request):
    if request.method == 'GET':
        checkbox = list(request.GET.get("data"))
        game = request.GET.get("name")
        game_name, div_name = game.split()
        file = open(f"{game}/{game}_счёт_7.txt", "w", encoding="utf-8")
        file.write(" ".join(checkbox))
        file.close()
        file = open(f"{game}/{game}_тур7.txt", "r", encoding="utf-8")
        file_list = []
        i = 0

        for line in file.readlines():
            if line.count("КОМАНДЫ") or line.count("---------------") or line.count(" ") > 40:
                file_list.append(line)
            else:
                new_line = line.replace("\n", "")
                # l1 = new_line[:len(line) // 2]
                # l2 = new_line[len(line) // 2:].replace("1", "").replace("0", "")
                l1 = new_line[:45]
                new_line = l1 + " " * 20 + checkbox[i] + "\n"
                file_list.append(new_line)
                i += 1

        file.close()

        file = open(f"{game}/{game}_тур6.txt", "w", encoding="utf-8")
        for el in file_list:
            file.write(el)
        file.close()

        # init dict with commands

        file_res = open(f"{game}/результат_6_{game}.txt", "r", encoding="utf-8")
        com_dict = {}
        for line in file_res.readlines():
            if line.count(": ") > 0:
                com_dict[line.split(": ")[0]] = int(line.split(": ")[1])

        # count win
        for el in file_list[1:]:
            if el.count("-") < 5:
                com = el[:45].strip()
                score = el[45:].strip()
                com_dict[com] += int(score)

        # save results from 3 tour
        res = open(f"{game}/результат_7_{game}.txt", "w", encoding="utf-8")
        for i in range(0, 10):
            k = 0
            for pair in com_dict.items():
                if pair[1] == i and pair[0] != "Пустышка":
                    res.write(pair[0] + ": " + str(i) + "\n")
                    k += 1
            if k % 2 != 0 and i != 0:
                res.write("Пустышка" + ": " + str(i) + "\n")
            res.write("\n")
        res.close()



        fp = open(f"{game}/пересечение_команд_{game}.json", "r", encoding="utf-8")
        commands_dict = json.load(fp)

        commands_dict["Пустышка"] = []

        res = open(f"{game}/результат_7_{game}.txt", "a", encoding="utf-8")
        com_file = open(f"{game}/команды_{game}.txt", "a", encoding="utf-8")
        com_add = request.GET.get("com").split("\n")

        add_com_file = open(f"{game}/{game}_7_доб.txt", "w", encoding="utf-8")

        if com_add[0] != "":
            for c in com_add:
                if list(c).count(" ") < 3:
                    res.write(f"{c[:len(c) - 2]}: {c[len(c) - 1:]}\n")
                    com_file.write(f"\n{c[:len(c) - 2]}")
                    commands_dict[c[:len(c) - 2]] = []
                    add_com_file.write(c[:len(c) - 2] + "\n")

        with open(f"{game}/пересечение_команд_{game}.json", "w", encoding="utf-8") as fp:
                s = json.dumps(commands_dict, ensure_ascii=False)
                fp.write(s)


        # new tour
        file_count = open(f"{game}/{game}_туры.txt", "w", encoding="utf-8")
        file_count.write("8")
        file_count.close()

        # generate shedule (photo)
        font_ = ImageFont.truetype("fonts/BebasNeueProExpandedExtraBoldIt.ttf", 40)
        font_c = ImageFont.truetype("fonts/BebasNeueProExpandedExtraBoldIt.ttf", 35)
        base_img = Image.open('shedule/base.png')
        div = Image.open(f'shedule/{div_name}.png').resize((250, 278))
        Image.Image.paste(base_img, div, (1570, 76), mask=div)
        game_ = Image.open(f'shedule/{game_name}.png').resize((220, 220))
        Image.Image.paste(base_img, game_, (1274, 90), mask=game_)
        drawer = ImageDraw.Draw(base_img)
        tour_ = 1
        drawer.text((55, 65), "7 ТУР", font=font_, fill='white')
        drawer.text((55, 98), "", font=font_, fill='white')

        height = 415

        file = open(f"{game}/{game}_тур7.txt", "r", encoding="utf-8")
        c = ((len(file.readlines()) - 2) // 3)
        count_photo = 0
        while c > 0:
            count_photo += 1
            c -= 5

        file.seek(0)
        other = 0
        for line in file.readlines():
            if line.count("----------------------------------") > 0:
                other += 1
        file.seek(0)
        file.seek(0)
        file.readline()
        file.readline()

        base_img.save(f'{game}/shedule_7.png', quality=100)

        for i in range(1, count_photo + 1):
            base_img_copy = Image.open(f'{game}/shedule_7.png')
            drawer = ImageDraw.Draw(base_img_copy)
            for _ in range(5):
                line = file.readline()
                team_1 = line[:45].strip()
                total_1 = line[45:].strip()
                line = file.readline()
                team_2 = line[:45].strip()
                total_2 = line[45:].strip()
                file.readline()
                drawer.text((120, height), team_1, font=font_c, fill='white')
                drawer.text((1180, height), team_2, font=font_c, fill='white')
                drawer.text((820, height), total_1, font=font_c, fill='white')
                drawer.text((1085, height), total_2, font=font_c, fill='white')
                height += 134
            base_img_copy.save(f'{game}/shedule_7_{i}.png', quality=100)
            height = 415
        # ------ end ------


        data = {"message": "ok"}
        return JsonResponse(data)


def reset_7(request):
    if request.method == 'GET':
        game = request.GET.get("name")
        file_count = open(f"{game}/{game}_туры.txt", "w", encoding="utf-8")
        file_count.write("7")
        file_count.close()

        add_com_list = []
        for i in range(7, 8):
            if os.path.exists(f"{game}/{game}_{i}_доб.txt"):
                add_com_list += [c.replace("\n", "") for c in
                                 open(f"{game}/{game}_{i}_доб.txt", "r", encoding="utf-8").readlines()]
        com_list = [c.replace("\n", "") for c in open(f"{game}/команды_{game}.txt", "r", encoding="utf-8").readlines()]
        com_list_new = []

        for c in com_list:
            if c not in add_com_list:
                com_list_new.append(c)

        com_file = open(f"{game}/команды_{game}.txt", "w", encoding="utf-8")
        for i in range(len(com_list_new)):
            if i == 0:
                com_file.write(com_list_new[i])
            else:
                com_file.write("\n" + com_list_new[i])

        f = open(f"{game}/{game}_тур8.txt", "w", encoding="utf-8")


        fp = open(f"{game}/пересечение_команд_{game}.json", "r", encoding="utf-8")
        commands_dict = json.load(fp)

        for key in commands_dict.keys():
            commands_dict[key] = commands_dict[key][0:6]

        with open(f"{game}/пересечение_команд_{game}.json", "w", encoding="utf-8") as fp:
            s = json.dumps(commands_dict, ensure_ascii=False)
            fp.write(s)


        data = {"message": "ok"}
        return JsonResponse(data)


def save_tour_8(request):
    if request.method == 'GET':
        checkbox = list(request.GET.get("data"))
        game = request.GET.get("name")
        game_name, div_name = game.split()
        file = open(f"{game}/{game}_счёт_8.txt", "w", encoding="utf-8")
        file.write(" ".join(checkbox))
        file.close()
        file = open(f"{game}/{game}_тур8.txt", "r", encoding="utf-8")
        file_list = []
        i = 0

        for line in file.readlines():
            if line.count("КОМАНДЫ") or line.count("---------------") or line.count(" ") > 40:
                file_list.append(line)
            else:
                new_line = line.replace("\n", "")
                # l1 = new_line[:len(line) // 2]
                # l2 = new_line[len(line) // 2:].replace("1", "").replace("0", "")
                l1 = new_line[:45]
                new_line = l1 + " " * 20 + checkbox[i] + "\n"
                file_list.append(new_line)
                i += 1

        file.close()

        file = open(f"{game}/{game}_тур7.txt", "w", encoding="utf-8")
        for el in file_list:
            file.write(el)
        file.close()

        # init dict with commands

        file_res = open(f"{game}/результат_7_{game}.txt", "r", encoding="utf-8")
        com_dict = {}
        for line in file_res.readlines():
            if line.count(": ") > 0:
                com_dict[line.split(": ")[0]] = int(line.split(": ")[1])

        # count win
        for el in file_list[1:]:
            if el.count("-") < 5:
                com = el[:45].strip()
                score = el[45:].strip()
                com_dict[com] += int(score)

        # save results from 3 tour
        res = open(f"{game}/результат_8_{game}.txt", "w", encoding="utf-8")
        for i in range(0, 10):
            k = 0
            for pair in com_dict.items():
                if pair[1] == i and pair[0] != "Пустышка":
                    res.write(pair[0] + ": " + str(i) + "\n")
                    k += 1
            if k % 2 != 0 and i != 0:
                res.write("Пустышка" + ": " + str(i) + "\n")
            res.write("\n")
        res.close()



        fp = open(f"{game}/пересечение_команд_{game}.json", "r", encoding="utf-8")
        commands_dict = json.load(fp)

        commands_dict["Пустышка"] = []

        res = open(f"{game}/результат_8_{game}.txt", "a", encoding="utf-8")
        com_file = open(f"{game}/команды_{game}.txt", "a", encoding="utf-8")
        com_add = request.GET.get("com").split("\n")

        add_com_file = open(f"{game}/{game}_7_доб.txt", "w", encoding="utf-8")

        if com_add[0] != "":
            for c in com_add:
                if list(c).count(" ") < 3:
                    res.write(f"{c[:len(c) - 2]}: {c[len(c) - 1:]}\n")
                    com_file.write(f"\n{c[:len(c) - 2]}")
                    commands_dict[c[:len(c) - 2]] = []
                    add_com_file.write(c[:len(c) - 2] + "\n")

        with open(f"{game}/пересечение_команд_{game}.json", "w", encoding="utf-8") as fp:
                s = json.dumps(commands_dict, ensure_ascii=False)
                fp.write(s)


        # new tour
        file_count = open(f"{game}/{game}_туры.txt", "w", encoding="utf-8")
        file_count.write("9")
        file_count.close()

        # generate shedule (photo)
        font_ = ImageFont.truetype("fonts/BebasNeueProExpandedExtraBoldIt.ttf", 40)
        font_c = ImageFont.truetype("fonts/BebasNeueProExpandedExtraBoldIt.ttf", 35)
        base_img = Image.open('shedule/base.png')
        div = Image.open(f'shedule/{div_name}.png').resize((250, 278))
        Image.Image.paste(base_img, div, (1570, 76), mask=div)
        game_ = Image.open(f'shedule/{game_name}.png').resize((220, 220))
        Image.Image.paste(base_img, game_, (1274, 90), mask=game_)
        drawer = ImageDraw.Draw(base_img)
        tour_ = 1
        drawer.text((55, 65), "8 ТУР", font=font_, fill='white')
        drawer.text((55, 98), "", font=font_, fill='white')

        height = 415

        file = open(f"{game}/{game}_тур8.txt", "r", encoding="utf-8")
        c = ((len(file.readlines()) - 2) // 3)
        count_photo = 0
        while c > 0:
            count_photo += 1
            c -= 5

        file.seek(0)
        other = 0
        for line in file.readlines():
            if line.count("----------------------------------") > 0:
                other += 1
        file.seek(0)
        file.seek(0)
        file.readline()
        file.readline()

        base_img.save(f'{game}/shedule_8.png', quality=100)

        for i in range(1, count_photo + 1):
            base_img_copy = Image.open(f'{game}/shedule_8.png')
            drawer = ImageDraw.Draw(base_img_copy)
            for _ in range(5):
                line = file.readline()
                team_1 = line[:45].strip()
                total_1 = line[45:].strip()
                line = file.readline()
                team_2 = line[:45].strip()
                total_2 = line[45:].strip()
                file.readline()
                drawer.text((120, height), team_1, font=font_c, fill='white')
                drawer.text((1180, height), team_2, font=font_c, fill='white')
                drawer.text((820, height), total_1, font=font_c, fill='white')
                drawer.text((1085, height), total_2, font=font_c, fill='white')
                height += 134
            base_img_copy.save(f'{game}/shedule_8_{i}.png', quality=100)
            height = 415
        # ------ end ------


        data = {"message": "ok"}
        return JsonResponse(data)


def reset_8(request):
    if request.method == 'GET':
        game = request.GET.get("name")
        file_count = open(f"{game}/{game}_туры.txt", "w", encoding="utf-8")
        file_count.write("8")
        file_count.close()

        add_com_list = []
        for i in range(8, 8):
            if os.path.exists(f"{game}/{game}_{i}_доб.txt"):
                add_com_list += [c.replace("\n", "") for c in
                                 open(f"{game}/{game}_{i}_доб.txt", "r", encoding="utf-8").readlines()]
        com_list = [c.replace("\n", "") for c in open(f"{game}/команды_{game}.txt", "r", encoding="utf-8").readlines()]
        com_list_new = []

        for c in com_list:
            if c not in add_com_list:
                com_list_new.append(c)

        com_file = open(f"{game}/команды_{game}.txt", "w", encoding="utf-8")
        for i in range(len(com_list_new)):
            if i == 0:
                com_file.write(com_list_new[i])
            else:
                com_file.write("\n" + com_list_new[i])

        f = open(f"{game}/{game}_тур9.txt", "w", encoding="utf-8")


        fp = open(f"{game}/пересечение_команд_{game}.json", "r", encoding="utf-8")
        commands_dict = json.load(fp)

        for key in commands_dict.keys():
            commands_dict[key] = commands_dict[key][0:6]

        with open(f"{game}/пересечение_команд_{game}.json", "w", encoding="utf-8") as fp:
            s = json.dumps(commands_dict, ensure_ascii=False)
            fp.write(s)


        data = {"message": "ok"}
        return JsonResponse(data)



def new_files(request):
    if request.method == 'GET':
        name = request.GET.get("name")

        if not os.path.exists(name):
            os.mkdir(name)
            file = open(f"{name}/{name}_туры.txt", "w", encoding="utf-8")
            file.write("1")
            file.close()
            for i in range(1, 14):
                file = open(f"{name}/{name}_тур{i}.txt", "w", encoding="utf-8")
                file_res = open(f"{name}/результат_{i}_{name}.txt", "w", encoding="utf-8")
                file.close()
                file_res.close()
            with open(f"{name}/пересечение_команд_{name}.json", "w", encoding="utf-8") as fp:
                commands_dict = {}
                s = json.dumps(commands_dict, ensure_ascii=False)
                fp.write(s)

            fp.close()
        data = {"message": "ok"}
        return JsonResponse(data)


def del_dir_of_game(request):
    if request.method == 'GET':
        name = request.GET.get("name")
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), str(os.getcwd()) + "/" + name.replace('"', ''))
        shutil.rmtree(path)
        data = {"message": "ok"}
        return JsonResponse(data)


def download_shedule_1(request, game):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'tour_shedule_1.zip'

    file = open(f"{game}/{game}_тур1.txt", "r", encoding="utf-8")
    file.seek(0)
    c = ((len(file.readlines()) - 2) // 3)
    count_photo = 0
    while c > 0:
        count_photo += 1
        c -= 5


    with ZipFile(BASE_DIR + "/" + game + "/" + filename, "w") as myzip:
        # myzip.write(f"{game}/tour_shedule_1.png")
        for i in range(1, count_photo + 1):
            myzip.write(f"{game}/tour_shedule_1_{i}.png")

    filepath = BASE_DIR + "/" + game + "/" + filename
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)

    response = HttpResponse(path, content_type=mime_type)

    response['Content-Disposition'] = "attachment; filename=%s" % filename

    return response


def download_shedule_2(request, game):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'tour_shedule_2.zip'

    file = open(f"{game}/{game}_тур2.txt", "r", encoding="utf-8")
    file.seek(0)
    div_name = game.split()[1]

    if div_name == "МСКЛ":
        c = ((len(file.readlines()) - 23) // 3)
        count_photo = 0
        while c > 0:
            count_photo += 1
            c -= 11

        with ZipFile(BASE_DIR + "/" + game + "/" + filename, "w") as myzip:
            myzip.write(f"{game}/tour_shedule_2.png")
            for i in range(1, count_photo + 1):
                myzip.write(f"{game}/tour_shedule_2_{i}.png")
    else:
        c = ((len(file.readlines()) - 2) // 3)
        count_photo = 0
        while c > 0:
            count_photo += 1
            c -= 5


        with ZipFile(BASE_DIR + "/" + game + "/" + filename, "w") as myzip:
            # myzip.write(f"{game}/tour_shedule_2.png")
            for i in range(1, count_photo + 1):
                myzip.write(f"{game}/tour_shedule_2_{i}.png")

    filepath = BASE_DIR + "/" + game + "/" + filename
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)

    response = HttpResponse(path, content_type=mime_type)

    response['Content-Disposition'] = "attachment; filename=%s" % filename

    return response


def download_shedule_3(request, game):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'tour_shedule_3.zip'

    file = open(f"{game}/{game}_тур3.txt", "r", encoding="utf-8")
    file.seek(0)
    div_name = game.split()[1]

    if div_name == "МСКЛ":
        c = ((len(file.readlines()) - 23) // 3)
        count_photo = 0
        while c > 0:
            count_photo += 1
            c -= 11

        with ZipFile(BASE_DIR + "/" + game + "/" + filename, "w") as myzip:
            myzip.write(f"{game}/tour_shedule_3.png")
            for i in range(1, count_photo + 1):
                myzip.write(f"{game}/tour_shedule_3_{i}.png")
    else:
        c = ((len(file.readlines()) - 2) // 3)
        count_photo = 0
        while c > 0:
            count_photo += 1
            c -= 5


        with ZipFile(BASE_DIR + "/" + game + "/" + filename, "w") as myzip:
            # myzip.write(f"{game}/tour_shedule_2.png")
            for i in range(1, count_photo + 1):
                myzip.write(f"{game}/tour_shedule_3_{i}.png")

    filepath = BASE_DIR + "/" + game + "/" + filename
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)

    response = HttpResponse(path, content_type=mime_type)

    response['Content-Disposition'] = "attachment; filename=%s" % filename

    return response


def download_shedule_4(request, game):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'tour_shedule_2.zip'

    file = open(f"{game}/{game}_тур4.txt", "r", encoding="utf-8")
    file.seek(0)
    div_name = game.split()[1]

    if div_name == "МСКЛ":
        c = ((len(file.readlines()) - 23) // 3)
        count_photo = 0
        while c > 0:
            count_photo += 1
            c -= 11

        with ZipFile(BASE_DIR + "/" + game + "/" + filename, "w") as myzip:
            myzip.write(f"{game}/tour_shedule_4.png")
            for i in range(1, count_photo + 1):
                myzip.write(f"{game}/tour_shedule_4_{i}.png")
    else:
        c = ((len(file.readlines()) - 2) // 3)
        count_photo = 0
        while c > 0:
            count_photo += 1
            c -= 5


        with ZipFile(BASE_DIR + "/" + game + "/" + filename, "w") as myzip:
            # myzip.write(f"{game}/tour_shedule_2.png")
            for i in range(1, count_photo + 1):
                myzip.write(f"{game}/tour_shedule_4_{i}.png")

    filepath = BASE_DIR + "/" + game + "/" + filename
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)

    response = HttpResponse(path, content_type=mime_type)

    response['Content-Disposition'] = "attachment; filename=%s" % filename

    return response




def download_1(request, game):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'shedule_1.zip'

    file = open(f"{game}/{game}_тур1.txt", "r", encoding="utf-8")
    file.seek(0)
    c = ((len(file.readlines()) - 2) // 3)
    count_photo = 0
    while c > 0:
        count_photo += 1
        c -= 5


    with ZipFile(BASE_DIR + "/" + game + "/" + filename, "w") as myzip:
        # myzip.write(f"{game}/shedule_1.png")
        for i in range(1, count_photo + 1):
            myzip.write(f"{game}/shedule_1_{i}.png")

    filepath = BASE_DIR + "/" + game + "/" + filename
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)

    response = HttpResponse(path, content_type=mime_type)

    response['Content-Disposition'] = "attachment; filename=%s" % filename

    return response


def download_2(request, game):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'shedule_2.zip'

    file = open(f"{game}/{game}_тур2.txt", "r", encoding="utf-8")
    c = ((len(file.readlines()) - 2) // 3)
    count_photo = 0
    while c > 0:
        count_photo += 1
        c -= 5

    with ZipFile(BASE_DIR + "\\" + game + "\\" + filename, "w") as myzip:
        for i in range(1, count_photo + 1):
            myzip.write(f"{game}/shedule_2_{i}.png")

    filepath = BASE_DIR + "\\" + game + "\\" + filename
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)

    response = HttpResponse(path, content_type=mime_type)

    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


def download_3(request, game):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'shedule_3.zip'

    file = open(f"{game}/{game}_тур3.txt", "r", encoding="utf-8")
    c = ((len(file.readlines()) - 2) // 3)
    count_photo = 0
    while c > 0:
        count_photo += 1
        c -= 5

    with ZipFile(BASE_DIR + "\\" + game + "\\" + filename, "w") as myzip:
        for i in range(1, count_photo + 1):
            myzip.write(f"{game}/shedule_3_{i}.png")

    filepath = BASE_DIR + "\\" + game + "\\" + filename
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)

    response = HttpResponse(path, content_type=mime_type)

    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

def download_4(request, game):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'shedule_4.zip'

    file = open(f"{game}/{game}_тур4.txt", "r", encoding="utf-8")
    c = ((len(file.readlines()) - 2) // 3)
    count_photo = 0
    while c > 0:
        count_photo += 1
        c -= 5

    with ZipFile(BASE_DIR + "\\" + game + "\\" + filename, "w") as myzip:
        for i in range(1, count_photo + 1):
            myzip.write(f"{game}/shedule_4_{i}.png")

    filepath = BASE_DIR + "\\" + game + "\\" + filename
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)

    response = HttpResponse(path, content_type=mime_type)

    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


def download_5(request, game):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'shedule_5.zip'

    file = open(f"{game}/{game}_тур5.txt", "r", encoding="utf-8")
    c = ((len(file.readlines()) - 2) // 3)
    count_photo = 0
    while c > 0:
        count_photo += 1
        c -= 5

    with ZipFile(BASE_DIR + "\\" + game + "\\" + filename, "w") as myzip:
        for i in range(1, count_photo + 1):
            myzip.write(f"{game}/shedule_5_{i}.png")

    filepath = BASE_DIR + "\\" + game + "\\" + filename
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)

    response = HttpResponse(path, content_type=mime_type)

    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


def download_6(request, game):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'shedule_6.zip'

    file = open(f"{game}/{game}_тур6.txt", "r", encoding="utf-8")
    c = ((len(file.readlines()) - 2) // 3)
    count_photo = 0
    while c > 0:
        count_photo += 1
        c -= 5

    with ZipFile(BASE_DIR + "\\" + game + "\\" + filename, "w") as myzip:
        for i in range(1, count_photo + 1):
            myzip.write(f"{game}/shedule_6_{i}.png")

    filepath = BASE_DIR + "\\" + game + "\\" + filename
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)

    response = HttpResponse(path, content_type=mime_type)

    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


def download_7(request, game):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'shedule_7.zip'

    file = open(f"{game}/{game}_тур7.txt", "r", encoding="utf-8")
    c = ((len(file.readlines()) - 2) // 3)
    count_photo = 0
    while c > 0:
        count_photo += 1
        c -= 5

    with ZipFile(BASE_DIR + "\\" + game + "\\" + filename, "w") as myzip:
        for i in range(1, count_photo + 1):
            myzip.write(f"{game}/shedule_7_{i}.png")

    filepath = BASE_DIR + "\\" + game + "\\" + filename
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)

    response = HttpResponse(path, content_type=mime_type)

    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


def download_8(request, game):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'shedule_8.zip'

    file = open(f"{game}/{game}_тур6.txt", "r", encoding="utf-8")
    c = ((len(file.readlines()) - 2) // 3)
    count_photo = 0
    while c > 0:
        count_photo += 1
        c -= 5

    with ZipFile(BASE_DIR + "\\" + game + "\\" + filename, "w") as myzip:
        for i in range(1, count_photo + 1):
            myzip.write(f"{game}/shedule_8_{i}.png")

    filepath = BASE_DIR + "\\" + game + "\\" + filename
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)

    response = HttpResponse(path, content_type=mime_type)

    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


def download_9(request, game):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'shedule_9.zip'

    file = open(f"{game}/{game}_тур9.txt", "r", encoding="utf-8")
    c = ((len(file.readlines()) - 2) // 3)
    count_photo = 0
    while c > 0:
        count_photo += 1
        c -= 5

    with ZipFile(BASE_DIR + "\\" + game + "\\" + filename, "w") as myzip:
        for i in range(1, count_photo + 1):
            myzip.write(f"{game}/shedule_9_{i}.png")

    filepath = BASE_DIR + "\\" + game + "\\" + filename
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)

    response = HttpResponse(path, content_type=mime_type)

    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


def download_10(request, game):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'shedule_10.zip'

    file = open(f"{game}/{game}_тур10.txt", "r", encoding="utf-8")
    c = ((len(file.readlines()) - 2) // 3)
    count_photo = 0
    while c > 0:
        count_photo += 1
        c -= 5

    with ZipFile(BASE_DIR + "\\" + game + "\\" + filename, "w") as myzip:
        for i in range(1, count_photo + 1):
            myzip.write(f"{game}/shedule_10_{i}.png")

    filepath = BASE_DIR + "\\" + game + "\\" + filename
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)

    response = HttpResponse(path, content_type=mime_type)

    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


def download_11(request, game):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'shedule_11.zip'

    file = open(f"{game}/{game}_тур11.txt", "r", encoding="utf-8")
    c = ((len(file.readlines()) - 2) // 3)
    count_photo = 0
    while c > 0:
        count_photo += 1
        c -= 5

    with ZipFile(BASE_DIR + "\\" + game + "\\" + filename, "w") as myzip:
        for i in range(1, count_photo + 1):
            myzip.write(f"{game}/shedule_11_{i}.png")

    filepath = BASE_DIR + "\\" + game + "\\" + filename
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)

    response = HttpResponse(path, content_type=mime_type)

    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


def download_12(request, game):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'shedule_12.zip'

    file = open(f"{game}/{game}_тур12.txt", "r", encoding="utf-8")
    c = ((len(file.readlines()) - 2) // 3)
    count_photo = 0
    while c > 0:
        count_photo += 1
        c -= 5

    with ZipFile(BASE_DIR + "\\" + game + "\\" + filename, "w") as myzip:
        for i in range(1, count_photo + 1):
            myzip.write(f"{game}/shedule_12_{i}.png")

    filepath = BASE_DIR + "\\" + game + "\\" + filename
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)

    response = HttpResponse(path, content_type=mime_type)

    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


def download_13(request, game):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'shedule_13.zip'

    file = open(f"{game}/{game}_тур13.txt", "r", encoding="utf-8")
    c = ((len(file.readlines()) - 2) // 3)
    count_photo = 0
    while c > 0:
        count_photo += 1
        c -= 5

    with ZipFile(BASE_DIR + "\\" + game + "\\" + filename, "w") as myzip:
        for i in range(1, count_photo + 1):
            myzip.write(f"{game}/shedule_13_{i}.png")

    filepath = BASE_DIR + "\\" + game + "\\" + filename
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)

    response = HttpResponse(path, content_type=mime_type)

    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
