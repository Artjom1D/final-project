from flask import Flask, render_template,request, redirect

from flask_sqlalchemy import SQLAlchemy
from speech import speech_to_text
from translate import Translator
import bcrypt


def hashed_str(plain_text):
    return bcrypt.hashpw(plain_text.encode('utf-8'), bcrypt.gensalt()) 

def check_str(plain_text, hashed_str):
    return bcrypt.checkpw(plain_text.encode('utf-8'), hashed_str)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Card(db.Model):
   
    
    id = db.Column(db.Integer, primary_key=True)
    
    title = db.Column(db.String(100), nullable=False)
   
    subtitle = db.Column(db.String(300), nullable=False)
    
    text = db.Column(db.Text, nullable=False)

    
    def __repr__(self):
        return f'<Card {self.id}>'
    

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)










@app.route('/', methods=['GET','POST'])
def login():
        error = ''
        if request.method == 'POST':
            form_login = request.form['email']
            form_password = request.form['password']
            
           
            users_db = User.query.all()
            for user in users_db:
                if check_str(form_login, user.login) and check_str(form_password, user.password):
                    return redirect('/index')
            else:
                error = 'Неправильно указан пользователь или пароль'
                return render_template('login.html', error=error)

            
        else:
            return render_template('login.html')



@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        login= request.form['email']
        password = request.form['password']
        
        
        login = hashed_str(login)
        password = hashed_str(password)
        user = User(login=login, password=password)
        db.session.add(user)
        db.session.commit()
        
        return redirect('/')
    
    else:    
        return render_template('registration.html')


@app.route('/index')
def index():
    #Отображение объектов из БД
    cards = Card.query.order_by(Card.id).all()
    return render_template('index.html', cards=cards)


@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)

    return render_template('card.html', card=card)


@app.route('/create')
def create():
    return render_template('create_card.html')

@app.route("/create")
def home():
    return render_template('index.html')


def result_calculate(size, lights, device):
    
    return size + lights  + device 


@app.route('/1')
def opros():
    return render_template('opros.html')


@app.route('/<size>')
def lights(size):
    return render_template(
                            'opros2.html', 
                            size=size
                           )


@app.route('/<size>/<lights>')
def electronics(size, lights):
    return render_template(
                            'opros3.html',                           
                            size = size, 
                            lights = lights                           
                           )


@app.route('/<size>/<lights>/<device>')
def end(size, lights, device):
    return render_template('end.html', 
                            result=result_calculate(int(size),
                                                    int(lights), 
                                                    int(device)
                                                    )
                        )


@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']


        card = Card(title=title, subtitle=subtitle, text=text)

        db.session.add(card)
        db.session.commit()
        return redirect('/index')
    else:
        return render_template('create_card.html')


@app.route("/voice")
def voice():
    try:
        text = speech_to_text()
    except:
        text = 'Что-то пошло не так...'
    return render_template("create_card.html", text=text)

@app.route("/translate")
def translate():
    E = "English"
    R = "Russian"
    try:
        text = speech_to_text()
    except:
        text = 'Что-то пошло не так...'
    
    tr = Translator(from_lang=R, to_lang=E)
    result = tr.translate(text)

    return render_template("create_card.html", result=result)


@app.route("/delete", methods=['POST'])
def delete():

    return redirect('index')

if __name__ == "__main__":
    app.run(debug=True)
