import datetime, locale, sys
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from main_app import db, views, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class CRUDMixin():

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.commit()


class Association(db.Model, CRUDMixin):
    employee = db.Column(db.Integer, db.ForeignKey('archive_employees.id', ondelete='cascade'), primary_key=True)
    rating = db.Column(db.Integer, db.ForeignKey('ratings.id', ondelete='cascade'), primary_key=True)


class User(db.Model, UserMixin, CRUDMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    cs = db.relationship('CS', backref='user', lazy=True, cascade="all,delete")
    rating = db.relationship('Rating', backref='user', lazy=True, cascade="all,delete")

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class CS(db.Model, CRUDMixin):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), unique=False, index=True)
    last_name = db.Column(db.String(100), unique=False, index=True)
    middle_name = db.Column(db.String(100), unique=False, index=True)
    pos_plan = db.Column(db.Integer, nullable=False)
    pos_fact = db.Column(db.Integer, nullable=False)
    nps_plan = db.Column(db.Float, nullable=False)
    nps_fact = db.Column(db.Float, nullable=False)
    refund_fz = db.Column(db.Boolean, nullable=False)
    fz_plan = db.Column(db.Float, nullable=False)
    fz_fact = db.Column(db.Float, nullable=False)
    sms_plan = db.Column(db.Float, nullable=False)
    sms_fact = db.Column(db.Float, nullable=False)
    kr_plan = db.Column(db.Integer, nullable=False)
    kr_fact = db.Column(db.Integer, nullable=False)
    box_plan = db.Column(db.Integer, nullable=False)
    box_fact = db.Column(db.Integer, nullable=False)
    ops_plan = db.Column(db.Integer, nullable=False)
    ops_fact = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)

    def __repr__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    @property
    def fio(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    @property
    def serialize(self):
        return {'first_name': self.first_name, 'last_name': self.last_name,
                'middle_name': self.middle_name, 'pos_plan': self.pos_plan,
                'pos_fact': self.pos_fact, 'nps_plan': self.nps_plan,
                'nps_fact': self.nps_fact, 'refund_fz': self.refund_fz,
                'fz_plan': self.fz_plan, 'fz_fact': self.fz_fact,
                'sms_plan': self.sms_plan, 'sms_fact': self.sms_fact,
                'kr_plan': self.kr_plan, 'kr_fact': self.kr_fact,
                'box_plan': self.box_plan, 'box_fact': self.box_fact,
                'ops_plan': self.ops_plan, 'ops_fact': self.ops_fact,
                'user_id': self.user_id}

    def pretty_format(self, num):
        locale.setlocale(locale.LC_ALL, '')
        locale._override_localeconv = {'mon_thousands_sep': ' '}
        return locale.format('%.0f', num, grouping=True)


class ArchiveCS(db.Model, CRUDMixin):
    __tablename__ = 'archive_employees'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), unique=False, index=True)
    last_name = db.Column(db.String(100), unique=False, index=True)
    middle_name = db.Column(db.String(100), unique=False, index=True)
    pos_plan = db.Column(db.Integer, nullable=False)
    pos_fact = db.Column(db.Integer, nullable=False)
    nps_plan = db.Column(db.Float, nullable=False)
    nps_fact = db.Column(db.Float, nullable=False)
    refund_fz = db.Column(db.Boolean, nullable=False)
    fz_plan = db.Column(db.Float, nullable=False)
    fz_fact = db.Column(db.Float, nullable=False)
    sms_plan = db.Column(db.Float, nullable=False)
    sms_fact = db.Column(db.Float, nullable=False)
    kr_plan = db.Column(db.Integer, nullable=False)
    kr_fact = db.Column(db.Integer, nullable=False)
    box_plan = db.Column(db.Integer, nullable=False)
    box_fact = db.Column(db.Integer, nullable=False)
    ops_plan = db.Column(db.Integer, nullable=False)
    ops_fact = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)
    rating_id = db.relationship('Rating', secondary='association', back_populates='employees', cascade="all,delete")

    @property
    def pos_ratio(self):
        if self.pos_plan == 0:
            return 100
        else:
            return round(100 *self.pos_fact/self.pos_plan, 2)

    @property
    def nps_ratio(self):
        if self.nps_plan == 0:
            return 100
        else:
            return round(100 *self.nps_fact/self.nps_plan, 2)

    @property
    def refund_fz_ratio(self):
        if self.refund_fz is False:
            return 100
        else:
            return 0

    @property
    def fz_ratio(self):
        if self.fz_plan == 0:
            return 100
        else:
            return round(100 *self.fz_fact/self.fz_plan, 2)

    @property
    def sms_ratio(self):
        if self.sms_plan == 0:
            return 100
        else:
            return round(100 *self.sms_fact/self.sms_plan, 2)

    @property
    def kr_ratio(self):
        if self.kr_plan == 0:
            return 100
        else:
            return round(100 *self.kr_fact/self.kr_plan, 2)

    @property
    def box_ratio(self):
        if self.box_plan == 0:
            return 100
        else:
            return round(100 *self.box_fact/self.box_plan, 2)

    @property
    def ops_ratio(self):
        if self.ops_plan == 0:
            return 100
        else:
            return round(100 *self.ops_fact/self.ops_plan, 2)

    @property
    def fio(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    def __repr__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    def pretty_format(self, num):
        locale.setlocale(locale.LC_ALL, '')
        locale._override_localeconv = {'mon_thousands_sep': ' '}
        return locale.format('%.0f', num, grouping=True)

    def total_ratio(self, **kwargs):
        pos_weight = kwargs.get('pos_weight')
        nps_weight = kwargs.get('nps_weight')
        fz_weight = kwargs.get('fz_weight')
        refund_fz_weight = kwargs.get('refund_fz_weight')
        sms_weight = kwargs.get('sms_weight')
        kr_weight = kwargs.get('kr_weight')
        box_weight = kwargs.get('box_weight')
        ops_weight = kwargs.get('ops_weight')

        ratio = self.pos_ratio*pos_weight+self.nps_ratio*nps_weight+\
                self.fz_ratio*fz_weight+self.refund_fz_ratio*refund_fz_weight+\
                self.sms_ratio*sms_weight+self.kr_ratio*kr_weight+\
                self.box_ratio*box_weight+self.ops_ratio*ops_weight
        ratio = round(ratio/100, 2)
        return ratio


class Rating(db.Model, CRUDMixin):
    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)
    pos_weight = db.Column(db.Integer, nullable=False)
    nps_weight = db.Column(db.Integer, nullable=False)
    fz_weight = db.Column(db.Integer, nullable=False)
    refund_fz_weight = db.Column(db.Integer, nullable=False)
    sms_weight = db.Column(db.Integer, nullable=False)
    kr_weight = db.Column(db.Integer, nullable=False)
    box_weight = db.Column(db.Integer, nullable=False)
    ops_weight = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)
    employees = db.relationship('ArchiveCS', secondary='association', back_populates='rating_id', cascade="all,delete")

    def __repr__(self):
        return f'Рейтинг от {self.date}'

    @property
    def weight_serialize(self):
        return {
            'pos_weight': self.pos_weight, 'nps_weight': self.nps_weight,
            'fz_weight': self.fz_weight, 'refund_fz_weight': self.refund_fz_weight,
            'sms_weight': self.sms_weight, 'kr_weight': self.kr_weight,
            'box_weight': self.box_weight, 'ops_weight': self.ops_weight
        }

    @property
    def format_date_(self):
        if sys.platform == 'win32':
            locale.setlocale(locale.LC_ALL, 'rus_rus')
        else:
            locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

        format_ = datetime.datetime.strftime(self.date, '%d %B %Y')

        return format_
