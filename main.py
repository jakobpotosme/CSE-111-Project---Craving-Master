import sqlite3
from sqlite3 import Error


_dbFile = r"project.db"

# create a database connection
conn = sqlite3.connect(_dbFile)

try:
    sql = """CREATE TABLE Consumer (
                c_name char(25) PRIMARY KEY not null,
                c_phone varchar(25) not null,
                c_age INTEGER not null,
                c_citykey INTEGER not null,
                c_destination varchar(25) not null
            );
            CREATE TABLE Application (
                customer_name char(25) not null,
                fastfood_key INTEGER not null,
                restaurant_key INTEGER not null,
                streetfood_key INTEGER not null,
                FOREIGN KEY(customer_name) REFERENCES Consumer(c_name),
                FOREIGN KEY(fastfood_key) REFERENCES FastFood(ff_key),
                FOREIGN KEY(restaurant_key) REFERENCES Restaurant(r_key),
                FOREIGN KEY(streetfood_key) REFERENCES StreetFood(sf_key)
            );
            CREATE TABLE City(
                city_key INTEGER PRIMARY KEY not null,
                city_name char(25) not null,
                city_statekey INTEGER not null
            );
            CREATE TABLE FastFood (
                ff_name char(25) not null,
                ff_address varchar(50) not null,
                ff_phone varchar(25) not null,
                ff_citykey INTEGER not null,
                ff_key INTEGER PRIMARY KEY not null,
                ff_statekey INTEGER not null
            );
            CREATE TABLE FastFood_City(
                city_citykey INTEGER not null,
                fastfood_citykey INTEGER not null,
                FOREIGN KEY(city_citykey) REFERENCES City(city_key),
                FOREIGN KEY(fastfood_citykey) REFERENCES FastFood(ff_citykey)
            );
            CREATE TABLE Restaurant(
                r_name char(25) not null,
                r_statekey INTEGER not null,
                r_phone varchar(25) not null,
                r_address varchar(50) not null,
                r_key INTEGER PRIMARY KEY not null,
                r_citykey INTEGER not null
            );
            CREATE TABLE Restaurant_City(
                city_citykey INTEGER not null,
                rest_citykey INTEGER not null,
                FOREIGN KEY(city_citykey) REFERENCES City(city_key),
                FOREIGN KEY(rest_citykey) REFERENCES Restaurant(r_citykey)
            );
            CREATE TABLE StreetFood(
                sf_name char(25) not null,
                sf_phone varchar(25) not null,
                sf_citykey INTEGER not null,
                sf_key INTEGER PRIMARY KEY not null,
                sf_address varchar(50) not null
            );
            CREATE TABLE StreetFood_City(
                city_citykey INTEGER not null,
                streetfood_citykey INTEGER not null,
                FOREIGN KEY(city_citykey) REFERENCES City(city_key),
                FOREIGN KEY(streetfood_citykey) REFERENCES StreetFood(sf_citykey)
            );
            CREATE TABLE State(
                s_statekey INTEGER PRIMARY KEY not null,
                s_name char(25) not null
            );
            CREATE TABLE Favorites(
                f_name char(25) not null

            );

            """
    conn.executescript(sql)

    conn.commit()
    print("success")
except Error as e:
    conn.rollback()
    print(e)


print('closed DB')
conn.close()
