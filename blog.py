from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,SelectField,PasswordField,validators
import email_validator
from passlib.hash import sha256_crypt
from functools import wraps


app = Flask(__name__)

app.secret_key= "ybblog"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "ybblog"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

#Kullanıcı Giriş Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı görüntülemek için lütfen giriş yapınız.","danger")
            return redirect(url_for("login"))
    return decorated_function

#Kullanıcı Kayıt Formu
class RegisterForm(Form):
    name = StringField("İsim",validators=[validators.length(min=4,max=24)])
    surname = StringField("Soyad",validators=[validators.length(min=4,max=24)])
    username = StringField("Kullanıcı Adı",validators=[validators.length(min=5,max=35)])
    email = StringField("Email Adresi",validators=[validators.Email(message = "Lütfen Geçerli Bir Email Adresi Girin")])
    phone_number = StringField("Telefon Numarası")
    city = SelectField("İl Seçiniz",choices=[("Aydın")])
    district = SelectField("İlçe Seçiniz",choices=[("Bozdoğan"),("Buharkent"),("Çine"),("Didim"),("Efeler"),("Germencik"),("İncirliova"),("Karacasu"),("Karpuzlu"),("Koçarlı"),("Köşk"),("Kuşadası"),("Kuyucak"),("Nazilli"),("Söke"),("Sultanhisar"),("Yenipazar")])
    street = StringField("Mahalle")
    address = TextAreaField("Açık Adres")
    password = PasswordField("Parola:",validators=[
        validators.DataRequired(message = "Lütfen Bir Parola Belirleyin"),
        validators.EqualTo(fieldname = "confirm",message="Parolanız Uyuşmuyor..")
    ])
    confirm = PasswordField("Parola Doğrula")

#Login Formu
class LoginForm(Form):
    username = StringField("Kullanıcı Adı")
    password = PasswordField("Parola")

mysql = MySQL(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/dashboard")
@login_required
def dashboard():
    cursor = mysql.connection.cursor()
    sorgu = "SELECT * FROM masters WHERE username = %s"
    result = cursor.execute(sorgu,{session["username"],})

    cursor2 = mysql.connection.cursor()
    sorgu2 = "SELECT * FROM users WHERE username IN (SELECT username FROM booking WHERE owner_id IN(SELECT id FROM masters WHERE username = %s))"
    result2 = cursor2.execute(sorgu2,{session["username"],})

    cursor3 = mysql.connection.cursor()
    sorgu3 = "SELECT * FROM masters WHERE id IN(SELECT owner_id FROM booking WHERE username=%s)"
    result3 = cursor3.execute(sorgu3,{session["username"],})

    cursor4 = mysql.connection.cursor()
    sorgu4 = "SELECT * FROM booking WHERE owner_id IN(SELECT id FROM masters WHERE username = %s)"
    result4 = cursor4.execute(sorgu4,{session["username"]})

    if result > 0 or result2 > 0 or result3 > 0 or result4 > 0:
        masters = cursor.fetchall()
        bookingOwners = cursor2.fetchall()
        bookingOwners1 = cursor3.fetchall()
        bookingOwners2 = cursor4.fetchall()
        return render_template("dashboard.html",bookingOwners = bookingOwners,masters = masters,bookingOwners1=bookingOwners1,bookingOwners2=bookingOwners2)
    else:
        return render_template("dashboard.html")


#Hizmetler Sayfası
@app.route("/services")
@login_required
def services():
    cursor = mysql.connection.cursor()
    sorgu = "SELECT * FROM masters"
    result = cursor.execute(sorgu)

    if result > 0:
        masters = cursor.fetchall()
        return render_template("services.html",masters = masters)
    else:
        return render_template("services.html")

#Kayıt Olma
@app.route("/register",methods = ["GET","POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        surname = form.surname.data
        username = form.username.data
        email = form.email.data
        phone_number = form.phone_number.data
        city = form.city.data
        district = form.district.data
        street = form.street.data
        address = form.address.data
        password = sha256_crypt.encrypt(form.password.data)

        cursor = mysql.connection.cursor()
        sorgu = "INSERT INTO users(name,surname,email,username,password,phone_number,city,district,street,address) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sorgu,(name,surname,email,username,password,phone_number,city,district,street,address))
        mysql.connection.commit()
        cursor.close()

        flash("Başarıyla Kayıt Oldunuz..","success")

        return redirect(url_for("login"))
    else:
        return render_template("register.html",form = form)
#Login İşlemi
@app.route("/login",methods = ["GET","POST"])
def login():
    form = LoginForm(request.form)

    if request.method == "POST":
        username = form.username.data
        password_entered = form.password.data

        cursor = mysql.connection.cursor()
        sorgu = "SELECT * FROM users WHERE username = %s"
        result = cursor.execute(sorgu,(username,))

        if result > 0:
            data = cursor.fetchone()
            real_password = data["password"]
            if sha256_crypt.verify(password_entered,real_password):
                flash("Başarıyla Giriş Yaptınız...","success")
                session["logged_in"] = True
                session["username"] = username
                return redirect(url_for("index"))
            else:
                flash("Parolanızı Yanlış Girdiniz!","danger")
                return redirect(url_for("login"))
        else:
            flash("Böyle bir kullanıcı bulunmuyor...","danger")
            return redirect(url_for("login"))

    return render_template("login.html",form = form)

#Detay Sayfası ve booking
@app.route("/services/<string:id>",methods=["GET","POST"])
@login_required
def detail(id):
    cursor = mysql.connection.cursor()
    sorgu = "SELECT * FROM masters WHERE id = %s"
    result = cursor.execute(sorgu,(id,))
    form = BookingForm(request.form)

    if result > 0 and request.method == "GET":
        detail = cursor.fetchone()
        return render_template("detail.html",detail=detail,form=form)
    if request.method == "POST":
        day = form.day.data
        month = form.month.data
        year = form.year.data
        problem = form.problem.data
        cursor = mysql.connection.cursor()
        sorgu = "INSERT INTO booking(owner_id,username,year,month,day,problem) VALUES(%s,%s,%s,%s,%s,%s)"
        cursor.execute(sorgu,(id,session["username"],year,month,day,problem))
        mysql.connection.commit()
        cursor.close()

        flash("Randevu başarıyla alındı. En kısa sürede dükkan sahibi tarafından aranacaksınız.","success")
        return redirect(url_for("dashboard"))

#logout İşlemi
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

#İşyeri Silme
@app.route("/delete/<string:id>")
@login_required
def delete(id):
    cursor = mysql.connection.cursor()
    sorgu = "SELECT * FROM masters WHERE id = %s and username = %s"
    result = cursor.execute(sorgu,(id,session["username"]))

    if result > 0:
        sorgu2 = "DELETE FROM masters WHERE id = %s"
        cursor.execute(sorgu2,(id,))
        mysql.connection.commit()
        flash("İşlem başarıyla gerçekleşti.","success")
        return redirect(url_for("dashboard"))
    else:
        flash("Bu işlemi yapma yetkiniz bulunmamaktadır.","danger")
        return redirect(url_for("index"))

#İşyeri Güncelleme
@app.route("/edit/<string:id>", methods= ["GET","POST"])
@login_required
def update(id):
    if request.method == "GET":
        cursor = mysql.connection.cursor()
        sorgu = "SELECT * FROM masters WHERE id = %s and username = %s"
        result = cursor.execute(sorgu,(id,session["username"]))

        if result == 0:
            flash("Bu işlem için yetkiniz bulunmamaktadır.","danger")
            return redirect(url_for("index"))
        else:
            update = cursor.fetchone()
            form = StoreForm()
            form.type.data = update["type"]
            form.store.data = update["store"]
            form.phone_number.data = update["phone_number"]
            form.city.data = update["city"]
            form.district.data = update["district"]
            form.street.data = update["street"]
            form.address.data = update["address"]
            form.name.data = update["name"]
            form.surname.data = update["surname"]
            return render_template("update.html",form = form)
    else:
        form = StoreForm(request.form)
        newType = form.type.data
        newStore = form.store.data
        newPhoneNumber = form.phone_number.data
        newCity = form.city.data
        newDistrict = form.district.data
        newStreet = form.street.data
        newAddress = form.address.data
        newName = form.name.data
        newSurname = form.surname.data

        sorgu2 = "UPDATE masters SET type = %s,store = %s,phone_number = %s,city = %s,district = %s,street = %s,address = %s,name = %s,surname = %s WHERE id = %s"
        cursor = mysql.connection.cursor()
        cursor.execute(sorgu2,(newType,newStore,newPhoneNumber,newCity,newDistrict,newStreet,newAddress,newName,newSurname,id))
        mysql.connection.commit()
        flash("İşlem başarıyla gerçekleşti.","success")
        return redirect(url_for("dashboard"))


#İşyeri Ekleme
@app.route("/addstore", methods= ["GET","POST"])
def addstore():
    form = StoreForm(request.form)
    if request.method == "POST":
        type = form.type.data
        store = form.store.data
        phone_number = form.phone_number.data
        city = form.city.data
        district = form.district.data
        street = form.street.data
        address = form.address.data
        name = form.name.data
        surname = form.surname.data

        cursor = mysql.connection.cursor()
        sorgu = "INSERT INTO masters(type,store,phone_number,city,district,street,address,name,surname,username) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sorgu,(type,store,phone_number,city,district,street,address,name,surname,session["username"]))
        mysql.connection.commit()
        cursor.close()

        flash("İşyeri Başarıyla Eklendi.","success")

        return redirect(url_for("dashboard"))
    return render_template("addstore.html",form = form)

#İşyeri Form
class StoreForm(Form):
    type = SelectField("Tür",choices=[("Tesisatçı"),("Boyacı"),("Elektrikçi"),("Tamirci")])
    store = StringField("İşyeri Adı")
    phone_number = StringField("Telefon Numarası")
    city = SelectField("İl Seçiniz",choices=[("Aydın")])
    district = SelectField("İlçe Seçiniz",choices=[("Bozdoğan"),("Buharkent"),("Çine"),("Didim"),("Efeler"),("Germencik"),("İncirliova"),("Karacasu"),("Karpuzlu"),("Koçarlı"),("Köşk"),("Kuşadası"),("Kuyucak"),("Nazilli"),("Söke"),("Sultanhisar"),("Yenipazar")])
    street = StringField("Mahalle")
    address = TextAreaField("Açık Adres")
    name = StringField("Ad")
    surname = StringField("Soyad")

#Arama URL
@app.route("/search",methods = ["GET","POST"])
def search():
    if request.method == "GET":
        return redirect(url_for("index"))
    else:
        keyword = request.form.get("keyword")

        cursor = mysql.connection.cursor()
        sorgu = "SELECT * FROM masters WHERE type LIKE '%" + keyword +"%' OR city LIKE '%" + keyword +"%' OR district LIKE '%" + keyword +"%' OR street LIKE '%" + keyword +"%'"
        result = cursor.execute(sorgu)

        if result == 0:
            flash("Aranan kelimeye uygun hizmet bulunamadı","warning")
            return redirect(url_for("services"))
        else:
            masters = cursor.fetchall()
            return render_template("services.html",masters=masters)

#Booking Form
class BookingForm(Form):
    day = SelectField("Gün",choices=[("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("10"),("11"),("12"),("13"),("14"),("15"),("16"),("17"),("18"),("19"),("20"),("21"),("22"),("23"),("24"),("25"),("26"),("27"),("28"),("29"),("30"),("31")])
    month = SelectField("Ay",choices=[("Ocak"),("Şubat"),("Mart"),("Nisan"),("Mayıs"),("Haziran"),("Temmuz"),("Ağustos"),("Eylül"),("Ekim"),("Kasım"),("Aralık")])
    year = SelectField("Yıl",choices=[("2022"),("2023")])
    problem = TextAreaField("Problemi Yazınız")

if __name__ == "__main__":
    app.run(debug=True)