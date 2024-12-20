import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_babel import Babel, gettext as _

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config['BABEL_DEFAULT_LOCALE'] = 'ru'
app.config['BABEL_SUPPORTED_LOCALES'] = ['ru', 'en']
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

babel = Babel(app)


def get_locale():
    if 'lang' in session:
        return session['lang']
    return request.accept_languages.best_match((app.config['BABEL_SUPPORTED_LOCALES']))


babel.init_app(app, locale_selector=get_locale)


@app.context_processor
def inject_get_locale():
    return {'get_locale': get_locale}


@app.route('/set_language/<language>')
def set_language(language):
    if language not in app.config['BABEL_SUPPORTED_LOCALES']:
        language = 'ru'
    session['lang'] = language
    return redirect(request.referrer or url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def render_not_found(error):
    return "Ничего не нашлось! Вот неудача, отправляйтесь на главную!"


@app.errorhandler(500)
def render_server_error(error):
    return "Что-то не так, но мы все починим"


if __name__ == '__main__':
    app.run(port=5010, debug=True)
