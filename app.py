from flask import Flask,redirect,render_template,flash,request,send_file,url_for,session
from flask_session import Session
import mysql.connector
from otp import genotp
from cmail import sendmail
from stoken import token,dtoken
import io
import os
app=Flask(__name__)
app.config['SESSION_TYPE']='filesystem'
mydb=mysql.connector.connect(host='localhost',username='root',password='root',db='gallery')
app.secret_key=b'\xed+\xa2D\x1e\x88h\xde\x83v\x8c\xe46V\x80'
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/signin',methods=['GET','POST'])
def signin():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        confirm_password=request.form['confirm-password']
        print(name,email,password)
        if password==confirm_password:
            otp=genotp()
            data={'name':name,'email':email,'password':password,'otp':otp}
            print(data)
            subject='Admin verify for BUYMORE'
            body=f'Use this otp for verification {otp}'
            sendmail(email=email,subject=subject,body=body)
            return redirect(url_for('verifyotp',var1=token(data=data)))
    return render_template('signin.html')
@app.route('/verifyotp/<var1>',methods=['GET','POST'])
def verifyotp(var1):
    data=dtoken(data=var1)
    if request.method=='POST':
        uotp=request.form['otp']
        if uotp==data['otp']:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('insert into users(email,name,password) values(%s,%s,%s)',[data['email'],data['name'],data['password']])
            mydb.commit()
            cursor.close()
            return redirect(url_for('login'))
    return render_template("otp.html")
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['username']
        password=request.form['password']
        session['email']=email
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select password from users where email=%s',[email])
        dat=cursor.fetchone()[0]
        dbpassword=dat
        print(dbpassword)
        password=password.encode('utf-8')
        print("or",password)
        print("Db",dbpassword)
        if dbpassword==password:
            return redirect(url_for('photos'))
        else:
            return "Invalid Credentials"
    return render_template('login.html')
@app.route('/photos',methods=['GET','POST'])
def photos():
    print(session.get('email'))
    if not session.get('email'):
        return redirect(url_for('login'))
    else:
        return render_template('photos.html')
@app.route('/addphotos',methods=['GET','POST'])
def addphotos():
    if not session.get('email'):
        return redirect(url_for('login'))
    else:
        if request.method=='POST':
            photo_name=request.form['name']
            file = request.files['photo']
            print(file)
            filename=genotp()+'.'+file.filename.split('.')[-1]
            print(filename)
            path=os.path.dirname(os.path.abspath(__file__))
            static_path=os.path.join(path,'static')
            file.save(os.path.join(static_path,filename))
            cursor=mydb.cursor(buffered=True)
            cursor.execute('insert into photos(photo_name,added_by,filename) values(%s,%s,%s)',[photo_name,session.get('email'),filename])
            mydb.commit()
            cursor.close()
            return redirect(url_for('photos'))
    return render_template('addphoto.html')
@app.route('/viewphotos',methods=['GET','POST'])
def viewphotos():
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select filename from photos where added_by=%s',[session.get('email')])
    image_data=cursor.fetchall()
    cursor.close()
    print("The data is",image_data)
    
    return render_template('viewphotos.html',image_data=image_data)
@app.route('/deletephoto/<filename>',methods=['GET','POST'])
def deletephoto(filename):
    if not session.get('email'):
        return redirect(url_for('login'))
    else:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('delete from photos where filename=%s and added_by=%s',[filename,session.get('email')])
        mydb.commit()
        cursor.close()
        return redirect(url_for('viewphotos'))
@app.route('/download/<filename>')
def download(filename):
    if not session.get('email'):
        return redirect(url_for('login'))

    cursor = mydb.cursor(buffered=True)
    cursor.execute('SELECT filename FROM photos WHERE added_by = %s', [session.get('email')])
    result = cursor.fetchone()

        # Construct the path to the static folder where the file is stored
    path = os.path.dirname(os.path.abspath(__file__))
    static_path = os.path.join(path, 'static', filename)

    if os.path.exists(static_path):
        return send_file(static_path, download_name=filename, as_attachment=True)
    else:
        return "File not found", 404
@app.route('/updateprofile',methods=['GET','POST'])
def updateprofile():
    if not session.get('email'):
        return redirect(url_for('login'))
    else:
        if request.method=='POST':
            name=request.form['name']
            email=request.form['email']
            password=request.form['password']
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select name,email,password from users where email=%s',[session.get('email')])
            data=cursor.fetchone()
            dbpassword=data[2]
            
            if email=='':
                email=session.get('email')
            else:
                cursor.execute('update users set name=%s,email=%s,password=%s',[name,email,password])
                mydb.commit()
                cursor.close()
                return redirect(url_for('login'))
    return render_template('updateprofile.html')
@app.route('/deleteprofile')
def deleteprofile():
    if not session.get('email'):
        return redirect(url_for('login'))
    else:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('delete from photos where added_by=%s',[session.get('email')])
        cursor.execute('delete from users where email=%s',[session.get('email')])
        mydb.commit()
        cursor.close()
        return redirect(url_for('signin'))
@app.route('/logout')
def logout():
    if not session.get('email'):
        return redirect(url_for('login'))
    else:
        session.pop('email')
        return redirect(url_for('login'))
app.run(debug=True,use_reloader=True)