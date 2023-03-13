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

def authenticate_user_account(username, password):
    get_authentication_info_query = f"SELECT user_id,password FROM user WHERE username=\"{username}\""
    tapa_cursor.execute(get_authentication_info_query)
    auth_info = tapa_cursor.fetchall()
    if len(auth_info) == 0:
        return -2
    user_id = auth_info[0][0]
    correct_password = auth_info[0][1]
    if password == correct_password:
        return int(user_id)
    else:
        return -1

app = Flask(__name__)
 
@app.route('/')
def index():
    return "Getting started"

@app.route('/createAccount/<string:username>/<string:password>')
def create_account(username=None,password=None): 
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
    
@app.route('/removeAccount/<string:username>/<string:password>')
def remove_account(username,password):
    user_id = authenticate_user_account(username,password)
    if user_id >= 0:
        delete_account_query = f"DELETE FROM user WHERE user_id=\"{user_id}\""
        tapa_cursor.execute(delete_account_query)
        db_conn.commit()
        return "User account has been removed."
    elif user_id == -1:
        return "User authentication failed"
    elif user_id == -2:
        return "No account with such username exists"

    
@app.route('/updateUsername/<string:username>/<string:password>/<string:new_username>')
def update_username(username,password,new_username):
    user_id = authenticate_user_account(username,password)
    if user_id >= 0:
        get_curr_username_querry = f"SELECT username FROM user WHERE user_id={user_id}"
        tapa_cursor.execute(get_curr_username_querry)
        curr_username = tapa_cursor.fetchall()[0][0]

        if new_username != curr_username:
            update_username_query = f"UPDATE user SET username=\"{new_username}\" WHERE user_id=\"{user_id}\""
            tapa_cursor.execute(update_username_query)
            db_conn.commit()
            return "Successfully updated to new username"
        else:
            return "You are already using this username."
    elif user_id == -1:
        return "User authentication failed"
    elif user_id == -2:
        return "No account with such username exists"

@app.route('/updatePassword/<string:username>/<string:password>/<string:new_password>')
def update_password(username,password,new_password):
    user_id = authenticate_user_account(username,password)
    if user_id >= 0:
        get_curr_password_query = f"SELECT password FROM user WHERE user_id={user_id}"
        tapa_cursor.execute(get_curr_password_query)
        curr_password = tapa_cursor.fetchall()[0][0]
        
        if new_password != curr_password:
            update_password_query = f"UPDATE user SET password=\"{new_password}\" WHERE user_id=\"{user_id}\""
            tapa_cursor.execute(update_password_query)
            db_conn.commit()
            return "Successfully updated to new password"
        else:
            return "You are already using this password; choose a different one."
    elif user_id == -1:
        return "User authentication failed"
    elif user_id == -2:
        return "No account with such username exists"
    
 
@app.route('/createPostKey/<string:username>/<string:password>/<string:post_key>')
def create_post_key(username,password,post_key):
    user_id = authenticate_user_account(username,password)
    get_users_postkeys_query = f"SELECT post_key FROM user_post_key WHERE user_id=\"{user_id}\""
    tapa_cursor.execute(get_users_postkeys_query)
    get_post_key_repl = tapa_cursor.fetchall()
    post_keys = []
    for repl in get_post_key_repl:
        post_keys.append(repl[0])
    
    if user_id >= 0:
        if post_key not in post_keys:
            add_post_key_query = f"INSERT INTO user_post_key(user_id,post_key) VALUES({user_id},\"{post_key}\")"
            print("add post key query : ", add_post_key_query)
            tapa_cursor.execute(add_post_key_query)
            db_conn.commit()
            return f"Successfully added post key associated with user {user_id}"
        else:
            return "This post key already exists. Try create a different post key."
    elif user_id == -1:
        return "User authentication failed"
    elif user_id == -2:
        return "No account with such username exists"
    
@app.route('/deletePostKey/<string:username>/<string:password>/<string:post_key>')
def delete_post_key(username,password,post_key):
    user_id = authenticate_user_account(username,password)
    get_users_postkeys_query = f"SELECT post_key FROM user_post_key WHERE user_id=\"{username}\""
    tapa_cursor.execute(get_users_postkeys_query)
    get_post_key_repl = tapa_cursor.fetchall()
    post_keys = []
    for repl in get_post_key_repl:
        post_keys.append(repl[0])
    
    if user_id >= 0:
        if post_key in post_keys:
            delete_post_key_query = f"DELETE FROM user_post_key WHERE post_key=\"{post_key}\""
            tapa_cursor.execute(delete_post_key_query)
            db_conn.commit()
            return "Successfully removed post key"
        else:
            return "This post key does not exist."
    elif user_id == -1:
        return "User authentication failed"
    elif user_id == -2:
        return "No account with such username exists"
    
@app.route('/createPortfolio/<string:username>/<string:password>/<string:portfolio_name>/<string:introduction>/<string:phone>/<string:email>')
def create_portfolio(username,password,portfolio_name,introduction,phone,email):
    user_id = authenticate_user_account(username,password)
    get_existing_portfolio_query = f"SELECT portfolio_link FROM user_to_portfolio WHERE user_id>0"
    tapa_cursor.execute(get_existing_portfolio_query)
    existing_portfolios = [row[0] for row in tapa_cursor.fetchall()]
    if user_id >= 0:
        if portfolio_name not in existing_portfolios:
            create_new_portfolio_query = f"INSERT INTO portfolio(portfolio_link,introduction,contact_phone,contact_email) VALUES(\"{portfolio_name}\",\"{introduction}\",\"{phone}\",\"{email}\")"
            tapa_cursor.execute(create_new_portfolio_query)
            db_conn.commit()
            
            link_user_to_portfolio_query = f"INSERT INTO user_to_portfolio(user_id,portfolio_link) VALUES(\"{user_id}\",\"{portfolio_name}\")"
            tapa_cursor.execute(link_user_to_portfolio_query)
            db_conn.commit()
            return f"Successfully created a new portfolio for user \"{username}\""
        else:
            return "This portfolio name has already been used"
    elif user_id == -1:
        return "User authentication failed"
    elif user_id == -2:
        return "No account with such username exists"
    
@app.route('/deletePortfolio/<string:username>/<string:password>/<string:portfolio_name>')
def delete_portfolio(username,password,portfolio_name):
    user_id = authenticate_user_account(username,password)
    get_existing_portfolio_query = f"SELECT portfolio_link FROM portfolio"
    tapa_cursor.execute(get_existing_portfolio_query)
    existing_portfolio_names = [row[0] for row in tapa_cursor.fetchall()]
    
    if user_id >=0:
        if portfolio_name in existing_portfolio_names:
            delete_portfolio_query = f"DELETE FROM portfolio WHERE portfolio_link=\"{portfolio_name}\""
            tapa_cursor.execute(delete_portfolio_query)
            db_conn.commit()

            return f"Successfully deleted potfolio link {portfolio_name}"
        else:
            return f"This portfolio does not exist"
    elif user_id == -1:
        return "User authentication failed"
    elif user_id == -2:
        return "No account with such username exists"
if __name__=="__main__":
    app.run(debug=True)