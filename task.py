# data structure
# schools = {
#     _school_name_: {
#         courses: {
#             _course_name_: {
#                 teacher: str,
#                 classes_count: int
#             }
#         },
#         students: {
#             _student_id_: {
#                 first_name: str,
#                 last_name: str,
#                 enrolled_courses: [{
#                     course_name: str,
#                     attendance: int,
#                     scores: [int]
#                 }, ...]
#             }
#         }
#     }
# }

import json
import random as rnd
from statistics import mean
from pprint import pp

def _id_generator(start = 1):
    id = start
    while True:
        yield id
        id += 1

schools = dict()
_gen = _id_generator()

def add_school(school_name, courses = None, students = None):
    if school_name in schools:
        return False

    courses = dict() if courses is None else courses
    students = dict() if students is None else students

    schools[school_name] = {'courses': courses, 'students': students}
    return True

def add_course(school_name, course_name, teacher, classes_count):
    courses = schools[school_name]['courses']
    if course_name in courses:
        return False
    
    courses[course_name] = {'teacher': teacher, 'classes_count': classes_count}
    return True

def add_student(school_name, first_name, last_name, enrolled_courses = None):
    enrolled_courses = list() if enrolled_courses is None else enrolled_courses

    students = schools[school_name]['students']
    student_id = next(_gen)
    students[student_id] = {'first_name': first_name, 
                            'last_name': last_name, 
                            'enrolled_courses': enrolled_courses}
    
    return student_id

def enroll_student(school_name, student_id, course_name, attendance = 0, scores = None):
    scores = list() if scores is None else scores

    student = schools[school_name]['students'][student_id]
    student_courses = student['enrolled_courses']
    if course_name in list(map(lambda course: course['course_name'], student_courses)):
        return False
    
    student_courses.append({'course_name': course_name, 'attendance': attendance, 'scores': scores})
    return True

def student_attendace(school_name, student_id):
    student = schools[school_name]['students'][student_id]
    enrolled_courses = list(map(lambda course: course['course_name'], student['enrolled_courses']))
    total = sum((course_data['classes_count'] for course_name, course_data 
             in schools[school_name]['courses'].items() if course_name in enrolled_courses))
    attendace = sum(map(lambda course: course['attendance'], student['enrolled_courses']))
    return round(attendace / total * float(100), 2)


def average_score_for_student_in_course(school_name, student_id, course_name):
    student = schools[school_name]['students'][student_id]
    student_courses = student['enrolled_courses']
    scores = next((course['scores'] for course 
                   in student_courses if course['course_name'] == course_name))
                   
    return round(mean(scores), 2)

def average_score_for_course(school_name, course_name):
    students = schools[school_name]['students'].values()
    scores = []
    for student in students:
        scores += (mean(course['scores']) for course 
                   in student['enrolled_courses'] 
                   if course['course_name'] == course_name)
    
    return round(mean(scores), 2)

def average_score_for_student(school_name, student_id):
    student = schools[school_name]['students'][student_id]
    course_means = (mean(course['scores']) for course in student['enrolled_courses'])
    return round(mean(course_means), 2)

def average_score_for_school_per_course(school_name):
    course_names = schools[school_name]['courses'].keys()
    averages = {course_name: average_score_for_course(school_name, course_name) 
                for course_name in course_names}
    
    return averages

def average_score_for_school_per_student(school_name):
    student_ids = schools[school_name]['students'].keys()
    averages = {student_id: average_score_for_student(school_name, student_id) 
                for student_id in student_ids}
    
    return averages

def read_file(filename):
    try:
        with open(filename, 'r') as f:
            global schools, _gen
            schools = json.load(f)

            if not schools:
                return False

            ids = []
            for school in schools.values():
                ids += (int(id) for id in school['students'].keys())

            _gen = _id_generator(max(ids) + 1)
            return True
        
    except Exception:
        return False

def write_file(filename):
    with open(filename, 'w') as f:
        json.dump(schools, f)

def main():
    filename = 'schools.json'
    if(read_file(filename)):
        print(f'Data loaded from file {filename}')
    else:
        print('Generating random data')
        first_names = ('Kazimierz', 'Wacław', 'Jan', 'Dariusz', 'Mariusz', 'Zygmunt')
        last_names = ('Sloma', 'Janusz', 'Stary', 'Mlody', 'Kowal', 'Nowak')
        course_names = ['gotowanie', 'spawanie', 'wedkarstwo', 'nurkowanie', 'informatyka', 'stolarka']
        school_names = ('Pierwsza', 'Trzecia')
        courses_count = len(course_names)
        students_count = 20
        for i in range(len(school_names)):
            school_name = school_names[i]
            add_school(school_name)

            tmp = students_count
            if i != len(school_names) - 1:
                tmp = rnd.randint(4, students_count - (len(school_names[i+1:] * 4)))
                students_count -= tmp

            student_ids = []
            for _ in range(tmp):
                student_ids.append(add_student(school_name, rnd.choice(first_names), rnd.choice(last_names)))

            rnd.shuffle(course_names)
            courses_count = len(course_names)
            if i != len(school_names) - 1:
                courses_count = rnd.randint(2, len(course_names) - (len(school_names[i+1:]) * 2))

            courses = [course_names.pop() for _ in range(courses_count)]
            for course in courses:
                teacher = rnd.choice(first_names) + ' ' + rnd.choice(last_names)
                classes_count = rnd.randint(10, 20)
                add_course(school_name, course, teacher, classes_count)
                for id in student_ids:
                    empty_check = course == courses[-1] and not schools[school_name]['students'][id]['enrolled_courses']
                    if empty_check or rnd.choice([0,1]) == 0:
                        scores = [rnd.randint(0, 100) for _ in range(rnd.randint(2, 10))]
                        enroll_student(school_name, id, course, rnd.randint(0, classes_count), scores)

        print('Saving generated data')
        write_file(filename)

    school_name, school = rnd.choice(list(schools.items()))
    student_id, student = rnd.choice(list(school['students'].items()))
    course_name, course = rnd.choice(list(school['courses'].items()))

    print('***Student attendance***')
    attendace = student_attendace(school_name, student_id)
    print(f'School: {school_name}, student: {student['first_name']} {student['last_name']}, attendance: {attendace}%')

    print('\n***Average score for student***')
    score = average_score_for_student(school_name, student_id)
    print(f'School: {school_name}, student: {student['first_name']} {student['last_name']}, avg score: {score}%')

    print('\n***Average score for course***')
    score = average_score_for_course(school_name, course_name)
    print(f'School: {school_name}, course: {course_name}, avg score: {score}%')

    print('\n***Average score for school per student***')
    scores = average_score_for_school_per_student(school_name)
    print(f'School: {school_name}')
    for student_id, score in scores.items():
        student = schools[school_name]['students'][student_id]
        print(f'student: {student['first_name']} {student['last_name']}, avg score: {score}%')

    print('\n***Average score for school per course***')
    scores = average_score_for_school_per_course(school_name)
    print(f'School: {school_name}')
    for course_name, score in scores.items():
        print(f'course: {course_name}, avg score: {score}%')


if __name__ == '__main__':
    main()
