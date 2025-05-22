from flask import Flask, redirect, request, session, url_for, render_template
from uuid import uuid4

from config import load_config
from auth import MSAuth
from orchestrator_api import OrchestratorClient
from service_breaks import load_breaks, add_break

config = load_config()
app = Flask(__name__)
app.secret_key = config.get('flask_secret', 'secret')
ms_auth = MSAuth(config)
orch_client = OrchestratorClient(config)


@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    folders = orch_client.get_folders()
    user_email = session['user']['preferred_username']
    # Filter folders by user email (placeholder logic)
    accessible = [f for f in folders if user_email in f.get('DisplayName', '')]
    schedules = []
    for f in accessible:
        triggers = orch_client.get_triggers(f['Id'])
        for t in triggers:
            t['FolderName'] = f['DisplayName']
            schedules.append(t)
    breaks = load_breaks()
    return render_template('index.html', schedules=schedules, breaks=breaks, user=session['user'])


@app.route('/login')
def login():
    state = str(uuid4())
    session['state'] = state
    redirect_uri = url_for('authorized', _external=True)
    auth_url = ms_auth.build_auth_url(redirect_uri, state)
    return redirect(auth_url)


@app.route('/authorized')
def authorized():
    if request.args.get('state') != session.get('state'):
        return 'State mismatch', 400
    code = request.args.get('code')
    result = ms_auth.acquire_token_by_authorization_code(code, url_for('authorized', _external=True))
    if 'id_token_claims' in result:
        session['user'] = result['id_token_claims']
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect('https://login.microsoftonline.com/common/oauth2/v2.0/logout')


@app.route('/add_break', methods=['POST'])
def add_service_break():
    if 'user' not in session:
        return redirect(url_for('login'))
    entry = {
        'title': request.form['title'],
        'start': request.form['start'],
        'end': request.form['end'],
        'reason': request.form['reason']
    }
    add_break(entry)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
