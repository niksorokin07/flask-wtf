from flask import Flask, render_template, url_for, redirect, flash, request, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class LoginForm(FlaskForm):
    astronaut_id = StringField('id астронавта', validators=[DataRequired()])
    astronaut_password = PasswordField('Пароль астронавта', validators=[DataRequired()])
    captain_id = StringField('id капитана', validators=[DataRequired()])
    captain_password = PasswordField('Пароль капитана', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Доступ')


class SlideForm(FlaskForm):
    slide = FileField()
    submit = SubmitField('Загрузить изображение')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = "static/uploads"


@app.route('/')
@app.route('/index')
def index():
    param = {}
    param["title"] = "q"
    return render_template('base.html', **param)


@app.route('/training/<prof>')
def training(prof):
    param = {}
    param["title"] = prof
    print(prof)
    if "инженер" in prof or "строитель" in prof:
        q = 1
    else:
        q = 2
    param["img_name"] = q
    return render_template('training.html', **param)


@app.route('/list_prof/<t>')
def list_prof(t):
    param = {}
    param["list"] = ["инженер-исследователь", "пилот", "строитель", "экзоюиолог", "врач",
                     "инженер по терраформированию", "климатолог", "специалист по радиационной защите", "астрогеолог",
                     "гляциолог", "инженер жизнеобеспечения", "метеоролог", "оператор марсохода", "киберинженер",
                     "штурман", "пилот дронов"]
    if "ol" == t:
        q = 1
    elif "ul" == t:
        q = 2
    else:
        q = 3
    param["type"] = q
    print(q)
    return render_template('list_prof.html', **param)


@app.route('/answer')
@app.route('/auto_answer')
def answer():
    param = {"title": "q",
             "surname": "Watny",
             "name": "Mark",
             "education": "выше среднего",
             "profession": "штурман марсохода",
             "sex": "male",
             "motivation": "Всегда мечтал эить на марсе",
             "ready": True}
    return render_template('auto_answer.html', **param)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        astr = form["astronaut_id"]
        cap = form["captain_id"]
        return redirect(f'/success/{astr}/{cap}')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/success/<astr>/<cap>')
def success(astr, cap):
    return f"Форма для астронавта {astr} и капитана {cap} отправлена"


@app.route('/distribution')
def distribution():
    return render_template('distribution.html',
                           list=["Ридли Скот", "Энди Уир", "Марк Уотни", "Ванката Капур", "Тедди Сандерс", "Шон Бин"])


@app.route('/tables/<sex>/<age>')
def tables(sex, age):
    if not age.isdigit():
        return
    else:
        if sex == "male" and int(age) < 21:
            t = 1
        elif sex == "female" and int(age) < 21:
            t = 2
        elif sex == "male" and int(age) >= 21:
            t = 3
        elif sex == "female" and int(age) >= 21:
            t = 4
        else:
            t = 5
        return render_template('tables.html', type=t)


@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    form = SlideForm()
    if form.validate_on_submit():
        file = form.slide.data
        if file and allowed_file(file):
            filename = secure_filename(file)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(file_path)
            file.save(file_path)
            return render_template('gallery.html', form=form)
    return render_template('gallery.html', form=form)


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
