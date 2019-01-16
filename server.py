from flask import Flask, render_template, redirect, request
import data_manager

app = Flask(__name__)


@app.route('/WORK-IN-PROGRESS')
def workinprogress():
    return render_template("workinprogress.html")


@app.route('/')
def home_redirect():
    questions_dict=data_manager.read_latest_five_questions()
    return render_template("index.html", questions_dict=questions_dict)


@app.route('/list')
def mainpage():
    questions_dict = data_manager.read_all_questions()
    questions_dict = data_manager.sorted_by_submission_time(questions_dict)
    return render_template("index.html", questions_dict=questions_dict)


@app.route('/question/<num>')
def question(num):
    questions = data_manager.read_a_question(num)
    answers_list = data_manager.answer_by_question_id(num)
    return render_template("question.html", num=num, questions=questions, answers_list=answers_list)


# Need to implement vote up ---> Help implement this function please
'''@app.route('/question/<num>/vote_up', methods=['GET', 'POST'])
def vote_up_answer(num):
    if request.method == 'POST':
        data_manager.vote_up(num)
    return redirect('/question/<num>')'''


@app.route('/trying')
def trying():
    this_question = data_manager.read_a_question(2)
    #answers_list = data_manager.get_this_answer(1, 3)
    return render_template('testing.html', questions=this_question)


@app.route('/question/<num>/new-answer')
def new_answer(num):
    return render_template("new-answer.html", num=num)


@app.route('/new-question')
def new_question():
    return render_template("new-question.html")


@app.route('/submit-question', methods=['GET', 'POST'])
def submit_question():
    if request.method == 'POST':
        id_ = data_manager.get_new_question_id()
        submission_time = data_manager.convert_time(data_manager.get_current_unix_timestamp())
        title = request.form['title']
        message = request.form['message']
        views = 0
        votes = 0
        question_dict = {
            'id': id_,
            'submission_time': submission_time,
            'view_number': views,
            'vote_number': votes,
            'title': title,
            'message': message,
            'image': None
        }
        data_manager.add_question(question_dict)
    return redirect('/question/'+id_)


@app.route('/submit-answer', methods=['GET', 'POST'])
def submit_answer():
    if request.method == 'POST':
        id_ = data_manager.get_new_answer_id()
        # submission_time = data_manager.get_current_unix_timestamp()
        submission_time = data_manager.convert_time(data_manager.get_current_unix_timestamp())
        votes = 0
        question_id = request.form['question_id']
        message = request.form['message']
        answer_dict = {
            'id': id_,
            'submission_time': submission_time,
            'vote_number': votes,
            'question_id': question_id,
            'message': message,
            'image': None
        }
        data_manager.add_answer(answer_dict)
    return redirect('/question/'+question_id)


@app.route('/delete-question/<num>')
def delete_question(num):
    data_manager.delete_question(num)
    return redirect('/list')


@app.route('/answer/<num>/delete-answer/<answer_id>')
def delete_answer(num, answer_id):
    data_manager.delete_answer(answer_id)
    data_manager.delete_comment(num)
    return redirect('/question/'+num)


@app.route('/question/<num>/q-comment/<comment_id_>')
def delete_comment(num, comment_id_):
    data_manager.delete_comment(num, comment_id_)
    return redirect('/question/'+num+'/q-comment')


@app.route('/question/<num>/edit-answer/<answer_id>', methods=['GET', 'POST'])
def route_edit_answer(num, answer_id):
    if request.method == 'POST':
        update = request.form['message']
        data_manager.update_answer(update, answer_id)
        return redirect('/question/'+num)
    elif request.method == 'GET':
        answer = data_manager.get_this_answer(num, answer_id)
        return render_template("edit-answer.html", answer_id=answer_id, answer=answer, num=num)


@app.route('/question/<num>/q-comment')
def submit_q_comment(num):
    comments = data_manager.read_q_comments(num)
    return render_template('q-comment.html', num=num, comments=comments)


@app.route('/comment', methods=['POST'])
def comment_on_question():
    if request.method == 'POST':
        id_ = data_manager.get_new_comment_id()
        submission_time = data_manager.convert_time(data_manager.get_current_unix_timestamp())
        question_id = request.form['question_id']
        message = request.form['comment']
        comment_dict = {
            'id': id_,
            'question_id': question_id,
            'answer_id': None,
            'message': message,
            'submission_time': submission_time,
            'edited_count': None
            }
        data_manager.comment_on_question(comment_dict)
        return redirect('/question/'+question_id+'/q-comment')


if __name__ == "__main__":
    app.run()

