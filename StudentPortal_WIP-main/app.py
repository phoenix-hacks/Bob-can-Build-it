from flask import Flask, render_template, request, redirect, url_for,jsonify
import mysql.connector

app = Flask(__name__)
print('Starting')
# Function to check user input in the MySQL database
def check_user_input(user_input):
    print("Checking user input")
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host="localhost",      # Your MySQL host
        user="root",           # Your MySQL username
        password="Skibidi_Sigma",   # Your MySQL password
        database="student_portal"  # The database to check
    )
    
    # Ensure the connection is successful
    if conn.is_connected():
        cursor = conn.cursor()

        # Query to check if the user input exists in the USN field
        cursor.execute("SELECT * FROM student WHERE USN = %s", (user_input,))
        
        global temp
        temp = user_input
        
        result = cursor.fetchone()  # Use fetchone() for a single record
        print(result)
        conn.close()
        
        return result  # Returns None if no match, otherwise the matched user data
    else:
        print("Database connection failed.")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    print("works here2")
    if request.method == 'POST':
        # Get user input from the form
        user_input = request.form.get('userInput')
        print("User Input:", user_input)

        # Check if input is provided
        if not user_input:
            return "USN cannot be empty.", 400  # Return an error if USN is empty

        # Check the input in the database
        result = check_user_input(user_input)
        
        if result:
            return redirect(url_for('select'))  # Redirect to select.html if found
        else:
            return "No matching USN found", 404  # If not found, show an error
    else:
        print("thhis dont work here!")
    return render_template('index.html')  # Render the input form

@app.route('/select')
def select():
    print("works here")
    return render_template('select.html')  # Render the select.html page when redirected

@app.route('/dashboard')
def dashboard():
    print("works here")
    return render_template('dashboard.html')  # Render the dashboard.html page when redirected

#GET ATTENDACE
@app.route('/get_attendance')
def get_attendance():
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Skibidi_Sigma",
            database="student_portal"
        )
        cursor = conn.cursor(dictionary=True)
        
        # Query to fetch attendance data
        cursor.execute("SELECT Classes_Taken, Classes_Attended FROM Attendance")
        rows = cursor.fetchall()
        
        # Close the connection
        cursor.close()
        conn.close()
        
        # Return the data as JSON
        return jsonify(rows)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({"error": "Unable to fetch data"}), 500

    
if __name__ == '__main__':
    app.run(debug=True)
