import mysql.connector
from mysql.connector import Error

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='sdp',
            user='root',
            password='root123'
        )

        if connection.is_connected():
            print('Successfully connected to the database')
            cursor = connection.cursor()

            # Create table
            create_table_query = """
                CREATE TABLE IF NOT EXISTS employees (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    position VARCHAR(50),
                    salary INT
                )
            """
            cursor.execute(create_table_query)
            print("Table 'employees' created successfully")

            # Insert records
            insert_query = """
                INSERT INTO employees (name, position, salary)
                VALUES (%s, %s, %s)
            """
            employees_records = [
                ('alice', 'manager', 30),
                ('bob', 'developer', 50),
                ('charlie', 'tester', 45)
            ]
            cursor.executemany(insert_query, employees_records)
            connection.commit()
            print(f"{cursor.rowcount} records inserted into 'employees' table")

            # Select records
            select_query = "SELECT * FROM employees"
            cursor.execute(select_query)
            records = cursor.fetchall()
            print("Fetching data from 'employees' table:")
            for row in records:
                print(f"ID: {row[0]}, Name: {row[1]}, position: {row[2]}, salary: {row[3]}")

            # Update records
            update_query = """
                UPDATE employees
                SET position = %s
                WHERE name = %s
            """
            data_to_update = ('developer', 'anu')
            cursor.execute(update_query, data_to_update)
            connection.commit()
            print(f"Record updated for {cursor.rowcount} employees(s).")

            # Verify the update
            cursor.execute(select_query)
            records = cursor.fetchall()
            print("Data after update:")
            for row in records:
                print(f"ID: {row[0]}, Name: {row[1]}, position: {row[2]}, salary: {row[3]}")

           # Delete records
            delete_query = "DELETE FROM employees WHERE name = %s"
            name_to_delete = ('bob',)
            cursor.execute(delete_query, name_to_delete)
            connection.commit()
            print(f"Record deleted for {cursor.rowcount} employeent(s).")

            # Verify the deletion
            cursor.execute(select_query)
            records = cursor.fetchall()
            print(records)
            print("Data after deletion:")
            for row in records:
                print(f"ID: {row[0]}, Name: {row[1]}, position: {row[2]}, salary: {row[3]}")

            # Drop table
            #drop_table_query = "DROP TABLE IF EXISTS students"
            #cursor.execute(drop_table_query)
            #print("Table 'employee' dropped successfully.")

            # Close the cursor
            cursor.close()

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

# Call the function to execute CRUD operations
connect_to_database()