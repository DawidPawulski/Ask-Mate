from flask import Flask, render_template, request, redirect, session
import data_manager
import os
import util

app = Flask(__name__)
app.secret_key = b'lubie!@#$%^placky%#$#'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
target = os.path.join(APP_ROOT, 'static/images/')
data_manager.create_user_table_if_not_exist()


@app.route('/')
def display_all_questions():
    global current_sortkey
    global sort_order
    global limit
    if not request.args.get('order_by'):
        current_sortkey = 'submission_time'
        sortkey = current_sortkey
        sort_order = 'DESC'
    else:
        sortkey = request.args.get('order_by')
        if sortkey == current_sortkey:
            sort_order = util.toggle_order(sort_order)
        else:
            sort_order = 'DESC'
            current_sortkey = sortkey

    limit = 'limit_on'

    questions_data = data_manager.get_questions_by_key(sortkey, sort_order, limit)

    all_user_info = data_manager.get_exist_users_info()

    return render_template('home.html',
                           questions=questions_data,
                           limit=limit,
                           user_info=all_user_info)


@app.route('/list', methods=['POST', 'GET'])
def display_questions():
    global current_sortkey
    global sort_order
    global limit
    if not request.args.get('order_by'):
        current_sortkey = 'submission_time'
        sortkey = current_sortkey
        sort_order = 'DESC'
    else:
        sortkey = request.args.get('order_by')
        if sortkey == current_sortkey:
            sort_order = util.toggle_order(sort_order)
        else:
            sort_order = 'DESC'
            current_sortkey = sortkey

    limit = 'limit_off'

    questions_data = data_manager.get_questions_by_key(sortkey, sort_order, limit)

    return render_template('home.html', questions=questions_data, limit=limit)


@app.route('/question/<int:question_id>')
def display_answers(question_id):
    data_manager.update_views_number(question_id, 1)
    question_data = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    question_comments = data_manager.get_question_comments(question_id)
    answer_comments = data_manager.get_answer_comments(question_id)

    # it check who is log in and send message which decide that button display or not
    log_in_user = data_manager.get_user_by_question(question_id)
    if session.get('username'):
        if log_in_user['login'] == session['username']:
            show_check_button_for_question = True
        else:
            show_check_button_for_question = False
    else:
        show_check_button_for_question = False

    # it return a name of answers owner
    user_info_answer = data_manager.get_login_answer_ID_by_questionID(question_id)
    user_info_question = data_manager.get_exist_users_info()

    return render_template('answers.html',
                           question=question_data,
                           answers=answers,
                           question_comments=question_comments,
                           answer_comments=answer_comments,
                           check_button=show_check_button_for_question,
                           user_info_answer=user_info_answer,
                           user_info_question=user_info_question)


@app.route('/add-question', methods=['GET', 'POST'])
def add_new_question():
    if request.method == 'POST':
        logged_user = session['username']

        question = dict(request.form)
        question['image'] = util.upload_picture(request.files.getlist, target)
        question['user_id'] = data_manager.get_user_id_by_login(logged_user)

        data_manager.add_new_question(question)

        return redirect('/')
    return render_template('new_question.html', question=None)


@app.route('/question/<int:question_id>/delete', methods=['GET', 'POST'])
def delete_question(question_id):
    data_manager.delete_question(question_id)

    return redirect('/')


@app.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    question_data = data_manager.get_question_by_id(question_id)

    if request.method == 'POST':
        question = dict(request.form)
        question['question_id'] = question_id
        question['image'] = util.upload_picture(request.files.getlist, target)
        data_manager.update_question(question)
        return redirect(f'/question/{question_id}')

    return render_template('edit_question.html', question=question_data)


@app.route('/question/<int:question_id>/new-answer', methods=['GET', 'POST'])
def new_answer(question_id):
    if request.method == 'POST':
        logged_user = session['username']

        answer = dict(request.form)
        answer['question_id'] = question_id

        answer['image'] = util.upload_picture(request.files.getlist, target)
        answer['user_id'] = data_manager.get_user_id_by_login(logged_user)

        data_manager.add_answer(answer)
        return redirect(f'/question/{question_id}')

    return render_template('new_answer.html', question_id=question_id, answer_data=None)


@app.route('/answer/<int:answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    answer_data = data_manager.get_answers_by_id(answer_id)
    question_id = answer_data['question_id']
    if request.method == "POST":
        answer = dict(request.form)
        answer['image'] = util.upload_picture(request.files.getlist, target)
        data_manager.update_answer(answer, answer_id)

        return redirect('/question/{}'.format(question_id))

    return render_template('edit_answer.html', answer_data=answer_data)


@app.route('/answer/<int:answer_id>/delete')
def delete_answer(answer_id):
    question_id = data_manager.get_question_id_by_answer_id(answer_id)
    data_manager.delete_answer(answer_id)

    return redirect(f'/question/{question_id}')


@app.route('/question/<int:question_id>/vote/<which_page>')
def update_question_votes(question_id, which_page):
    vote_value = int(request.args.get('vote'))
    vote_number = data_manager.get_vote_number_by_question_id(question_id) + vote_value
    data_manager.update_question_vote_number(question_id, vote_number)

    # it give reputation points and question owner the reputation points
    info = data_manager.get_reputation_points_and_userID_question(question_id)

    # it change reputation points
    if vote_value < 0:
        new_reputation_points = int(info['reputation']) - 2
        data_manager.change_reputation_points(new_reputation_points, info['user_id'])
    elif vote_value > 0:
        new_reputation_points = int(info['reputation']) + 5
        data_manager.change_reputation_points(new_reputation_points, info['user_id'])

    if which_page == "home":
        return redirect('/')
    else:
        # this function causes that the number of visits does not change
        value_for_change_number_of_views = -1
        data_manager.update_views_number(question_id, value_for_change_number_of_views)
        return redirect(f'/question/{question_id}')


@app.route('/question/vote/<int:answer_id>/<int:question_id>')
def update_answer_votes(answer_id, question_id):
    vote_value = int(request.args.get('vote'))

    # it add plus/minus votes into the question
    vote_number = data_manager.get_vote_number_by_answer_id(answer_id) + vote_value
    data_manager.update_answer_vote_number(answer_id, vote_number)

    # it give reputation points and question owner the reputation points
    info = data_manager.get_reputation_points_answer(answer_id)

    # it change reputation points
    if vote_value < 0:
        new_reputation_points = int(info['reputation']) - 2
        data_manager.change_reputation_points(new_reputation_points, info['user_id'])
    elif vote_value > 0:
        new_reputation_points = int(info['reputation']) + 10
        data_manager.change_reputation_points(new_reputation_points, info['user_id'])

    # this causes that the number of visits does not change
    value_for_change_number_of_views = -1
    data_manager.update_views_number(question_id, value_for_change_number_of_views)

    return redirect(f'/question/{question_id}')


@app.route('/search')
def searching_by_phrase():
    search_phrase = request.args.get('q')
    questions = data_manager.get_question_by_phrase(search_phrase)
    answers = data_manager.get_answer_by_phrase(search_phrase)

    return render_template('search-result.html', questions=questions, answers=answers, search_phrase=search_phrase)


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def new_question_comment(question_id):
    if request.method == 'POST':
        logged_user = session['username']

        comment = dict(request.form)
        comment['question_id'] = question_id
        comment['user_id'] = data_manager.get_user_id_by_login(logged_user)

        data_manager.add_question_comment(comment)

        return redirect(f'/question/{question_id}')

    return render_template('new_question_comment.html', question_id=question_id)


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def new_answer_comment(answer_id):
    if request.method == 'POST':
        logged_user = session['username']

        comment = dict(request.form)
        comment['answer_id'] = answer_id
        comment['user_id'] = data_manager.get_user_id_by_login(logged_user)

        question_id = data_manager.get_question_id_by_answer_id(answer_id)
        comment['question_id'] = question_id
        data_manager.add_answer_comment(comment)

        return redirect(f'/question/{question_id}')

    return render_template('answer_comment_form.html', answer_id=answer_id, comment_message=None)


@app.route('/comments/<comment_id>/delete')
def delete_comment(comment_id):
    question_id = data_manager.get_question_id_by_comment_id(comment_id)
    data_manager.delete_comment(comment_id)

    return redirect(f'/question/{question_id}')


@app.route('/register', methods=['GET', 'POST'])
def check_newuser_nickname_login_password():
    if request.method == 'POST':
        register_user_login = request.form['login']
        register_password = util.hash_password(request.form['password'])
        if util.check_new_user_username_login(register_user_login):
            data_manager.register_new_user(register_user_login,
                                           register_password)
        return redirect('/')


@app.route('/users')
def display_all_users():
    all_users = data_manager.get_exist_users_info()
    return render_template('user_list.html', all_users=all_users)


@app.route('/login', methods=['POST'])
def login_user():
    typed_user = request.form['login']
    typed_password = request.form['password']

    database_password = data_manager.find_user_and_password(typed_user)
    if database_password:
        if util.verify_password(typed_password, database_password[0]['password']):
            session['username'] = typed_user
    return redirect(request.form['current_path'])


@app.route('/logout')
def logout_user():
    session.pop('username', None)
    return redirect('/')


@app.route('/check_question/<answer_id>/<question_id>')
def check_question(answer_id, question_id):
    data_manager.update_answer_check(answer_id)

    # it change reputation points
    info = data_manager.get_reputation_points_answer(answer_id)
    new_reputation_points = int(info['reputation']) + 15
    data_manager.change_reputation_points(new_reputation_points, info['user_id'])

    return redirect(f'/question/{question_id}')


@app.route('/users/<int:user_id>')
def display_user_details(user_id):
    user_details = data_manager.get_user_details(user_id)
    user_answers = data_manager.get_user_answers(user_id)
    user_questions = data_manager.get_user_questions(user_id)
    user_comments = data_manager.get_user_comments(user_id)
    return render_template('user_info.html',
                           user_details=user_details,
                           user_answers=user_answers,
                           user_questions=user_questions,
                           user_comments=user_comments,
                           clever_function=data_manager.get_question_id_by_answer_id)


if __name__ == '__main__':
    app.run(debug=True)
