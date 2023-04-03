from datacenter.models import Schoolkid, Subject, Lesson
from datacenter.models import Mark, Chastisement, Commendation
from random import choice


def get_schoolkid(name):
    if not name:
        raise ValueError('Имя не может быть пустым!')
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=name)
    except Schoolkid.MultipleObjectsReturned:
        raise Schoolkid.MultipleObjectsReturned(
            '\nОшибка! В школе несколько учеников с таким именем! Уточните запрос!'
            )
    except Schoolkid.DoesNotExist:
        raise Schoolkid.DoesNotExist(
            '\nОшибка! В школе нет ученика с таким именем! Уточните запрос!'
        )
    return schoolkid


def is_the_subject_correct(schoolkid, subject):
    if not subject:
        raise ValueError('Предмет не может быть пустым!')   
    try:
        subject = Subject.objects.get(
            title=subject.capitalize(), year_of_study=schoolkid.year_of_study
        )
    except Subject.DoesNotExist:
        raise Subject.DoesNotExist(
            '\nОшибка! Такого предмета нет! Уточните запрос!'
        )
    return subject


def get_last_lesson(schoolkid, subject):
    try:
        last_lesson = Lesson.objects.filter(
            subject__title=subject.title,
            year_of_study=schoolkid.year_of_study,
            group_letter=schoolkid.group_letter).order_by('date').last()
    except Lesson.DoesNotExist:
        raise Lesson.DoesNotExist('\nОшибка! Урок не найден! Уточните запрос!')
    return last_lesson


def fix_marks(name):
    schoolkid = get_schoolkid(name)
    Mark.objects.filter(schoolkid=schoolkid, points__lt=4).update(points=5)


def remove_chastisements(name):
    schoolkid = get_schoolkid(name)
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def create_commendation(name, subject):
    schoolkid = get_schoolkid(name)
    subject = is_the_subject_correct(schoolkid, subject)
    with open('commendations.txt', encoding='utf-8') as commendations:
        commendations = commendations.readlines()
    text = choice(commendations).strip()
    last_lesson = get_last_lesson(schoolkid, subject)
    teacher = last_lesson.teacher
    Commendation.objects.create(text=text, created=last_lesson.date,
                                schoolkid=schoolkid, subject=subject,
                                teacher=teacher)


def main():
    fix_marks('Имя ученика')
    remove_chastisements('Имя ученика')
    create_commendation('Имя ученика', 'Предмет')


if __name__ == '__main__':
    main()
