import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user

# ------------------------------------------------------------------------------
# 1) Flask + SQLAlchemy + LoginManager + Admin Konfigürasyonu
# ------------------------------------------------------------------------------
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Burada daha önceden kullandığınız veri tabanı bağlantısını aynen bırakın.
# Örnek: SQLite kullanıyorsanız:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'config.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super-secret-key'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ------------------------------------------------------------------------------
# 2) Modeller: Cookie ve CronSetting (önceden eklediğiniz satırlar)
# ------------------------------------------------------------------------------
class Cookie(db.Model):
    __tablename__ = 'cookie'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    value = db.Column(db.Text, nullable=False)
    domain = db.Column(db.String(255), nullable=False)
    path = db.Column(db.String(255), nullable=False, default='/')
    http_only = db.Column(db.Boolean, nullable=False, default=False)
    secure = db.Column(db.Boolean, nullable=False, default=False)
    same_site = db.Column(db.String(20), nullable=False, default='None')  # “None”, “Lax” veya “Strict”
    expires = db.Column(db.Integer, nullable=True)  # UNIX timestamp olarak saklanabilir
    session = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Cookie {self.name} | {self.domain}>'

class CronSetting(db.Model):
    __tablename__ = 'cron_setting'
    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(255), nullable=False, unique=True)
    cron_expression = db.Column(db.String(100), nullable=False)  # Örnek: "0 0 * * *"
    enabled = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f'<CronSetting {self.job_name} | {self.cron_expression} | Enabled={self.enabled}>'

# ------------------------------------------------------------------------------
# 3) Basit Admin Kullanıcısı (örnek) ve SecureModelView
# ------------------------------------------------------------------------------
class AdminUser(UserMixin):
    id = 1
    username = 'admin'
    is_admin = True

@login_manager.user_loader
def load_user(user_id):
    if int(user_id) == 1:
        return AdminUser()
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'password':
            user = AdminUser()
            login_user(user)
            return redirect(request.args.get('next') or url_for('admin.index'))
        flash('Geçersiz kullanıcı adı veya şifre.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

class SecureModelView(ModelView):
    def is_accessible(self):
        try:
            return current_user.is_authenticated and current_user.is_admin
        except:
            return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

# ------------------------------------------------------------------------------
# 4) Admin Panelini Oluştur ve Modelleri Kaydet
# ------------------------------------------------------------------------------
admin = Admin(app, name='Control Panel', template_mode='bootstrap3')
admin.add_view(SecureModelView(Cookie, db.session, category='Ayarlar'))
admin.add_view(SecureModelView(CronSetting, db.session, category='Ayarlar'))

# ------------------------------------------------------------------------------
# 5) “Ham JSON Olarak Çerez Yapıştırma” İçin Özel View
# ------------------------------------------------------------------------------
class CookieImportView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        # Giriş kontrolü
        if not (current_user.is_authenticated and current_user.is_admin):
            return redirect(url_for('login', next=request.url))

        if request.method == 'POST':
            raw_json = request.form.get('cookie_json', '').strip()
            if not raw_json:
                flash('Lütfen JSON içeriği yapıştırın.', 'warning')
                return redirect(url_for('cookieimport.index'))

            try:
                parsed_list = json.loads(raw_json)
                if not isinstance(parsed_list, list):
                    raise ValueError('Yapıştırdığınız içerik bir liste değil.')

                # Mevcut Cookie kayıtlarını tamamen silip yenilerini eklemek isterseniz:
                # Cookie.query.delete()
                # db.session.commit()

                for item in parsed_list:
                    # Zorunlu alanlar kontrolü
                    name = item.get('name')
                    value = item.get('value', '')
                    domain = item.get('domain')
                    path = item.get('path', '/')
                    http_only = item.get('httpOnly', False)
                    secure = item.get('secure', False)
                    same_site_raw = item.get('sameSite', '')
                    session_flag = item.get('session', False)
                    expires_raw = item.get('expirationDate', None)

                    # sameSite dönüştürme: “no_restriction” veya “unspecified” → “None”
                    same_site = 'None'
                    if same_site_raw.lower() in ('no_restriction', 'unspecified'):
                        same_site = 'None'
                    elif same_site_raw.lower() == 'lax':
                        same_site = 'Lax'
                    elif same_site_raw.lower() == 'strict':
                        same_site = 'Strict'

                    expires = None
                    if not session_flag and expires_raw is not None:
                        try:
                            expires = int(expires_raw)
                        except:
                            expires = None

                    # Burada, eğer isim+domain ikilisiyle kayıt varsa güncelle, yoksa yeni ekle:
                    existing = Cookie.query.filter_by(name=name, domain=domain).first()
                    if existing:
                        existing.value = value
                        existing.path = path
                        existing.http_only = http_only
                        existing.secure = secure
                        existing.same_site = same_site
                        existing.expires = expires
                        existing.session = session_flag
                    else:
                        new_cookie = Cookie(
                            name=name,
                            value=value,
                            domain=domain,
                            path=path,
                            http_only=http_only,
                            secure=secure,
                            same_site=same_site,
                            expires=expires,
                            session=session_flag
                        )
                        db.session.add(new_cookie)

                db.session.commit()
                flash(f'{len(parsed_list)} adet çerez başarıyla aktarıldı.', 'success')
                return redirect(url_for('cookieimport.index'))

            except Exception as e:
                db.session.rollback()
                flash(f'Import hatası: {str(e)}', 'danger')
                return redirect(url_for('cookieimport.index'))

        # GET isteğinde sadece form göster
        return self.render('import_cookies.html')

    def is_accessible(self):
        try:
            return current_user.is_authenticated and current_user.is_admin
        except:
            return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

# Admin paneline bu view'i ekleyelim. endpoint='cookieimport'
admin.add_view(CookieImportView(name='Import Cookies', endpoint='cookieimport'))

# ------------------------------------------------------------------------------
# 6) Uygulamayı Çalıştır ve Tablo Oluştur
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
