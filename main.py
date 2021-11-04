from os import close
import sqlite3
from sqlite3 import Error


def openConnection(_dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Open database: ", _dbFile)

    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

    return conn


def closeConnection(_conn, _dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Close database: ", _dbFile)

    try:
        _conn.close()
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")


def createTable(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Create tables")
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
        _conn.executescript(sql)

        _conn.commit()
        print("success")
    except Error as e:
        _conn.rollback()
        print(e)


def dropTable(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Drop tables")
    try:
        sql = """
        DROP TABLE Application;
        DROP TABLE City;
        DROP TABLE Consumer;
        DROP TABLE FastFood;
        DROP TABLE FastFood_City;
        DROP TABLE Favorites;
        DROP TABLE Restaurant;
        DROP TABLE Restaurant_City;
        DROP TABLE State;
        DROP TABLE StreetFood;
        DROP TABLE StreetFood_City;
        
        """
        _conn.executescript(sql)

        _conn.commit()
    except Error as e:
        _conn.rollback()
        print(e)
    print("++++++++++++++++++++++++++++++++++")


def main():
    _dbFile = r"project.db"

    # create a database connection
    # conn = sqlite3.connect(_dbFile)
    conn = openConnection(_dbFile)
    with conn:
        createTable(conn)
        # dropTable(conn)

    closeConnection(conn, _dbFile)


if __name__ == '__main__':
    main()
