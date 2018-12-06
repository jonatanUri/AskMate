from flask import Flask, render_template, redirect, request
import data_manager

app = Flask(__name__)


@app.route('/WORK-IN-PROGRESS')
def workinprogress():
    return render_template("workinprogress.html")


@app.route('/')
def mainpage():
    questions_dict = data_manager.read_question()
    return render_template("index.html", questions_dict=questions_dict)


@app.route('/question/<num>')
def question(num):
    questions_dict = data_manager.read_question()
    answer_dict = data_manager.read_answer()
    return render_template("question.html", num=num, questions_dict=questions_dict, answer_dict=answer_dict)


@app.route('/question/<num>/answer')
def add_answer(num):
    questions_dict = data_manager.read_question()
    answers_dict = data_manager.read_csv()
    return render_template("new-answer.html", num=num, questions_dict=questions_dict, answer_dicts=answers_dict)


@app.route('/new-question')
def new_question():
    return None


if __name__ == "__main__":
    app.run()


# request.form['name'] in py, and name in html
# <form method = "post">