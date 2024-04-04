CREATE TABLE Business(
    Business_id CHAR(20) PRIMARY KEY,
    Name VARCHAR(25) NOT NULL,
    Address VARCHAR(40),
    City CHAR(15), 
    State VARCHAR(20)
    Total_Checkin INT,
    Num_of_Review INT,
    Business_rating FLOAT 
);

CREATE TABLE Review(
    Review_id VARCHAR(25) NOT NULL,
    User_id VARCHAR(25) PRIMARY KEY,
    Business_id VARCHAR(30),
    Rating INT
    FOREIGN KEY Business_id REFERENCES Business(Business_id)
);

CREATE TABLE User(
    User_id VARCHAR(25) PRIMARY KEY,
    Name VARCHAR(25) NOT NULL,
    FOREIGN KEY user_id REFERENCES Review (user_id)
);

CREATE TABLE Check-in_Logs(
    Check_in_total INT
    Check_in_day VARCHAR(15)
    Check-in_time VARCHAR(15) 
    FOREIGN KEY Business_id REFERENCES Business(Business_id)
);


