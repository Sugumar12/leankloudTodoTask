from flask_mysqldb import MySQL 

def setDBConnection(app):
    app.config["MYSQL_HOST"] = "localhost"
    app.config["MYSQL_USER"] = "root"
    app.config["MYSQL_PASSWORD"] = "root"
    app.config["MYSQL_DB"] = "lk_todo"

    # Initializing DB for the App
    mysql = MySQL(app)
    return mysql