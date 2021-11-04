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
                    c_citykey INTEGER not null
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
                    sf_citykey INTEGER not null,
                    sf_key INTEGER PRIMARY KEY not null,
                    sf_statekey INTEGER not null
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
        print("Successfully dropped tables")
    except Error as e:
        _conn.rollback()
        print(e)
    print("++++++++++++++++++++++++++++++++++")


def populateTables(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Populate tables")
    try:
        sql = """
        INSERT INTO Consumer(c_name,c_phone,c_age,c_citykey)
        VALUES ("Henry", "209-123-4567",21,1),
            ("Blake", "209-321-7654",22,2),
            ("James", "209-121-1654",23,3),
            ("John", "209-321-1754",20,4),
            ("Adam", "209-345-1664",24,5),
            ("Arianna", "209-235-6764",21,6),
            ("Rebecca", "209-785-6234",23,7),
            ("Mary", "209-955-6454",45,8),
            ("George", "209-376-3354",50,9),
            ("Victor", "209-745-8903",35,10);

        INSERT INTO City(city_key,city_name,city_statekey)
        VALUES(1,"San Francisco", 1),
            (2,"Merced", 1),
            (3,"Stockton", 1),
            (4,"Sacramento", 1),
            (5,"Los Angelas", 1);

        INSERT INTO State(s_statekey,s_name)
        VALUES(1,"California");

        INSERT INTO FastFood(ff_name,ff_citykey,ff_key,ff_statekey)
        VALUES("Wendy's",1,1,1),
            ("Taco Bell",2,2,1),
            ("Chick-fil-A",3,3,1),
            ("Starbucks",4,4,1),
            ("McDonald's",5,5,1);

        INSERT INTO FastFood_City(city_citykey,fastfood_citykey)
        VALUES(1,1),
            (2,2),
            (3,3),
            (4,4),
            (5,5);

        INSERT INTO Restaurant(r_name,r_citykey,r_key,r_statekey)
        VALUES("Applebee's",1,1,1),
            ("Olive Garden",2,2,1),
            ("Buffalo Wild Wings",3,3,1),
            ("IHOP",4,4,1),
            ("Red Lobster",5,5,1);

        INSERT INTO Restaurant_City(city_citykey,rest_citykey)
        VALUES(1,1),
            (2,2),
            (3,3),
            (4,4),
            (5,5);

        INSERT INTO StreetFood(sf_name,sf_citykey,sf_key,sf_statekey)
        VALUES ("Soma Street Food Park",1,1,1),
            ("El Fuego",2,2,1),
            ("Korean Street Food",3,3,1),
            ("Tacos Las Ranitas",4,4,1),
            ("The Papaya Lady",5,5,1);

        INSERT INTO StreetFood_City(city_citykey,streetfood_citykey)
        VALUES(1,1),
            (2,2),
            (3,3),
            (4,4),
            (5,5);

        INSERT INTO Application(customer_name,fastfood_key,restaurant_key,streetfood_key)
            VALUES("Henry",1,1,1);
            
        """
        _conn.executescript(sql)

        _conn.commit()
        print("Successfully populated tables")
    except Error as e:
        _conn.rollback()
        print(e)


def main():
    _dbFile = r"project.db"

    # create a database connection
    # conn = sqlite3.connect(_dbFile)
    conn = openConnection(_dbFile)
    with conn:
        dropTable(conn)
        createTable(conn)
        populateTables(conn)

    closeConnection(conn, _dbFile)


if __name__ == '__main__':
    main()
