import bcrypt
from flask import Flask, render_template, redirect, request, session, escape
import data_manager
import login_manager

app = Flask(__name__)

app.secret_key = b'verk49v,3,,32__'


@app.route('/WORK-IN-PROGRESS')
def workinprogress():
    return render_template("workinprogress.html")


@app.route('/')
def home_redirect():
    if 'username' in session:
        name = 'Logged in as %s' % escape(session['username'])
    else:
        name = 'You are not logged in'

    questions_dict=data_manager.read_latest_five_questions()

    return render_template("index.html", questions_dict=questions_dict, name=name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pw = request.form['password']
        username = request.form['username']
        hash_pw = login_manager.read_hash(username)['user_password']
        if login_manager.verify_password(pw, hash_pw):
            session['username'] = username
        return redirect('/')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect('/')


@app.route('/list')
def mainpage():
    questions_dict = data_manager.read_all_questions()
    questions_dict = data_manager.sorted_by_submission_time(questions_dict) # We could refactor this into one
    return render_template("index.html", questions_dict=questions_dict)


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


@app.route('/registration', methods=['GET', 'POST'] )
def registration():
    if request.method == 'POST':
        hashed_password = hash_password(request.form['candy'])
        user_name = request.form['user_name']
        reg_dict = {
            'user_name': user_name,
            'user_password': hashed_password
        }
        data_manager.registration(reg_dict)
        return redirect('/')
    elif request.method == 'GET':
        return render_template('registration.html')


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
    answers_list = data_manager.get_this_comment(0, 1)
    return render_template('testing.html', questions=this_question, answer=answers_list)


@app.route('/question/<num>/new-answer')
def new_answer(num):
    return render_template("new-answer.html", num=num)


@app.route('/new-question')
def new_question():
    return render_template("new-question.html")


@app.route('/submit-question', methods=['GET', 'POST'])
def submit_question():
    if request.method == 'POST':
        questions = data_manager.read_all_questions()
        id_ = data_manager.get_new_id(questions)
        user_name = session['username']
        user_id = data_manager.get_user_id_from_username(user_name)['id']
        submission_time = data_manager.convert_time(data_manager.get_current_unix_timestamp())
        title = request.form['title']
        message = request.form['message']
        views = 0
        votes = 0
        print(user_id)
        question_dict = {
            'id': id_,
            'user_id': user_id,
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
        answers = data_manager.read_answer()
        id_ = data_manager.get_new_id(answers)
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
    data_manager.delete_all_comments_from_answer(answer_id)
    data_manager.delete_answer(answer_id) # WE could refactor this by Join
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
        comments = data_manager.read_comments()
        id_ = data_manager.get_new_id(comments)
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


@app.route('/question/<num>/a-comment/<answer_id>')
def answer_comments(num, answer_id):
    comments = data_manager.read_a_comments(answer_id)
    return render_template('a-comment.html', num=num, answer_id=answer_id, comments=comments)


@app.route('/question/<num>/a-comment/<answer_id>/delete-comment/<comment_id>')
def delete_answer_comment(num, answer_id, comment_id):
    data_manager.delete_comment_for_answer(answer_id, comment_id)
    return redirect('/question/'+num+'/a-comment/'+answer_id)


@app.route('/answercomment', methods=['POST'])
def comment_on_answer():
    if request.method == 'POST':
        comments = data_manager.read_comments()
        id_ = data_manager.get_new_id(comments)
        submission_time = data_manager.convert_time(data_manager.get_current_unix_timestamp())
        question_id = request.form['question_id']
        answer_id = request.form['answer_id']
        message = request.form['comment']
        answer_comment_dict = {
            'id': id_,
            'question_id': None,
            'answer_id': answer_id,
            'message': message,
            'submission_time': submission_time,
            'edited_count': None
        }
        data_manager.comment_on_answer_question(answer_comment_dict)
        return redirect('/question/'+question_id+'/a-comment/'+answer_id)


@app.route('/question/<num>/q-comment/edit-comment/<comment_id>', methods=['GET', 'POST'])
def edit_comment(num, comment_id):
    if request.method == 'POST':
        update = request.form['message']
        data_manager.update_comment(update, num, comment_id)
        return redirect('/question/' + num+'/q-comment')
    elif request.method == 'GET':
        comment = data_manager.get_this_comment(num, comment_id)
        return render_template("edit-question-comment.html", comment_id=comment_id, comment=comment, num=num)


@app.route('/question/<num>/a-comment/<answer_id_>/edit-comment/<comment_id_>', methods=['GET', 'POST'])
def edit_a_comment(num, answer_id_, comment_id_):
    if request.method == 'POST':
        update = request.form['message']
        data_manager.update_answer_comment(update, answer_id_, comment_id_)
        return redirect('/question/' + num + '/a-comment/' + answer_id_)

    comment = data_manager.get_this_answer_comment(comment_id_)
    return render_template('edit-answer-comment.html', comment_id_=comment_id_, answer_id_=answer_id_, num=num, comment=comment)


if __name__ == "__main__":
    app.run()
