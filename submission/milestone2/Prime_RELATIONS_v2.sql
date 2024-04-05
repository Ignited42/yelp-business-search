CREATE TABLE Business(
    Business_id CHAR(22) PRIMARY KEY,
    Name VARCHAR(90) NOT NULL,
    Address VARCHAR(90),
    City VARCHAR(30),
    State CHAR(2),
    Zipcode CHAR(5),
    Total_checkin INT,
    Num_review INT,
    Business_rating FLOAT
);
CREATE TABLE Review(
    Review_id CHAR(22) PRIMARY KEY,
    User_id CHAR(22) REFERENCES YelpUser(User_id),
    Rating INT,
    Business_id CHAR(22) REFERENCES Business(Business_id)
);
CREATE TABLE YelpUser(
    User_id CHAR(22) PRIMARY KEY,
    Name VARCHAR(40) NOT NULL
);
CREATE TABLE CheckinLogs(
    Checkin_count INT,
    Checkin_day VARCHAR(9),
    Checkin_time VARCHAR(5),
    Business_id CHAR(22) REFERENCES Business(Business_id)
);