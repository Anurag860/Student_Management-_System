
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  

db_path = os.path.join("database", "students.db")
db = SQLiteDB(db_path)
       
@app.route("/")