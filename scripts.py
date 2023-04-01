from datacenter.models import Schoolkid, Subject, Lesson
from datacenter.models import Mark, Chastisement, Commendation
from random import choice
from django.core import exceptions


def is_the_name_unique(name):
    try:
        Schoolkid.objects.get(full_name__contains=name)
    except exceptions.MultipleObjectsReturned:
        raise exceptions.MultipleObjectsReturned(
            '\nОшибка! В школе несколько учеников с таким именем! Уточните запрос!'
            )
    except exceptions.ObjectDoesNotExist:
        raise exceptions.ObjectDoesNotExist(
            '\nОшибка! В школе нет ученика с таким именем! Уточните запрос!'
        )
    return Schoolkid.objects.filter(full_name__contains=name).last()


def is_the_subject_correct(subject):
    try:
        Subject.objects.get(title=subject)
    except exceptions.ObjectDoesNotExist:
        raise exceptions.ObjectDoesNotExist(
            '\nОшибка! Такого предмета нет! Уточните запрос!'
        )
    except exceptions.MultipleObjectsReturned:
        pass


def fix_marks(name):
    schoolkid = is_the_name_unique(name)
    marks = Mark.objects.filter(schoolkid=schoolkid, points__lt=4)
    for mark in marks:
        mark.points = 5
        mark.save()


def remove_chastisements(name):
    schoolkid = is_the_name_unique(name)
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def create_commendation(name, subject):
    is_the_subject_correct(subject.capitalize())
    with open('commendations.txt', encoding='utf-8') as commendations:
        commendations = commendations.readlines()
    text = choice(commendations).strip()
    schoolkid = is_the_name_unique(name)
    last_lesson = Lesson.objects.filter(
        subject__title=subject.capitalize(),
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter).order_by('date').last()
    subject = Subject.objects.filter(
        title=subject.capitalize(), year_of_study=schoolkid.year_of_study
        ).last()
    teacher = last_lesson.teacher
    Commendation.objects.create(text=text, created=last_lesson.date,
                                schoolkid=schoolkid, subject=subject,
                                teacher=teacher)


fix_marks('Имя ученика')
remove_chastisements('Имя ученика')
create_commendation('Имя ученика', 'Предмет')
