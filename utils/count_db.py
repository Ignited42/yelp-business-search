import psycopg2 as psy2

try:
    infile = open("bin/password.txt", "r")
    password_string = infile.read()
    infile.close()
except:
    print("Create a file named 'password.txt' in the bin folder and type your pSQL password into it!")


def countRowsInTable(database, tableName):
    # Open connection to database
    try:
        pysql_string = "dbname='"+ database + "' user='postgres' host='localhost' password='" + password_string + "'"
        conn = psy2.connect(pysql_string)
    except RuntimeError as error:
        print(error)
        print("Unable to connect to database!")

    curr = conn.cursor()
    sql_str = "SELECT COUNT(*) from " + tableName

    curr.execute(sql_str)
    conn.commit()
    
    result = curr.fetchone()

    return result[0]


if __name__ == "__main__":
    f = open("./submission/milestone2/Prime_TableSizes.txt", "w")
    
    f.write(f"business    = " + str(countRowsInTable("yelpdb","business")))
    f.write(f"\nreview      = " + str(countRowsInTable("yelpdb","review")))
    f.write(f"\nyelpuser    = " + str(countRowsInTable("yelpdb","yelpuser")))
    f.write(f"\ncheckinlogs = " + str(countRowsInTable("yelpdb","checkinlogs")))

    f.close()