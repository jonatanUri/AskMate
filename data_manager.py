import csv
import time

question_path="/home/jonatan/codecool/WEB/SI1/ksfhdjgfh/sample_data/question.csv"
answer_path="/home/jonatan/codecool/WEB/SI1/ksfhdjgfh/sample_data/answer.csv"


def read_question():
    global question_path
    return read_csv(question_path)

def read_answer():
    global answer_path
    return  read_csv(answer_path)


def read_csv(path):
    with open(path, "r") as questions:
        reader = csv.DictReader(questions)
        myList = []
        for row in reader:
            if 'submission_time' in row:
                row['submission_time'] = convert_time(row['submission_time'])
            myList.append(row)
    return myList


def convert_time(unix_timestamp):
    readable_time = time.ctime(int(unix_timestamp))
    return readable_time


def delete_answer(id_):
    answers = read_answer()
    for answer in answers:
        if id_ == answer['id']:
            answers.remove(answer)
    rewrite_csv(answers,answer_path)


def delete_question(id_):
    questions = read_question()
    answers = read_answer()
    for question in questions:
        if id_ == question['id']:
            questions.remove(question)
    rewrite_csv(questions,question_path)
    for answer in answers:
        if id_ == answer['question_id']:
            answers.remove(answer)
    rewrite_csv(answers, answer_path)


def rewrite_csv(data, path):
    with open(path, "w") as csvfile:
        writer = csv.DictWriter(csvfile)
        writer.writeheader()
        for i in data:
            writer.writerow(i)
