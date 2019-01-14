import csv
import time
import data_paths

question_path = data_paths.question_path
answer_path = data_paths.answer_path
question_header = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
answer_header = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def read_question():
    global question_path
    return read_csv(question_path)


def read_answer():
    global answer_path
    return read_csv(answer_path)


def read_csv(path):
    with open(path, "r") as questions:
        reader = csv.DictReader(questions)
        myList = []
        for row in reader:
            myList.append(row)
    return myList


def convert_csv_to_human_readable(list_of_dicts):
    new_csv = []
    for row in list_of_dicts:
        if 'submission_time' in row:
            row['submission_time'] = convert_time(row['submission_time'])
        new_csv.append(row)
    return new_csv


def convert_time(unix_timestamp):
    readable_time = time.ctime(int(unix_timestamp))
    return readable_time


def delete_answer(id_):
    answers = read_answer()
    for answer in answers:
        if id_ == answer['id']:
            answers.remove(answer)
    rewrite_csv(answers, answer_path, answer_header)


def delete_question(id_):
    questions = read_question()
    answers = read_answer()
    for question in questions:
        if id_ == question['id']:
            questions.remove(question)
            break
    rewrite_csv(questions, question_path, question_header)
    for answer in answers:
        if id_ == answer['question_id']:
            answers.remove(answer)
    rewrite_csv(answers, answer_path, answer_header)


def rewrite_csv(data, path, header):
    with open(path, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, header)
        writer.writeheader()
        for i in data:
            writer.writerow(i)


def add_question(new_question):
    with open(question_path, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, question_header)
        writer.writerow(new_question)


def add_answer(new_answer):
    with open(answer_path, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, answer_header)
        writer.writerow(new_answer)


def sorted_by_submission_time(list_of_dicts):
    n = len(list_of_dicts)
    for i in range(n):
        for j in range(i, n):
            if list_of_dicts[j]['submission_time'] > list_of_dicts[i]['submission_time']:
                temp = list_of_dicts[i]
                list_of_dicts[i] = list_of_dicts[j]
                list_of_dicts[j] = temp
    return list_of_dicts


def get_new_question_id():
    questions = read_question()
    max_id = "0"
    for i in questions:
        if max_id < i['id']:
            max_id = i['id']
    max_id = int(max_id) + 1
    return str(max_id)


def get_new_answer_id():
    answers = read_answer()
    max_id = "0"
    for i in answers:
        if max_id < i['id']:
            max_id = i['id']
    max_id = int(max_id) + 1
    return str(max_id)


def get_current_unix_timestamp():
    current_time = time.time()
    return int(current_time)
