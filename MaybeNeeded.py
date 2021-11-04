# CREATE TABLE FastFood(
#     ff_name char(25) not null,
#     ff_address varchar(50) not null,
#     ff_phone varchar(25) not null,
#     ff_citykey INTEGER not null,
#     ff_key INTEGER PRIMARY KEY not null,
#     ff_statekey INTEGER not null
# )

# CREATE TABLE Restaurant(
#     r_name char(25) not null,
#     r_statekey INTEGER not null,
#     r_phone varchar(25) not null,
#     r_address varchar(50) not null,
#     r_key INTEGER PRIMARY KEY not null,
#     r_citykey INTEGER not null
# )

# CREATE TABLE StreetFood(
#     sf_name char(25) not null,
#     sf_phone varchar(25) not null,
#     sf_citykey INTEGER not null,
#     sf_key INTEGER PRIMARY KEY not null,
#     sf_address varchar(50) not null
# )
