from flask import Flask, render_template, request, redirect, url_for
import ibm_db

app = Flask(__name__)

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=2d46b6b4-cbf6-40eb-bbce-6251e6ba0300.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32328;SECURITY=SSL;SSLServiceCertificate=DigiCertGlobalRootCA.crt;UID=vgn43463;PWD=kDssNk4shnXqThgr",'','')

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/aboutus')
def login(): 
    return render_template('aboutus.html')

@app.route("/signin")
def blog():
    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/doSignin',methods = ['POST', 'GET'])
def doSignin():
  if request.method == 'POST':

    email = request.form['email']
    password = request.form['password']

    sql = "SELECT * FROM users WHERE email =? AND password=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.bind_param(stmt,2,password)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)

    if account:
      return render_template('index.html', msg="Successfully signed in")
    else:
        return render_template('signin.html', msg="Invalid credentials")


@app.route('/doSignup',methods = ['POST', 'GET'])
def doSignup():
  if request.method == 'POST':

    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    cpassword = request.form['cpassword']

    if password!=cpassword:
        return render_template('signup.html', msg="Password don't match")

    sql = "SELECT * FROM users WHERE email =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)

    if account:
      return render_template('signup.html', msg="Email already exists")
    else:
      insert_sql = "INSERT INTO users (name,email,password) VALUES (?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, email)
      ibm_db.bind_param(prep_stmt, 3, password)
      ibm_db.execute(prep_stmt)
    
    return render_template('index.html', msg="You have successfully signed up")


app.run()