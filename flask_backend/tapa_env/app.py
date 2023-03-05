from flask import Flask,request,url_for,redirect
import pymysql

# Initialize DB connection
db_conn = pymysql.connect(
                user = "tumaaga",
                password = "geommojam*12",
                db = "tapa",
                charset = "utf8"
)
tapa_cursor = db_conn.cursor()
# Function to execute DB query e/ time an action from DB is necessary.

app = Flask(__name__)

@app.route('/')
def index():
    return "Getting started"

@app.route('/register/<string:username>/<string:password>')
def register(username=None,password=None): 
    # Check if username from request form is already in db
    select_username_query = f"SELECT username FROM user"
    tapa_cursor.execute(select_username_query)
    existing_usernames = [row[0] for row in tapa_cursor.fetchall()]
    if username in existing_usernames:
        return "username already exists; choose a different username"
    else:
        insert_new_user_query = f"INSERT INTO user(username,password) VALUES(\"{username}\",\"{password}\")"
        tapa_cursor.execute(insert_new_user_query)
        db_conn.commit()
        return "successfully registered a new user"

if __name__=="__main__":
    app.run(debug=True)