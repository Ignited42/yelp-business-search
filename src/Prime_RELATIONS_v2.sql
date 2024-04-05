CREATE TABLE Business(
    Business_id CHAR(22) PRIMARY KEY,
    Name VARCHAR(30) NOT NULL,
    Address VARCHAR(40),
    City VARCHAR(30),
    State VARCHAR(20),
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
    Name VARCHAR(25) NOT NULL
);
CREATE TABLE CheckinLogs(
    Checkin_total INT,
    Checkin_day TEXT,
    Checkin_time TEXT,
    Business_id CHAR(22) REFERENCES Business(Business_id)
);

-- UPDATE dup_business
-- SET numCheckins = (SELECT sum FROM numcheckins WHERE numcheckins.business_id = dup_business.business_id),
--     reviewcount = (SELECT count FROM reviewcount WHERE reviewcount.business_id = dup_business.business_id),
--     reviewrating = (SELECT average_rating FROM reviewrating WHERE reviewrating.business_id = dup_business.business_id);
