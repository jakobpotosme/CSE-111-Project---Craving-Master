from logging import fatal
from re import LOCALE
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
    type = db.Column(db.String, nullable=False)

    applicationConnect = db.relationship(
        'Application', backref='Favorites', lazy=True)
    # connectFavoriteFastFood = db.relationship(
    #     'Favorites', backref='Favorites', lazy=True
    # )


class City(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    stateConnect = db.relationship('State', backref='City', lazy=True)
    CityCuisineConnect = db.relationship(
        'City_Cuisines', backref='City', lazy=True)


class FastFood(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    state_id = db.Column(db.Integer, nullable=False)
    cuisine = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)

    connectFastFoodCity = db.relationship(
        'FastFood_City', backref='FastFood', lazy=True)

    connectFastFoodCuisine = db.relationship(
        'FastFood_Cuisine', backref='FastFood', lazy=True)

    # one to many, fastfood can have many cuisines
    # connectCuisines = db.relationship('Cuisines')


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
    name = db.Column(db.String, nullable=False)
    state_id = db.Column(db.Integer, unique=False, nullable=False)
    cuisine = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)

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
    name = db.Column(db.String, nullable=False)
    state_id = db.Column(db.Integer, unique=False, nullable=False)
    cuisine = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)

    connectStreetFoodCity = db.relationship(
        'StreetFood_City', backref='StreetFood', lazy=True)


class StreetFood_City(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    StreetFood_id = db.Column(db.Integer, db.ForeignKey(
        StreetFood.id))
    City_id = db.Column(db.Integer, db.ForeignKey(
        City.id))


class Cuisines(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cuisine = db.Column(db.String, nullable=False)

    connectCityCuisine = db.relationship(
        'City_Cuisines', backref='Cuisines', lazy=True)

# many to many


class City_Cuisines(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String, db.ForeignKey(City.name))
    cuisine_name = db.Column(db.String, db.ForeignKey(Cuisines.cuisine))


class FastFood_Cuisine(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ff_cuisine = db.Column(db.Integer, db.ForeignKey(
        FastFood.cuisine))
    c_cuisine = db.Column(db.Integer, db.ForeignKey(
        Cuisines.cuisine))


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
# db.create_all()

# user = Consumer(name='john', phone='209-111-1234', age=23, citykey=2)
# db.session.add(user)
# db.session.commit()
# fav = Favorites(name='FirstFavorite')

# db.session.add(fav)
# db.session.commit()
# db.drop_all()


# adding to fastfood
# ff = FastFood(name="Wendy's", city_id=1, state_id=1,
#               cuisine='American', type='ff')
# ff = FastFood(name='Taco Bell', city_id=2, state_id=1,
#               cuisine='Mexican', type='ff')
# ff = FastFood(name='Chick-fil-A', city_id=3,
#               state_id=1, cuisine='American', type='ff')
# ff = FastFood(name='Starbucks', city_id=4, state_id=1,
#               cuisine='American', type='ff')
# ff = FastFood(name="McDonald's", city_id=5, state_id=1,
#               cuisine='American', type='ff')
# ff = FastFood(name="McDonald's", city_id=3, state_id=1,
#               cuisine='American', type='ff')
# ff = FastFood(name="El Pollo Loco", city_id=1,
#               state_id=1, cuisine='Mexican', type='ff')
# ff = FastFood(name="El Pollo Loco", city_id=4,
#               state_id=1, cuisine='Mexican', type='ff')
# ff = FastFood(name="Luu's Chicken", city_id=1,
#               state_id=1, cuisine='Japanese', type='ff')
# ff = FastFood(name="Luu's Chicken", city_id=2,
#               state_id=1, cuisine='Japanese', type='ff')

# ff = db.session()
# objects = [
#     FastFood_Cuisine(ff_cuisine='American', c_cuisine='American'),
#     FastFood_Cuisine(ff_cuisine='Mexican', c_cuisine='Mexican'),
#     FastFood_Cuisine(ff_cuisine='Japanese', c_cuisine='Japanese')
# ]
# ff.bulk_save_objects(objects)
# db.session.commit()

# add to City_Cuisines
# cc = db.session()
# objects = [
#     City_Cuisines(city_name='San Francisco', cuisine_name='American'),
#     City_Cuisines(city_name='San Francisco', cuisine_name='Mexican'),
#     City_Cuisines(city_name='Merced', cuisine_name='Mexican'),
#     City_Cuisines(city_name='Merced', cuisine_name='Japanese'),
#     City_Cuisines(city_name='Stockton', cuisine_name='American'),
#     City_Cuisines(city_name='Sacramento', cuisine_name='American'),
#     City_Cuisines(city_name='Sacramento', cuisine_name='Mexican'),
#     City_Cuisines(city_name='Los Angelas', cuisine_name='American')

# ]
# cc.bulk_save_objects(objects)
# db.session.commit()

# db.session.add(ff)
# db.session.commit()
# FastFood.query.filter_by(name="Wendy'd").delete()

# Favorites.query.filter_by(name="Buffalo Wild Wings").delete()

# adding to restaurant
# r = Restaurant(name="Applebee's", city_id=1,
#                state_id=1, cuisine='American', type='r')
# r = Restaurant(name="Olive Garden", city_id=2,
#                state_id=1, cuisine='Italian', type='r')
# r = Restaurant(name="Tacos Chapala", city_id=2,
#                state_id=1, cuisine='Mexican', type='r')
# r = Restaurant(name="Buffalo Wild Wings", city_id=3,
#                state_id=1, cuisine='American', type='r')
# r = Restaurant(name="Nena's", city_id=3, state_id=1,
#                cuisine='Mexican', type='r')
# r = Restaurant(name="IHOP", city_id=4, state_id=1,
#                cuisine='American', type='r')
# r = Restaurant(name="Misaki Sushi & Bar", city_id=4,
#                state_id=1, cuisine='Japanese', type='r')
# r = Restaurant(name="Red Lobster", city_id=5,
#                state_id=1, cuisine='American', type='r')
# r = Restaurant(name="Toyo Sushi", city_id=5,
#                state_id=1, cuisine='Japanese', type='r')

# db.session.add(r)
# db.session.commit()

# adding streetfood
# s = StreetFood(name="Soma Street Food Park", city_id=1,
#                state_id=1, cuisine='American', type='s')
# s = StreetFood(name="Yummy Sushi Burrito", city_id=1,
#                state_id=1, cuisine='Japanese', type='s')
# s = StreetFood(name="El Fuego", city_id=2, state_id=1,
#                cuisine='Mexican', type='s')
# s = StreetFood(name="Shirasoni", city_id=2, state_id=1,
#                cuisine='Japanese', type='s')
# s = StreetFood(name="Korean Street Food", city_id=3,
#                state_id=1, cuisine='Korean', type='s')
# s = StreetFood(name="Baked Mac", city_id=3, state_id=1,
#                cuisine='American', type='s')
# s = StreetFood(name="Tacos Las Ranitas", city_id=4,
#                state_id=1, cuisine='Mexican', type='s')
# s = StreetFood(name="The Boys", city_id=4, state_id=1,
#                cuisine='American', type='s')
# s = StreetFood(name="The Papaya Lady", city_id=5,
#                state_id=1, cuisine='Thai', type='s')
# s = StreetFood(name="Bonchon", city_id=5, state_id=1,
#                cuisine='Korean', type='s')
# db.session.add(s)
# db.session.commit()

# adding cuisines
# c = Cuisines(cuisine='American')
# c = Cuisines(cuisine='Mexican')
# c = Cuisines(cuisine='Japanese')
# c = Cuisines(cuisine='Italian')
# c = Cuisines(cuisine='Korean')
# c = Cuisines(cuisine='Thai')
# db.session.add(c)
# db.session.commit()

# FastFood.__table__.drop(db.engine)
# Restaurant.__table__.drop(db.engine)
# StreetFood.__table__.drop(db.engine)
# Favorites.__table__.drop(db.engine)
# Cuisines.__table__.drop(db.engine)
# FastFood_Cuisine.__table__.drop(db.engine)
# City_Cuisines.__table__.drop(db.engine)
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


@app.route('/cuisine', methods=['GET', 'POST'])
@login_required
def cuisines():
    input = request.form['city-input']
    print(input)
    # cuisines = Cuisines.query.all()
    cuisines = City_Cuisines.query.filter_by(city_name=input).all()
    print(cuisines)
    return render_template('cuisines.html', cuisines=cuisines, city=input)


@app.route('/selection', methods=['GET', 'POST'])
@login_required
def selection():
    input = request.form['city']
    print(input)
    cuisine = request.form['cuisine-btn']
    print(cuisine)

    # move here to only display what is available if there is a cuisine with fastfood in that city
    joinedFastFoodResult = []
    for c, ff in db.session.query(City, FastFood).filter(
            City.name == input).filter(City.id == FastFood.city_id).filter(FastFood.cuisine == cuisine).all():
        joinedFastFoodResult.append(ff.name)

    joinedStreetFoodResult = []
    for c, s in db.session.query(City, StreetFood).filter(
            City.name == input).filter(City.id == StreetFood.city_id).filter(StreetFood.cuisine == cuisine).all():
        joinedStreetFoodResult.append(s.name)

    joinedRestaurantResult = []
    for c, r in db.session.query(City, Restaurant).filter(
            City.name == input).filter(City.id == Restaurant.city_id).filter(Restaurant.cuisine == cuisine).all():
        joinedRestaurantResult.append(r.name)

    # return render_template('selection.html', City=input, FastFood=joinedFastFoodResult, StreetFood=joinedStreetFoodResult, Restaurant=joinedRestaurantResult)
    return render_template('selection.html', City=input, cuisine=cuisine, fastfood=joinedFastFoodResult,
                           streetfood=joinedStreetFoodResult, restaurant=joinedRestaurantResult)


@app.route('/fastfood', methods=['GET', 'POST'])
@login_required
def fastfood():

    selectionType = request.form['ff-btn']
    city = request.form['city']
    cuisine = request.form['cuisine']

    print(selectionType)
    print(city)
    joinedFastFoodResult = []
    for c, ff in db.session.query(City, FastFood).filter(
            City.name == city).filter(City.id == FastFood.city_id).filter(FastFood.cuisine == cuisine).all():
        joinedFastFoodResult.append(ff.name)

    return render_template('fastfood.html', fastfood=joinedFastFoodResult)


@app.route('/streetfood', methods=['GET', 'POST'])
@login_required
def streetfood():
    streetfoodInfo = request.form['s-btn']
    city = request.form['city']
    cuisine = request.form['cuisine']

    joinedStreetFoodResult = []
    for c, s in db.session.query(City, StreetFood).filter(
            City.name == city).filter(City.id == StreetFood.city_id).filter(StreetFood.cuisine == cuisine).all():
        joinedStreetFoodResult.append(s.name)

    print(streetfoodInfo)
    return render_template('streetfood.html', streetfood=joinedStreetFoodResult)


@app.route('/restaurant', methods=['GET', 'POST'])
@login_required
def restaurant():
    restaurantInfo = request.form['r-btn']
    city = request.form['city']
    cuisine = request.form['cuisine']
    print(restaurantInfo)

    joinedRestaurantResult = []
    for c, r in db.session.query(City, Restaurant).filter(
            City.name == city).filter(City.id == Restaurant.city_id).filter(Restaurant.cuisine == cuisine).all():
        joinedRestaurantResult.append(r.name)

    return render_template('restaurant.html', restaurant=joinedRestaurantResult)


@app.route('/favorites', methods=['GET', 'POST'])
def favorites():

    # maybe add a column to favorites where indicates top 3 or just list them all
    # with details

    favorites = Favorites.query.all()
    fastfoodFavorites = Favorites.query.filter_by(type='ff').all()
    restaurantFavorites = Favorites.query.filter_by(type='r').all()
    streetfoodFavorites = Favorites.query.filter_by(type='s').all()

    print(favorites)
    return render_template('favorites.html', favorites=favorites, fastFavs=fastfoodFavorites,
                           restFavs=restaurantFavorites, streetFavs=streetfoodFavorites)


@app.route('/addfavorite', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':

        type = request.form['type']
        if type == 'ff':
            name = request.form['edit']
            newFavorite = Favorites(name=name, type=type)
            db.session.add(newFavorite)
            db.session.commit()
        elif type == 's':
            name = request.form['edit']
            newFavorite = Favorites(name=name, type=type)
            db.session.add(newFavorite)
            db.session.commit()
        elif type == 'r':
            name = request.form['edit']
            newFavorite = Favorites(name=name, type=type)
            db.session.add(newFavorite)
            db.session.commit()

    return redirect(url_for('favorites'))


@app.route('/deleteFavorite', methods=['GET', 'POST'])
def delete():
    name = request.form['selected_option']
    print(name)
    Favorites.query.filter_by(name=name).delete()
    db.session.commit()

    return redirect(url_for('favorites'))


@app.route('/list', methods=['GET', 'POST'])
def list():

    ffPlaces = FastFood.query.all()
    sPlaces = StreetFood.query.all()
    rPlaces = Restaurant.query.all()
    print(ffPlaces)
    return render_template('list.html', fastfood=ffPlaces, streetfood=sPlaces, restaurant=rPlaces)


@app.route('/congrats', methods=['GET', 'POST'])
def congrats():
    selection = request.form['selected']

    return render_template('congrats.html', selection=selection)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
