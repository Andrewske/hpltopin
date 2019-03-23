import psycopg2, secrets
from werkzeug.security import generate_password_hash

# connect to the database
class DatabaseConnection:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="kevin",
                password=secrets.db_password,
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except:
            print("Cannot connect to database")

    def create_user(self, username, access_token, password_hash):
        create_user_command = (
            "INSERT INTO users(username, access_token) VALUES ('"
            + username
            + "' , '"
            + access_token
            + "') ON CONFLICT (username) DO UPDATE SET access_token = '"
            + access_token
            + "','"
            + password_hash
            + "';"
        )
        self.cursor.execute(create_user_command)

    def create_board(self, username, board_name, url):
        create_board_command = (
            "INSERT INTO boards(id, username, board_name, board_url) VALUES ('"
            + username
            + "','"
            + board_name
            + "','"
            + url
            + "') ON CONFLICT (username, board_name) DO NOTHING"
        )
        self.cursor.execute(create_board_command)

    def create_pin(self, username, name, url, img_url):
        create_pin_command = (
            "INSERT INTO boards(id, username, name, url, img_url) VALUES ('"
            + username
            + "','"
            + name
            + "','"
            + url
            + "','"
            + img_url
            + "') ON CONFLICT (username, name) DO UPDATE SET URL = '"
            + url
            + "';"
        )
        self.cursor.execute(create_pin_command)


if __name__ == "__main__":
    con = DatabaseConnection()
    con.create_user("kevinbigfoot", "new_acces_token")  # secrets.pinterest_test_key)


# con =
# #create cursor
# cur = con.cursor()

# #IMPORTANT
# #remember to commit changes
# con.commit()
# #close the cursor
# cur.close()
# #close the connection
# con.close()

