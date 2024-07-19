from flask import Flask, jsonify, make_response, request
import json

app = Flask(__name__)


students = {'size': 0, 'students': []}

try:
    with open('students.json', 'r') as f:
        students = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    students = {'size': 0, 'students': []}


@app.route('/')
def home():
    return "Welcome to the KenGen Geothermal Training Institute"


@app.route('/api/v1/students', methods=['POST'])
def add_student():
    global students # Use the global students variable
    data = request.get_json()

    if data is None or 'student_name' not in data:
        error_response = {
                'error': 'Your request should have the student name'
                }
        return make_response(jsonify(error_response), 400)

    new_student = {
            'name': data['student_name']
            }
    if students is None:
        new_student['id'] = 1
        students = {
                'size': 1,
                'students': [new_student]
                }
    else:
        total = students['size']
        new_student['id'] = total + 1
        students['students'].append(new_student)
        students['size'] = total + 1

    with open('students.json', 'w') as f:
        json.dump(students, f, indent=2, sort_keys=True)

    successful_response = {
            'message': 'Added new student successfully',
            'data': students
            }
    return make_response(jsonify(successful_response), 200)


@app.route('/api/v1/students', methods=['GET'])
def get_all_students():
    if students is None:
        response = {
                'message': 'No students in the records',
                'data': None
                }
        return make_response(jsonify(response), 200)

    response = {
            'message': 'Current student records',
            'data': students['students']
            }
    return make_response(jsonify(response), 200)


@app.route('/api/v1/students/<int:student_id>', methods=['GET'])
def get_student_by_id(student_id):
    error_response = {
            'message': f'No record found with the student ID: {student_id}',
            'data': None
            }

    if student_id <= 0 or students is None:
        return make_response(jsonify(error_response), 404)

    if student_id > students['size'] or students['size'] == 0:
        return make_response(jsonify(error_response), 404)

    students_list = students['students']

    student = next((student for student in students_list if student['id'] == student_id), None)
    if student is None:
        response = {
                'message': 'No such student record exists',
                'data': None
                }
        return make_response(jsonify(response), 404)

    response = {
            'message': 'Student record successfully found',
            'data': student
            }
    return make_response(jsonify(response), 200)


@app.route('/api/v1/students/<int:student_id>', methods=['DELETE'])
def delete_student_by_id(student_id):
    global students

    error_response = {
            'message': f'No record found with the student ID: {student_id}',
            'data': None
            }

    if student_id <= 0 or students is None:
        return make_response(jsonify(error_response), 404)

    if student_id > students['size'] or students['size'] == 0:
        return make_response(jsonify(error_response), 404)

    student_list = students['students']
    student_to_delete = next((student for student in student_list if student_id == student['id']), None)
    
    if student_to_delete is None:
        return make_response(jsonify(error_response), 404)

    successful_response = {
            'message': 'Successfuly deleted student record',
            'deleted_record': student_to_delete
            }
    students['students'].remove(student_to_delete)
    students['size'] -= 1  # Decrease the size by one
    with open('students.json', 'w') as f:
        json.dump(students, f, indent=2, sort_keys=True)

    return make_response(jsonify(successful_response), 200)


if __name__ == '__main__':
    app.run(debug=True)
