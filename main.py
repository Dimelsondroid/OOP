student_dict = {}
lector_dict = {}
reviewer_dict = {}


class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __str__(self):
        return f'Name: {self.name}\n' \
               f'Surname: {self.surname}\n' \
               f'Average homework mark: {_avg_grade(self.grades):.1f}\n' \
               f'Courses in progress: {self.courses_in_progress}\n' \
               f'Finished courses: {self.finished_courses}\n'

    def rate_hw(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) \
                and course in self.courses_in_progress \
                and course in lecturer.courses_attached \
                and 0 <= grade <= 10:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            print(f'Some marks were skipped for {lecturer.surname} due to discrepancy in courses')
            return

    def __lt__(self, other):
        if not isinstance(other, Student):
            print('Not a student')
            return
        return _avg_grade(self.grades) < _avg_grade(other.grades)

    def __le__(self, other):
        if not isinstance(other, Student):
            print('Not a student')
            return
        return _avg_grade(self.grades) <= _avg_grade(other.grades)

    def __eq__(self, other):
        if not isinstance(other, Student):
            print('Not a student')
            return
        return _avg_grade(self.grades) == _avg_grade(other.grades)

    def compare(self, operator, other):
        if operator in ['<', '>']:
            if not self.__lt__(other):
                print(f'{self.name} {self.surname} have better average mark')
            else:
                print(f'{other.name} {other.surname} have better average mark')
        elif operator in ['<=', '>=']:
            if not self.__le__(other):
                print(f'{self.name} {self.surname} have better or equal average mark')
            else:
                print(f'{other.name} {other.surname} have better or equal average mark')
        elif operator in ['==', '!=']:
            if not self.__eq__(other):
                print(f'Students have different average mark')
            else:
                print(f'Students have equal average mark')


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        return f'Name: {self.name}\n' \
               f'Surname: {self.surname}\n' \
               f'Average lector`s mark: {_avg_grade(self.grades):.1f}\n'

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            print('Not a lector')
            return
        return _avg_grade(self.grades) < _avg_grade(other.grades)

    def __le__(self, other):
        if not isinstance(other, Lecturer):
            print('Not a student')
            return
        return _avg_grade(self.grades) <= _avg_grade(other.grades)

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            print('Not a student')
            return
        return _avg_grade(self.grades) == _avg_grade(other.grades)

    def compare(self, operator, other):
        if operator in ['<', '>']:
            if not self.__lt__(other):
                print(f'{self.name} {self.surname} have better average mark')
            else:
                print(f'{other.name} {other.surname} have better average mark')
        elif operator in ['<=', '>=']:
            if not self.__le__(other):
                print(f'{self.name} {self.surname} have better or equal average mark')
            else:
                print(f'{other.name} {other.surname} have better or equal average mark')
        elif operator in ['==', '!=']:
            if not self.__eq__(other):
                print(f'Lectors have different average mark')
            else:
                print(f'Lectors have equal average mark')


class Reviewer(Mentor):
    def __str__(self):
        return f'Name: {self.name}\n' \
               f'Surname: {self.surname}\n'

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) \
                and course in self.courses_attached \
                and course in student.courses_in_progress \
                and 0 <= grade <= 10:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            print(f'Some marks were skipped for {student.surname} due to discrepancy in courses')
            return


def _all_courses():
    all_courses_temp = set()
    for person in student_dict.values():
        all_courses_temp = all_courses_temp | set(person.courses_in_progress)
    for person in lector_dict.values():
        all_courses_temp = all_courses_temp | set(person.courses_attached)
    for person in reviewer_dict.values():
        all_courses_temp = all_courses_temp | set(person.courses_attached)
    all_courses = list(all_courses_temp)
    print(all_courses)  # for testing\checking or like a help if the input was incorrect
    return all_courses


def _avg_grade(grades):
    mark_sum = 0
    i = 0
    for courses, marks in grades.items():
        for mark in marks:
            mark_sum += int(mark)
            i += 1
    if mark_sum == 0:
        return mark_sum
    return mark_sum/i


def _search_by_id(ident, group):
    for identity, person in group.items():
        if ident == person.name or ident == person.surname or ident == identity:
            return person
        else:
            continue
    print('No such person')
    return False


def stud_avg_by_course(students, course):
    i = 0
    summary = 0
    for student in students.values():
        if isinstance(student, Student) and course in student.courses_in_progress and course in student.grades.keys():
            for mark in student.grades[course]:
                summary += mark
                i += 1
    if summary != 0:
        print(f'Average mark for all students on {course} course is {summary / i:.1f}')
    else:
        print(f'Average mark for all students on {course} course is 0')


def lect_avg_by_course(lectors, course):
    i = 0
    summary = 0
    for lector in lectors.values():
        if isinstance(lector, Lecturer) and course in lector.courses_attached and course in lector.grades.keys():
            for mark in lector.grades[course]:
                summary += mark
                i += 1
    if summary != 0:
        print(f'Average mark for all lectors on {course} course is {summary / i:.1f}')
    else:
        print(f'Average mark for all lectors on {course} course is 0')


def compare():
    group = input('Enter group to compare it`s members: ')
    if group in ['stud', 'student', 'students']:
        first = _search_by_id(input('Input name, surname or id of first student: '), student_dict)
        second = _search_by_id(input('Input name, surname or id of second student: '), student_dict)
        while True:
            operand = input('Input compare operator: ')
            if operand not in ['<', '>', '<=', '>=', '==', '!=']:
                print('Use correct operand')
            else:
                break
    elif group in ['lect', 'lector', 'lecturer', 'lecturers']:
        first = _search_by_id(input('Input name, surname or id of first lector: '), lector_dict)
        second = _search_by_id(input('Input name, surname or id of second lector: '), lector_dict)
        while True:
            operand = input('Input compare operator: ')
            if operand not in ['<', '>', '<=', '>=', '==', '!=']:
                print('Use correct operand')
            else:
                break
    else:
        print(f'Not a group with any grades')
        return
    first.compare(operand, second)


def rate_student():
    reviewer = _search_by_id(input('Input reviewer name, surname or id: '), reviewer_dict)
    student = _search_by_id(input('Input student name, surname or id: '), student_dict)
    if not reviewer or not student:
        print('Wrong data, aborting')
        return
    course = input('Input course student attended: ')
    if course not in _all_courses():
        print('There`s no such course')
        return
    reviewer.rate_hw(student, course, int(input('Enter mark for homework: ')))


def rate_lector():
    student = _search_by_id(input('Input student name, surname or id: '), student_dict)
    lector = _search_by_id(input('Input lector name, surname or id: '), lector_dict)
    if not lector or not student:
        print('Wrong data, aborting')
        return
    course = input('Input course student attended: ')
    if course not in _all_courses():
        print('There`s no such course')
        return
    student.rate_hw(lector, course, int(input('Enter mark for homework: ')))


def add_student():
    while True:
        student_id = input('Input new student identificator: ')
        if student_id in student_dict.keys():
            print('Identificator already exists, try again')
        else:
            break
    name = input('Input name: ')
    surname = input('Input surname: ')
    gender = input('Input gender: ')
    new_student = Student(name, surname, gender)
    student_dict[student_id] = new_student
    courses_in_progress = input('Input courses to attend: ').split(' ')
    new_student.courses_in_progress += courses_in_progress


def add_lector():
    while True:
        lector_id = input('Input new lector identificator: ')
        if lector_id in lector_dict.keys():
            print('Identificator already exists, try again')
        else:
            break
    name = input('Input name: ')
    surname = input('Input surname: ')
    new_lector = Lecturer(name, surname)
    lector_dict[lector_id] = new_lector
    courses_attached = input('Input course attached: ').split(' ')
    new_lector.courses_attached += courses_attached


def add_reviewer():
    while True:
        reviewer_id = input('Input new reviewer identificator: ')
        if reviewer_id in reviewer_dict.keys():
            print('Identificator already exists, try again')
        else:
            break
    name = input('Input name: ')
    surname = input('Input surname: ')
    new_reviewer = Reviewer(name, surname)
    reviewer_dict[reviewer_id] = new_reviewer
    courses_attached = input('Input course attached: ').split(' ')
    new_reviewer.courses_attached += courses_attached


def show_group():
    group = input('Enter group to show: ')
    if group in ['stud', 'student', 'students']:
        for student in student_dict.values():
            print(student)
    elif group in ['lect', 'lector', 'lecturer', 'lecturers']:
        for lector in lector_dict.values():
            print(lector)
    elif group in ['rev', 'review', 'reviewer']:
        for reviewer in reviewer_dict.values():
            print(reviewer)
    else:
        print('Wrong input')


def avg_marks():
    who = input('Look for avg marks students or lectors? ')
    course = input('Enter course name: ')
    if course not in _all_courses():
        print('There`s no such course')
        return
    if who in ['stud', 'student', 'students']:
        stud_avg_by_course(student_dict, course)
    elif who in ['lect', 'lector', 'lecturer', 'lecturers']:
        lect_avg_by_course(lector_dict, course)
    else:
        print('Wrong input')


def short_show_all():
    print('Students:')
    for key, person in student_dict.items():
        print(f'{key} - {person.name} {person.surname} {person.courses_in_progress}. Marks: {person.grades}')
    print('Lectors:')
    for key, person in lector_dict.items():
        print(f'{key} - {person.name} {person.surname} {person.courses_attached}. Marks: {person.grades}')
    print('Reviewers:')
    for key, person in reviewer_dict.items():
        print(f'{key} - {person.name} {person.surname} {person.courses_attached}')


# Mostly for starting and testing purposes
def _pre_creation():
    student1 = Student('Ruoy', 'Eman', 'male')
    student1.courses_in_progress += ['Python', 'JS']
    student2 = Student('Dan', 'Mark', 'male')
    student2.courses_in_progress += ['JS']
    student_dict['student1'] = student1
    student_dict['student2'] = student2

    reviewer1 = Reviewer('Some', 'Buddy')
    reviewer1.courses_attached += ['Python']
    reviewer2 = Reviewer('Roy', 'Lino')
    reviewer2.courses_attached += ['JS']
    reviewer_dict['reviewer1'] = reviewer1
    reviewer_dict['reviewer2'] = reviewer2

    lector1 = Lecturer('Any', 'Boddy')
    lector1.courses_attached += ['JS']
    lector2 = Lecturer('Troy', 'Leggy')
    lector2.courses_attached += ['Python', 'JS']
    lector_dict['lector1'] = lector1
    lector_dict['lector2'] = lector2

    reviewer2.rate_hw(student1, 'JS', 7)
    reviewer1.rate_hw(student1, 'Python', 8)
    reviewer1.rate_hw(student1, 'Python', 5)
    reviewer2.rate_hw(student2, 'JS', 9)
    reviewer2.rate_hw(student2, 'JS', 4)
    reviewer2.rate_hw(student2, 'JS', 6)
    student2.rate_hw(lector1, 'JS', 6)
    student1.rate_hw(lector1, 'JS', 5)
    student2.rate_hw(lector1, 'JS', 6)
    student1.rate_hw(lector2, 'Python', 7)
    student1.rate_hw(lector2, 'Python', 4)
    student2.rate_hw(lector2, 'JS', 9)

    # print('Student\n', student1)
    # print('Student\n', student2)
    # print('Lector\n', lector1)
    # print('Lector\n', lector2)
    # print('Mentor\n', reviewer1)
    # print('Mentor\n', reviewer2)
    #
    # student2.compare('>=', student1)
    # lector2.compare('>', lector1)
    # print(student1 != student2)
    # print(lector1 != lector2)
    #
    # stud_avg_by_course(student_dict, 'Python')
    # lect_avg_by_course(lector_dict, 'JS')


def main():
    """
    "c": compare students or lectors,
    "rs": rate specific student homework by a lector,
    "rl": rate specific lector by a student
    "as": add new student
    "ar": add new reviewer
    "al": add new lector
    "s": prints out all info for chosen group
    "a": average mark for courses
    "ssa": short list of all groups
    """

    commands = {
        "c": compare,
        "rs": rate_student,
        "rl": rate_lector,
        "as": add_student,
        "ar": add_reviewer,
        "al": add_lector,
        "s": show_group,
        "a": avg_marks,
        "ssa": short_show_all,
        "h": help
    }

    _pre_creation()

    while True:
        command = ""
        while not bool(command):
            command = input("Awaiting command: ")
        for key in commands:
            if command == "h":
                commands[command](main)
                break
            if command == key:
                commands[command]()
                break

        if command == "q":
            print("\nQuiting...")
            break


main()
