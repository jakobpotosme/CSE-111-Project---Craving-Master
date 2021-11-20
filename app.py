from flask import Flask, request, url_for, redirect
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, LoginManager, UserMixin, logout_user, login_required
from sqlalchemy.orm import backref
from sqlalchemy.util.langhelpers import method_is_overridden


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
    city_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    state_id = db.Column(db.Integer, nullable=False)

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
    city_id = db.Column(db.Integer, unique=False, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    state_id = db.Column(db.Integer, unique=False, nullable=False)

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
    city_id = db.Column(db.Integer, unique=False, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    state_id = db.Column(db.Integer, unique=False, nullable=False)

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

# adding to fastfood
# ff = FastFood(name="Wendy's", city_id=1, state_id=1)
# ff = FastFood(name='Taco Bell', city_id=2, state_id=1)
# ff = FastFood(name='Chick-fil-A', city_id=3, state_id=1)
# ff = FastFood(name='Starbucks', city_id=4, state_id=1)
# ff = FastFood(name="McDonald's", city_id=5, state_id=1)
# db.session.add(ff)
# FastFood.query.filter_by(name="Wendy'd").delete()


# adding to restaurant
# r = Restaurant(name="Applebee's", city_id=1, state_id=1)
# r = Restaurant(name="Olive Garden", city_id=2, state_id=1)
# r = Restaurant(name="Buffalo Wild Wings", city_id=3, state_id=1)
# r = Restaurant(name="IHOP", city_id=4, state_id=1)
# r = Restaurant(name="Red Lobster", city_id=5, state_id=1)
# db.session.add(r)

# adding streetfood
# s = StreetFood(name="Soma Street Food Park", city_id=1, state_id=1)
# s = StreetFood(name="El Fuego", city_id=2, state_id=1)
# s = StreetFood(name="Korean Street Food", city_id=3, state_id=1)
# s = StreetFood(name="Tacos Las Ranitas", city_id=4, state_id=1)
# s = StreetFood(name="The Papaya Lady", city_id=5, state_id=1)

# db.session.add(s)
# FastFood.__table__.drop(db.engine)
# Restaurant.__table__.drop(db.engine)
# StreetFood.__table__.drop(db.engine)
# db.session.commit()


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


@app.route('/selection', methods=['GET', 'POST'])
@login_required
def selection():
    input = request.form['city-input']
    print(input)

    joinedFastFoodResult = []
    for c, ff in db.session.query(City, FastFood).filter(
            City.name == input).filter(City.id == FastFood.city_id).all():
        joinedFastFoodResult.append(ff.name)

    joinedStreetFoodResult = []
    for c, s in db.session.query(City, StreetFood).filter(
            City.name == input).filter(City.id == StreetFood.city_id).all():
        joinedStreetFoodResult.append(s.name)

    joinedRestaurantResult = []
    for c, r in db.session.query(City, Restaurant).filter(
            City.name == input).filter(City.id == Restaurant.city_id).all():
        joinedRestaurantResult.append(r.name)
    print(joinedRestaurantResult)
    return render_template('selection.html', FastFood=joinedFastFoodResult, StreetFood=joinedStreetFoodResult, Restaurant=joinedRestaurantResult)


@app.route('/fastfood', methods=['GET', 'POST'])
@login_required
def fastfood():
    fastfoodInfo = request.form['ff-btn']
    print(fastfoodInfo)
    return render_template('fastfood.html', fastfood=fastfoodInfo)


@app.route('/streetfood', methods=['GET', 'POST'])
@login_required
def streetfood():
    streetfoodInfo = request.form['s-btn']
    print(streetfoodInfo)
    return render_template('streetfood.html', streetfood=streetfoodInfo)


@app.route('/restaurant', methods=['GET', 'POST'])
@login_required
def restaurant():
    restaurantInfo = request.form['r-btn']
    print(restaurantInfo)
    return render_template('restaurant.html', restaurant=restaurantInfo)


@app.route('/favorites', methods=['GET', 'POST'])
def favorites():

    # maybe add a column to favorites where indicates top 3 or just list them all
    # with details
    favorites = Favorites.query.all()
    fastfood = FastFood.query.all()
    restaurant = Restaurant.query.all()
    streetfood = StreetFood.query.all()

    print(favorites)
    return render_template('favorites.html', favorites=favorites, fastfood=fastfood, restaurant=restaurant, streetfood=streetfood)


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
