from flask import Flask, render_template, request
from authorization import authorize
from config import oauth_url
from leaderboard import leaderboard_sort
from play import *
from token_exchange import get_token
from userform_upload import user_data_upload
from user import *
from questions import *
from play import checkifrunning
from hunt import pausehunt, runhunt, endhunt
from sidequests import *
import cryptocode
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ok'
log = logging.getLogger('werkzeug')
log.disabled = True
SESSION_COOKIE_SECURE = True
PORT = 5000


@app.route('/')
def home():
    try:
        login = session['login']
        return render_template('index.html', url=oauth_url, login=login)
    except KeyError:
        session['login'] = False
        login = session['login']
        return render_template('index.html', url=oauth_url, login=login)


@app.route('/profile')
def myprofile():
    try:
        if session['login'] and session['user']:
            return redirect(f"/u/{session['user']}")
        else:
            return redirect('/auth')
    except KeyError:
        return redirect('/auth')


@app.route('/auth')
def auth_redirect():
    try:
        if session['user']:
            return redirect('/')
        else:
            return redirect(oauth_url)
    except KeyError:
        return redirect(oauth_url)


@app.route('/callback')
def callback():
    return get_token()


@app.route('/fetch-userdata')
def dashboard():
    token = session['token']
    session['login'] = False
    return authorize(token)


@app.route('/userform', methods=['POST', 'GET'])
def form():
    data = request.form
    name = data['name']
    organization = data['organization']
    return user_data_upload(name, organization)


@app.route('/u/edit', methods=['POST', 'GET'])
def edit_profile():
    try:
        if session['user']:
            return render_template('userform.html')
        else:
            return redirect(oauth_url)
    except KeyError:
        return redirect(oauth_url)


@app.route('/play', methods=['POST', 'GET'])
def play_dashboard():
    if checkifrunning() == 'paused':
        flash('The platform is under maintenance, try again later', 'incorrect-ans')
        return redirect('/')

    elif checkifrunning() == 'ended':
        question = get_level_content()
        if question == None:
            return render_template('userform.html')
        else:
            flash('the hunt has ended', 'correct-ans')
            return redirect('/')

    elif checkifrunning() == 'running':
        try:
            check = session['login']
            check2 = session['user']
        except:
            return redirect('/auth')
        login_check(check)
        if dq_check(session['user']):
            flash('you have been disqualified smh', 'incorrect-ans')
            return redirect('/')
        else:
            if session['question_display']:
                question = get_level_content()
                if question == "True":
                    flash('Congratulations, you have completed the hunt!', 'correct-ans')
                    return redirect('/')
                else:
                    if str(get_level()[-1]) == '-':
                        return render_template('userform.html')
                    else:
                        flash(question, 'level-content')
                        flash(get_level(), 'level-num')
                        flash(get_level_image(), 'level-image')
                        login = session['login']
                        return render_template('play.html', login=login, url=oauth_url, source_hint=get_source_hint())
        return redirect('/auth')


@app.route('/play/validate', methods=['GET', 'POST'])
def validate_ans():
    ip = request.remote_addr
    response = request.form['response']
    return validate_answer(response, ip)

@app.route('/submit_click', methods=['GET', 'POST'])
def submit_click():
    question = get_level_content()
    flash(question, 'level-content')
    flash(get_level(), 'level-num')
    flash(get_level_image(), 'level-image')
    login = session['login']
    return render_template('submit_click.html', login=login, url=oauth_url, user_answer="heck")

@app.route('/leaderboard')
def leaderboard():
    try:
        login = session['login']
        return render_template('leaderboard.html', leaderboard=leaderboard_sort(), login=login, url=oauth_url)
    except KeyError:
        session['login'] = False
        session['user'] = None
        return render_template('leaderboard.html', leaderboard=leaderboard_sort(), url=oauth_url,
                               login=session['login'])


@app.route('/guidelines')
def guidelines():
    flash('coming soon', 'correct-ans')
    return redirect('/')


@app.route('/u/<user_id>')
def user(user_id):
    try:
        login = session['login']
        data = user_page(user_id)
        details = f"""<u>Name</u><br>{data['name']}<br><u>Level</u><br>{data['level']}<br><u>Organisation</u><br>{data['organization']}<br><u>Registration Time</u><br>{data['time']}<br><u>Last Solved</u><br>{data['last_solved']}<br>"""
        return render_template('user.html', login=login, url=oauth_url, user=user_id, data=data, details=details,
                               admin=admin_check(session['user']), dq_check=dq_check(user_id))
    except KeyError:
        session['login'] = False
        session['user'] = None
        data = user_page(user_id)
        details = f"""<u>Name</u><br>{data['name']}<br><u>Level</u><br>{data['level']}<br><u>Organisation</u><br>{data['organization']}<br><u>Registration Time</u><br>{data['time']}<br><u>Last Solved</u><br>{data['last_solved']}<br>"""
        return render_template('user.html', login=session['login'], url=oauth_url, user=user_id, data=data,
                               details=details, admin=admin_check(session['user']), dq_check=dq_check(user_id))


@app.route('/u/<user_id>/dq', methods=['GET', 'POST'])
def disqualify(user_id):
    if admin_check(session['user']):
        flash(disqualify_user(user_id), 'success')
        return redirect(f'/u/{user_id}')
    else:
        flash('you have been disqualified from the hunt', 'incorrect-ans')
        return redirect('/')


@app.route('/u/<user_id>/rq', methods=['GET', 'POST'])
def requalify(user_id):
    if admin_check(session['user']):
        flash(requalify_user(user_id), 'success')
        return redirect(f'/u/{user_id}')
    else:
        flash('you have been requalified to the hunt', 'correct-ans')
        return redirect('/')


@app.route('/u/<user_id>/modifyrole', methods=['GET', 'POST'])
def role(user_id):
    if admin_check(session['user']):
        flash(change_role(user_id), 'success')
        return redirect(f'/u/{user_id}')
    else:
        flash('you do not have access to this location', 'incorrect-ans')
        return redirect('/')


@app.route('/sidequest')
def quest():
    content = fetch_quest()
    if content.lower() == 'no sidequests available at the moment':
        flash(content, 'incorrect-ans')
        return redirect('/play')
    else:
        flash(content, 'correct-ans')
        return redirect('/play')


@app.route('/sidequest/replace', methods=['GET', 'POST'])
def quest_replace():
    try:
        if admin_check(session['user']):
            return render_template('new_quest.html')
        else:
            flash('you do not have access to this location', 'incorrect-ans')
            return redirect('/')
    except KeyError:
        return redirect('/auth')


@app.route('/sidequest/replace/submit', methods=['GET', 'POST'])
def submit_replaceed_sq():
    if request.method == 'POST':
        data = request.form['content']
        new_quest(data)
        return redirect('/')


@app.route('/logout')
def logout():
    session['login'] = False
    session['token'] = None
    session['user'] = None
    session['question_display'] = False
    flash('logged out succesfully', 'correct-ans')
    return redirect('/')


@app.route('/admin')
def admin_dashboard():
    if admin_check(session['user']):
        return render_template('admin.html', admin=admin_check(session['user']))
    else:
        flash('you are not an admin 🙄', 'incorrect-ans')
        return redirect('/')


@app.route('/admin/hunt/pause')
def huntpauser():
    if admin_check(session['user']):
        pausehunt()
        return redirect('/')
    else:
        flash('you are not an admin 🙄', 'incorrect-ans')
        return redirect('/')


@app.route('/admin/hunt/run')
def huntrunner():
    if admin_check(session['user']):
        runhunt()
        flash('hunt started', 'correct-ans')
        return redirect('/')
    else:
        flash('you are not an admin 🙄', 'incorrect-ans')
        return redirect('/')


@app.route('/admin/hunt/end')
def huntender():
    if admin_check(session['user']):
        endhunt()
        flash('Hunt ended', 'incorrect-ans')
        return redirect('/')
    else:
        flash('you are not an admin 🙄', 'incorrect-ans')
        return redirect('/')


@app.route('/admin/questions')
def question_list():
    login = session['login']
    return render_template('questions.html', questions=fetch_questions(), login=login, url=oauth_url,
                           admin=admin_check(session['user']))


@app.route('/admin/questions/add')
def new_question_data():
    return render_template('add_question.html', admin=admin_check(session['user']))


@app.route('/admin/questions/add/submit', methods=['GET', 'POST'])
def new_question():
    question_data = request.form
    add_question(question_data['id'], question_data['content'], question_data['image'], question_data['source_hint'], question_data['answer'],
                 question_data['points'], question_data['next_level'])
    return redirect('/admin/questions')


@app.route('/admin/questions/edit/<question_id>')
def modify_question_data(question_id):
    print(fetch_questions(int(question_id)))
    return render_template('edit_question.html', question=fetch_questions(int(question_id)),
                           admin=admin_check(session['user']))


@app.route('/admin/questions/edit/<question_id>/submit', methods=['GET', 'POST'])
def modify_question(question_id):
    question_data = request.form
    flash(edit_question(int(question_id), question_data['content'], question_data['image'], question_data['source_hint'], question_data['answer'],
                        int(question_data['points']), int(question_data['next_level'])))
    return redirect('/admin/questions')


if __name__ == "__main__":
    app.run(debug=True)