import csv
import os

def get_data_from_file(file):
    records = []

    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
    return records


def get_grades_loop(students, marks, tests, courses):
    for student in students:
        total_weight = 0
        course_cutoff = False
        student_cutoff = False
        course_grade = 0

        old_course = None
        course_tracker = None
        student_tracker = None
        total_grade = 0
        course_grades = []
        old_courses = []

        for mark in marks:
            if mark['student_id'] == student['id']:
                for test in tests:
                    if test['id'] == mark['test_id']:
                        for course in courses:
                            if course['id'] == test['course_id']:
                                if course_tracker is None:
                                    course_tracker = course
                                # If course changes and the total weight was not reset, then there is an error with the previous course's total weight not totaling 100%
                                elif course_tracker['id'] != course['id'] and total_weight > 0:
                                    return -1
                                total_weight += int(test['weight'])
                                course_cutoff = (total_weight == 100)
                                course_grade += float(mark['mark']) * float(test['weight']) / 100
                                old_course = course_tracker
                                course_tracker = course
                                break
                        break
            if student_tracker is None:
                student_tracker = student
            elif (student_tracker['id'] != mark['student_id'] and len(old_courses) > 0) or (mark == marks[-1] and len(old_courses) > 0):
                student_cutoff = True

            if course_cutoff:
                course_grade = round(course_grade, 2)
                course_grades.append(course_grade)
                old_courses.append(old_course)
                total_grade += course_grade
                total_weight = 0
                course_cutoff = False
                course_grade = 0
            if student_cutoff:
                average_grade = round(total_grade/len(old_courses), 2)
                print(f"Student Id: {student_tracker['id']}, Name: {student_tracker['name']}")
                print(f"Total Average:\t{'{:.2f}'.format(average_grade)}%\n")
                for old_course, course_grade in zip(old_courses, course_grades):
                    print(f"\tCourse: {old_course['name']}, Teacher: {old_course['teacher']}")
                    print(f"\tFinal Grade:\t{'{:.2f}'.format(course_grade)}%\n")
                print('\n')
                total_grade = 0
                student_cutoff = False
                old_courses.clear()

            student_tracker = student


def get_grades(students, marks, tests, courses,
               students_index=0, marks_index=0, tests_index=0, courses_index=0,
               student_index_tracker=None, course_index_tracker=None,
               total_weight=0, course_grade=0.0, total_grade=0.0, course_grades=[], old_courses=[]):

    # if students_index != student_index_tracker:
    #     print(f"Id: {students[students_index]['id']}, Name: {students[students_index]['name']}")

    course_cutoff = False
    student_cutoff = False

    if marks[marks_index]['student_id'] == students[students_index]['id']:

        #if marks_index != mark_index_tracker:
            #print(f"{3*' '}Test_Id: {marks[marks_index]['test_id']}, Student_Id: {marks[marks_index]['student_id']}, Mark: {marks[marks_index]['mark']}")

        if tests[tests_index]['id'] == marks[marks_index]['test_id']:

            #if tests_index != test_index_tracker:
                #print(f"{6*' '}Id: {tests[tests_index]['id']}, Course_Id: {tests[tests_index]['course_id']}, Weight: {tests[tests_index]['weight']}")

            if courses[courses_index]['id'] == tests[tests_index]['course_id']:
                # if courses_index != course_index_tracker:
                #     print(f"{9*' '}Id: {courses[courses_index]['id']}, Name: {courses[courses_index]['name']}, Teacher: {courses[courses_index]['teacher']}")

                if course_index_tracker is None:
                    course_index_tracker = courses_index
                # If course changes and the total weight was not reset, then there is an error with the previous course's total weight not totaling 100%
                if courses_index != course_index_tracker and total_weight > 0:
                    return -1
                total_weight += int(tests[tests_index]['weight'])
                course_cutoff = (total_weight == 100)
                course_grade += float(marks[marks_index]['mark']) * float(tests[tests_index]['weight']) / 100

            elif courses_index < len(courses):
                return get_grades(students, marks, tests, courses,
                                  students_index, marks_index, tests_index, courses_index+1,
                                  student_index_tracker, courses_index+1,
                                  total_weight, course_grade, total_grade, course_grades, old_courses)

        elif tests_index < len(tests):
            return get_grades(students, marks, tests, courses,
                              students_index, marks_index, tests_index+1, courses_index,
                              student_index_tracker, course_index_tracker,
                              total_weight, course_grade, total_grade, course_grades, old_courses)

    if student_index_tracker is None:
        student_index_tracker = students_index
    if (students[student_index_tracker]['id'] != marks[marks_index]['student_id'] and len(old_courses) > 0) or (
            marks_index == len(marks)-1 and len(old_courses) > 0):
        student_cutoff = True
    if student_index_tracker != students_index:
        student_index_tracker = students_index

    if marks_index < len(marks):
        if course_cutoff:
            course_grade = round(course_grade, 2)
            course_grades.append(course_grade)
            old_courses.append(courses[course_index_tracker])
            total_grade += course_grade
            total_weight = 0
            course_grade = 0
            course_index_tracker += 1
        if student_cutoff:
            average_grade = round(total_grade/len(old_courses), 2)
            print(f"Student Id: {students[student_index_tracker]['id']}, Name: {students[student_index_tracker]['name']}")
            print(f"Total Average:\t{'{:.2f}'.format(average_grade)}%\n")
            for old_course, course_grade in zip(old_courses, course_grades):
                print(f"\tCourse: {old_course['name']}, Teacher: {old_course['teacher']}")
                print(f"\tFinal Grade:\t{'{:.2f}'.format(course_grade)}%\n")
            print('\n')
            old_courses.clear()
            #total_grade = 0
            #course_index_tracker = None
        else:
            return get_grades(students, marks, tests, courses,
                              students_index, marks_index+1, tests_index, 0,
                              student_index_tracker, course_index_tracker,
                              total_weight, course_grade, total_grade, course_grades, old_courses)

    if students_index < len(students)-1:
        return get_grades(students, marks, tests, courses,
                          students_index+1, marks_index, 0, 0,
                          student_index_tracker, None,
                          0, 0, 0, [], [])


def main():
    resources_dir = os.path.join(os.getcwd(), 'Resources')

    students_path = os.path.join(resources_dir, 'students.csv')
    marks_path = os.path.join(resources_dir, 'marks.csv')
    tests_path = os.path.join(resources_dir, 'tests.csv')
    courses_path = os.path.join(resources_dir, 'courses.csv')

    students = get_data_from_file(students_path)
    marks = get_data_from_file(marks_path)
    tests = get_data_from_file(tests_path)
    courses = get_data_from_file(courses_path)

    #get_grades_loop(students, marks, tests, courses)

    get_grades(students, marks, tests, courses)


if __name__ == "__main__":
    main()
