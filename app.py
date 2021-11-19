from flask import Flask, request, url_for, redirect
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, LoginManager, UserMixin, logout_user, login_required
from sqlalchemy.orm import backref


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.secret_key = 'keep it secret, keep it safe'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# users is now the old consumer table


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    name = db.Column(db.String, unique=False, nullable=False)
    phone = db.Column(db.String, unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    city = db.Column(db.Integer, unique=False, nullable=False)

    applicationConnect = db.relationship(
        'Application', backref='users', lazy=True)

    def check_password(self, password):
        return self.password == password


class Favorites(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    applicationConnect = db.relationship(
        'Application', backref='Favorites', lazy=True)


class City(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    stateConnect = db.relationship('State', backref='City', lazy=True)


class FastFood(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    state_id = db.Column(db.Integer, unique=True, nullable=False)

    connectFastFoodCity = db.relationship(
        'FastFood_City', backref='FastFood', lazy=True)


# many to many
class FastFood_City(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FastFood_id = db.Column(db.Integer, db.ForeignKey(
        FastFood.id))
    City_id = db.Column(db.Integer, db.ForeignKey(
        City.id))


class Restaurant(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    state_id = db.Column(db.Integer, unique=True, nullable=False)

    connectRestaurantCity = db.relationship(
        'Restaurant_City', backref='Restaurant', lazy=True)


class Restaurant_City(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Restaurant_id = db.Column(db.Integer, db.ForeignKey(
        Restaurant.id))
    City_id = db.Column(db.Integer, db.ForeignKey(
        City.id))


class StreetFood(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    state_id = db.Column(db.Integer, unique=True, nullable=False)

    connectStreetFoodCity = db.relationship(
        'StreetFood_City', backref='StreetFood', lazy=True)


class StreetFood_City(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    StreetFood_id = db.Column(db.Integer, db.ForeignKey(
        StreetFood.id))
    City_id = db.Column(db.Integer, db.ForeignKey(
        City.id))


class State(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    city_name = db.Column(db.String, db.ForeignKey(
        City.name), nullable=False)


class Application(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, db.ForeignKey(
        Users.username), nullable=False)
    # maybe allow user to have top 3 from favorites always displayed on homepage
    favorites_name = db.Column(db.String, db.ForeignKey(
        Favorites.name), nullable=False)

    # maybe allow users to have favorites for different cities?
db.create_all()
# user = Consumer(name='john', phone='209-111-1234', age=23, citykey=2)
# db.session.add(user)
# db.session.commit()
# fav = Favorites(name='FirstFavorite')

# db.session.add(fav)
# db.session.commit()
# db.drop_all()


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = ''
        password = ''
        username += request.form['username']
        password += request.form['password']

        print(username)
        print(password)

        user = Users.query.filter_by(username=username).filter_by(
            password=password).first()

        if user is None or user.check_password(password) is None:
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('homepage'))

    return render_template('login.html')


@app.route('/register', methods=['POST'])
def register():
    username = request.form['register-username']
    password = request.form['register-password']
    name = request.form['register-name']
    phone = request.form['register-phone']
    age = request.form['register-age']
    city = request.form['register-username']

    newUser = Users(username=username, password=password,
                    name=name, phone=phone, age=age, city=city)

    db.session.add(newUser)
    db.session.commit()

    return 'success: Registration Success!'


@app.route('/home', methods=['GET', 'POST'])
@login_required
def homepage():

    return render_template('home.html')


@app.route('/favorites', methods=['GET', 'POST'])
def favorites():

    favorites = Favorites.query.all()
    print(favorites)
    return render_template('favorites.html')


@app.route('/list', methods=['GET', 'POST'])
def list():
    return render_template('list.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
