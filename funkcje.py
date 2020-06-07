import os
import random
import re
import sqlite3
from datetime import date

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Pydate.settings')
django.setup()

from Pydate.models import PersonalQuestionUser, PersonalQuestionContent, User, UserData, Match


def choose_best_by_personality(my_personality, users_list):
    if len(users_list) == 0:
        return None
    list_to_sort = []
    for u in users_list:
        if re.match("IN.J", my_personality) and re.match("EN.P", u.profile.personality) or \
                re.match("IN.J", u.profile.personality) and re.match("EN.P", my_personality) or \
                re.match("IS.J", my_personality) and re.match("ES.P", u.profile.personality) or \
                re.match("IS.J", u.profile.personality) and re.match("ES.P", my_personality) or \
                re.match("ES.J", my_personality) and re.match("IS.P", u.profile.personality) or \
                re.match("ES.J", u.profile.personality) and re.match("IS.P", my_personality) or \
                re.match("EN.J", my_personality) and "INFP" == u.profile.personality or \
                re.match("EN.J", u.profile.personality) and "INFP" == my_personality or \
                re.match("E.TJ", my_personality) and "INTP" == u.profile.personality or \
                re.match("E.TJ", u.profile.personality) and "INTP" == my_personality or \
                "ISFP" == my_personality and "ENFJ" == u.profile.personality or \
                "ISFP" == u.profile.personality and "ENFJ" == my_personality:  # blue
            list_to_sort.append({'user': u, 'points': 5})
        elif re.match(".S.P", my_personality) and re.match(".NT.", u.profile.personality) or \
                re.match(".S.P", u.profile.personality) and re.match(".NT.", my_personality) or \
                re.match(".S.J", my_personality) and re.match(".S.P", u.profile.personality) or \
                re.match(".S.J", u.profile.personality) and re.match(".S.P", my_personality) or \
                re.match(".S..", my_personality) and "ENTJ" == u.profile.personality or \
                re.match(".S..", u.profile.personality) and "ENTJ" == my_personality:  # light green
            list_to_sort.append({'user': u, 'points': 3})
        elif re.match(".S.P", my_personality) and re.match(".S.P", u.profile.personality) or \
                re.match(".S.J", my_personality) and re.match(".NT.", u.profile.personality) or \
                re.match(".S.J", u.profile.personality) and re.match(".NT.", my_personality):  # yellow
            list_to_sort.append({'user': u, 'points': 2})
        elif re.match(".N..", my_personality) and re.match(".N..", u.profile.personality) or \
                re.match(".S.J", my_personality) and re.match(".S.J", u.profile.personality):  # dark green
            list_to_sort.append({'user': u, 'points': 4})
        elif re.match(".NF.", my_personality) and re.match(".S..", u.profile.personality) or \
                re.match(".NF.", u.profile.personality) and re.match(".S..", my_personality):
            list_to_sort.append({'user': u, 'points': 1})
    list_to_sort.sort(key=lambda x: x['points'], reverse=True)
    return list_to_sort[0]['user']


def dodaj_pytanie():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("INSERT INTO starter_question ('content') VALUES ('pytam')")
    conn.commit()
    conn.close()


# dodaj_pytanie()


def populate():
    for a in range(8):
        user = User(username=str(a), password="helloworld")
        user.save()
        profile = UserData(user=user)
        profile.birth = date.today()
        profile.sex = "F"
        profile.searching_for = "M"
        profile.description = "esfbhfssbef"
        profile.latitude = "0"
        profile.longitude = "0"
        profile.save()
    for a in range(10):
        p1 = PersonalQuestionContent(content="How are you?")
        p1.save()
        user = User.objects.all()[0]
        p2 = PersonalQuestionUser(user=user, questionID=p1)
        p2.save()
    for a in range(3):
        numbers = [i for i in range(8)]
        user1_rn = numbers[random.randint(0, len(numbers) - 1)]
        numbers.remove(user1_rn)
        user2_rn = numbers[random.randint(0, len(numbers) - 1)]
        numbers.remove(user2_rn)
        user1 = User.objects.get(username=user1_rn)
        user2 = User.objects.get(username=user2_rn)
        if a == 0:
            chat = Match(user1=user1, user2=user2, personal_questions_match="00")
        elif a == 1:
            chat = Match(user1=user1, user2=user2, personal_questions_match="01")
        else:
            chat = Match(user1=user1, user2=user2, personal_questions_match="11")
        chat.save()


if __name__ == "__main__":
    # populate()
    pass
