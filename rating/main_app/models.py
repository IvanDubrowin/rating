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


class User(db.Model, UserMixin, CRUDMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    cs = db.relationship('CS', backref='user', lazy=True)

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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    @property
    def pos_ratio(self):
        if self.pos_plan == 0:
            return 100
        else:
            return self.pos_fact/self.pos_plan

    @property
    def nps_ratio(self):
        if self.nps_plan == 0:
            return 100
        else:
            return self.nps_fact/self.nps_plan

    @property
    def refund_fz_ratio(self):
        if refund_fz is not False:
            return 100
        else:
            return 0

    @property
    def fz_ratio(self):
        if self.fz_plan == 0:
            return 100
        else:
            return self.fz_fact/self.fz_plan

    @property
    def sms_ratio(self):
        if self.sms_plan == 0:
            return 100
        else:
            return self.sms_fact/self.sms_plan

    @property
    def kr_ratio(self):
        if self.kr_plan == 0:
            return 100
        else:
            return self.kr_fact/self.kr_plan

    @property
    def box_ratio(self):
        if self.box_plan == 0:
            return 100
        else:
            return self.box_fact/self.box_plan

    @property
    def ops_ratio(self):
        if self.ops_plan == 0:
            return 100
        else:
            return self.ops_fact/self.ops_plan

    @property
    def fio(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'
