import json
import psycopg2 as psy2
import psycopg2.extras as psy2b

try:
    infile = open("bin/password.txt", "r")
    password_string = infile.read()
    infile.close()
except:
    print("Create a file named 'password.txt' in the bin folder and type your pSQL password into it!")

def cleanStr4SQL(s):
    return s.replace("'","''").replace("\n"," ")

def getAttributes(attributes):
    L = []
    for (attribute, value) in list(attributes.items()):
        if isinstance(value, dict):
            L += getAttributes(value)
        else:
            L.append((attribute,value))
    return L

#==========================================================================================================

def parseBusinessData():
    """
    Parses the yelp_business.JSON file and inputs tuples into the 
    'business' table of our SQL database.
    """

    print("Parsing businesses...")
    #read the JSON file
    with open('./dataset/Yelp-CptS451/yelp_business.JSON','r') as f:
        line = f.readline()
        count_line = 0

        # Open connection to database
        try:
            pysql_string = "dbname='yelpdb' user='postgres' host='localhost' password='" + password_string + "'"
            conn = psy2.connect(pysql_string)
        except RuntimeError as error:
            print(error)
            print("Unable to connect to database!")

        sql_batchTuple = []
        curr = conn.cursor()

        sql_str = \
            """INSERT INTO business(Business_id, Name, Address, City, State, Zipcode, Total_Checkin, Num_review, Business_rating)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        #read each JSON abject and extract data
        while line:
            data = json.loads(line)

            sql_tuple = (data['business_id'], cleanStr4SQL(data['name']), cleanStr4SQL(data['address']), \
                         cleanStr4SQL(data['city']), data['state'], data['postal_code'], 0, 0, 0.0)

            sql_batchTuple.append(sql_tuple)

            line = f.readline()
            count_line +=1

            if (count_line % 20 == 0):
                psy2b.execute_batch(curr, sql_str, tuple(sql_batchTuple))
                sql_batchTuple = []
                conn.commit()
        psy2b.execute_batch(curr, sql_str, tuple(sql_batchTuple))
        conn.commit()  
    print(count_line)
    f.close()

#==========================================================================================================

def parseUserData():
    """
    Parses the yelp_user.JSON file and inputs tuples into the 
    'user' table of our SQL database.
    """
    print("Parsing users...")
    #reading the JSON file
    with open('./dataset/Yelp-CptS451/yelp_user.JSON','r') as f:
        line = f.readline()
        count_line = 0

        # Open connection to database
        try:
            pysql_string = "dbname='yelpdb' user='postgres' host='localhost' password='" + password_string + "'"
            conn = psy2.connect(pysql_string)
        except RuntimeError as error:
            print(error)
            print("Unable to connect to database!")
        
        sql_batchTuple = []
        curr = conn.cursor()
        
        sql_str = \
            """INSERT INTO yelpuser(user_id, name)
            VALUES (%s, %s)"""

        while line:
            data = json.loads(line)

            sql_tuple = (data['user_id'], (data["name"]))
            sql_batchTuple.append(sql_tuple)

            line = f.readline()
            count_line +=1

            if (count_line % 100 == 0):
                psy2b.execute_batch(curr, sql_str, tuple(sql_batchTuple))
                sql_batchTuple = []
                conn.commit()
        psy2b.execute_batch(curr, sql_str, tuple(sql_batchTuple))
        conn.commit()  
    print(count_line)
    f.close()

#==========================================================================================================

def parseCheckinData():
    """
    Parses the yelp_checkin.JSON file and inputs tuples into the 
    'checkinlogs' table of our SQL database.
    """
    print("Parsing checkins...")
    #reading the JSON file
    with open('./dataset/Yelp-CptS451/yelp_checkin.JSON','r') as f:
        line = f.readline()
        count_line = 0

        # Open connection to database
        try:
            pysql_string = "dbname='yelpdb' user='postgres' host='localhost' password='" + password_string + "'"
            conn = psy2.connect(pysql_string)
        except RuntimeError as error:
            print(error)
            print("Unable to connect to database!")
        
        sql_batchTuple = []
        curr = conn.cursor()
        
        sql_str = \
            """INSERT INTO checkinlogs(checkin_count, checkin_day, checkin_time, business_id)
            VALUES (%s, %s, %s, %s)"""

        #read each JSON abject and extract data
        while line:
            data = json.loads(line)
            business_id = data['business_id']
            for (dayofweek,time) in data['time'].items():
                for (hour,count) in time.items():
                    sql_tuple = (str(count), dayofweek, hour, business_id)
                    sql_batchTuple.append(sql_tuple)

            line = f.readline()
            count_line +=1

            if (count_line % 200 == 0):
                psy2b.execute_batch(curr, sql_str, tuple(sql_batchTuple))
                sql_batchTuple = []
                conn.commit()
        psy2b.execute_batch(curr, sql_str, tuple(sql_batchTuple))
        conn.commit()  
    print(count_line)
    f.close()

#==========================================================================================================

def parseReviewData():
    """
    Parses the yelp_review.JSON file and inputs tuples into the 
    'review' table of our SQL database.
    """
    print("Parsing reviews...")
    #reading the JSON file
    with open('./dataset/Yelp-CptS451/yelp_review.JSON','r') as f:
        line = f.readline()
        count_line = 0

        # Open connection to database
        try:
            pysql_string = "dbname='yelpdb' user='postgres' host='localhost' password='" + password_string + "'"
            conn = psy2.connect(pysql_string)
        except RuntimeError as error:
            print(error)
            print("Unable to connect to database!")
        
        sql_batchTuple = []
        curr = conn.cursor()

        sql_str = \
            """INSERT INTO review(review_id, user_id, rating, business_id)
            VALUES (%s, %s, %s, %s)"""
        
        while line:
            data = json.loads(line)

            sql_tuple = (data['review_id'], data['user_id'], data['stars'], data['business_id'])
            sql_batchTuple.append(sql_tuple)

            line = f.readline()
            count_line +=1

            if (count_line % 2000 == 0):
                psy2b.execute_batch(curr, sql_str, tuple(sql_batchTuple))
                sql_batchTuple = []
                conn.commit()
        psy2b.execute_batch(curr, sql_str, tuple(sql_batchTuple))
        conn.commit()  
    print(count_line)
    f.close()

parseBusinessData()
parseUserData()
parseCheckinData()
parseReviewData()

