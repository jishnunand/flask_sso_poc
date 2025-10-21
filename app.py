from flask import Flask, request, redirect, session, render_template, url_for
from onelogin.saml2.auth import OneLogin_Saml2_Auth
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

def init_saml_auth(req):
    # Flask request to dict expected by python3-saml
    url_data = req.url
    post_data = req.form.copy()
    return OneLogin_Saml2_Auth({
        'https': 'on' if req.scheme == 'https' else 'off',
        'http_host': req.host,
        'script_name': req.path,
        'get_data': req.args.copy(),
        'post_data': post_data
    }, custom_base_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), ''))

@app.route('/')
def index():
    if 'samlUserdata' in session:
        user_data = session['samlUserdata']
        return render_template('index.html', user=user_data)
    else:
        return redirect(url_for('login'))

@app.route('/login/')
def login():
    req = request
    auth = init_saml_auth(req)
    return redirect(auth.login())

@app.route('/acs/', methods=['POST'])
def acs():
    req = request
    auth = init_saml_auth(req)
    auth.process_response()
    errors = auth.get_errors()
    if len(errors) == 0:
        if auth.is_authenticated():
            session['samlUserdata'] = auth.get_attributes()
            session['samlNameId'] = auth.get_nameid()
            return redirect(url_for('index'))
        else:
            return render_template('error.html', error="User not authenticated")
    else:
        return render_template('error.html', error=', '.join(errors))

@app.route('/logout/')
def logout():
    req = request
    auth = init_saml_auth(req)
    name_id = session.get('samlNameId', None)
    session.clear()
    return redirect(auth.logout(name_id=name_id))

@app.route('/metadata/')
def metadata():
    from onelogin.saml2.metadata import OneLogin_Saml2_Metadata
    saml_settings = OneLogin_Saml2_Auth({'custom_base_path':os.path.join(os.path.dirname(os.path.abspath(__file__)), '')}).get_settings()
    metadata = saml_settings.get_sp_metadata()
    errors = saml_settings.validate_metadata(metadata)
    if len(errors) == 0:
        resp = app.response_class(response=metadata, status=200, mimetype='text/xml')
        return resp
    else:
        return ", ".join(errors), 500

if __name__ == "__main__":
    app.run(debug=True)
