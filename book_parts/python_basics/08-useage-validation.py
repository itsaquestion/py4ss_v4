student_1 = {'student_id': 2021001, 'name': 'Alex', 'major': 'finance', 'class_id': 1}
student_2 = {'student_id': 2021002, 'name': 'Bob', 'major': 'finance', 'class_id': 1}
student_3 = {'student_id': 2021003, 'name': 'Clare', 'major': 'accounting', 'class_id': 2}
student_4 = {'student_id': 2021004, 'name': 'David', 'major': 'marketing', 'class_id': 2}
student_5 = {'student_id': 2021005, 'name': 'Eva', 'major': 'finance', 'class_id': 1}
student_6 = {'student_id': 2021006, 'name': 'Frank', 'major': 'accounting', 'class_id': 1}

students_info = [
    student_1,
    student_2,
    student_3,
    student_4,
    student_5,
    student_6
]


def find_students_by_name(data, name):
    result = [student for student in data if student['name'] == name]
    return result


def find_students_by_major(data, major):
    result = [
        student for student in data
        if student['major'] == major
    ]
    return result


def count_by_major(data, major):
    class_size = len(find_students_by_major(data, major))
    return class_size


def find_student_by_id(data, student_id):
    for student in data:
        if student['student_id'] == student_id:
            return student
    return None


def set_python_score(data, student_id, score):
    student = find_student_by_id(data, student_id)
    if student is not None:
        student['python_score'] = score
    return data


def apply_score_updates(data, updates):
    for update in updates:
        set_python_score(data, update['student_id'], update['python_score'])
    return data


def get_avg_python_score(data):
    total_score = 0
    for student in data:
        total_score = total_score + student['python_score']
    return total_score / len(data)


def find_students_by_class(data, class_id):
    result = [
        student for student in data
        if student['class_id'] == class_id
    ]
    return result


def get_avg_python_score_by_class(data, class_id):
    students = find_students_by_class(data, class_id)
    return get_avg_python_score(students)


def get_rank(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'E'


def set_rank(data):
    for student in data:
        student['rank'] = get_rank(student['python_score'])
    return data


def set_pass_status(data):
    for student in data:
        student['passed'] = student['python_score'] >= 60
    return data


def get_pass_rate(data):
    passed_students = [
        student for student in data
        if student['passed']
    ]
    return len(passed_students) / len(data)


def format_student_by_id(data, student_id):
    student = find_student_by_id(data, student_id)
    class_name = student['major'] + ' ' + str(student['class_id']) + '班'
    text = (
        '学号: ' + str(student['student_id']) +
        '；姓名: ' + student['name'] +
        '；班级: ' + class_name +
        '；Python成绩: ' + str(student['python_score']) +
        '；评级: ' + student['rank']
    )
    return text


def list_failed_students(data):
    failed_students = [
        student for student in data
        if student['passed'] == False
    ]
    lines = [
        format_student_by_id(data, student['student_id'])
        for student in failed_students
    ]
    return '\n'.join(lines)


def list_top_students(data):
    highest_score = data[0]['python_score']
    for student in data:
        if student['python_score'] > highest_score:
            highest_score = student['python_score']

    top_students = []
    for student in data:
        if student['python_score'] == highest_score:
            top_students.append(student)

    lines = [
        format_student_by_id(data, student['student_id'])
        for student in top_students
    ]
    return '\n'.join(lines)


python_scores = [
    {'student_id': 2021001, 'python_score': 86},
    {'student_id': 2021002, 'python_score': 59},
    {'student_id': 2021003, 'python_score': 92},
    {'student_id': 2021004, 'python_score': 54},
    {'student_id': 2021005, 'python_score': 88},
    {'student_id': 2021006, 'python_score': 67}
]

set_python_score(students_info, 2021002, 59)
apply_score_updates(students_info, python_scores)
set_rank(students_info)
set_pass_status(students_info)

print('Python平均分:', round(get_avg_python_score(students_info), 2))
print('1班平均分:', round(get_avg_python_score_by_class(students_info, 1), 2))
print('2班平均分:', round(get_avg_python_score_by_class(students_info, 2), 2))
print('及格率:', round(get_pass_rate(students_info), 2))
print(format_student_by_id(students_info, 2021001))
print(list_failed_students(students_info))
print(list_top_students(students_info))
