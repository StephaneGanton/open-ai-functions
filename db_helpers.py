import mysql.connector

host = "localhost"
user = "root"
password = ""
database = "atliq_college_db"

def get_db_cursor():
    # Create a connection to the MySQL database
    db = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    # Create a cursor to interact with the database
    cursor = db.cursor()

    return db, cursor

def close_db_connection(db, cursor):
    #disconnect from server
    cursor.close()
    db.close()

def get_marks(params):
    db, cursor = get_db_cursor()
    cursor.callproc('get_marks', [params.get('student_name', ''), params.get('semester', ''), params.get('operation', '')])
    result = None

    for res in cursor.stored_results():
        result = float(res.fetchone()[0]) #Fetch the first column of the first row
    
    close_db_connection(db, cursor)

    return result

def get_fees(params):
    db, cursor = get_db_cursor()
    cursor.callproc('get_fees', [params.get('student_name', ''), params.get('semester', ''), params.get('fees_type', '')])
    result = None

    for res in cursor.stored_results():
        result = float(res.fetchone()[0]) #Fetch the first column of the first row
    
    close_db_connection(db, cursor)

    return result

# Create a dictionary mapping function names to function objects
functions = {
    "get_marks": get_marks,
    "get_fees": get_fees,
}

if __name__ == "__main__":
    print(get_marks({
        'semester': 3,
        'operation': 'avg',
    }))

    print(get_fees({
        'student_name': 'Peter Pandey',
        'semester': 1,
        'fees_type': 'paid'
    }))