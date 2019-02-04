from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, BooleanField, IntegerField, FloatField, SelectMultipleField
from wtforms.compat import string_types
from wtforms.validators import Email, Required, Length, Regexp, EqualTo, NumberRange, InputRequired, StopValidation
from wtforms import ValidationError
from wtforms.fields.html5 import IntegerRangeField
from .models import User
from main_app import db

class CorrectRequired(Required):
    def __call__(self, form, field):
        if field.data is None or isinstance(field.data, string_types) and not field.data.strip():
            if self.message is None:
                message = field.gettext('')
            else:
                message = self.message
            field.errors[:] = []
            raise StopValidation(message)


class LoginForm(FlaskForm):
    username = StringField('логин', validators=[Required()], render_kw={"class": "validate"})
    password = PasswordField('пароль', validators=[Required()], render_kw={"class": "validate"})
    submit = SubmitField('Вход', render_kw={"class": "btn waves-effect waves-light btn-large auth-button"})
    remember_me = BooleanField('Не выходить из системы')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(
            username=self.username.data).first()
        if user is None:
            self.username.errors.append('Неверный логин')
            return False

        if not user.verify_password(self.password.data):
            self.password.errors.append('Неверный пароль')
            return False

        self.user = user
        return True


class RegistrationForm(FlaskForm):
    username = StringField('логин',
                            validators=[Required(),
                            Length(1, 64),
                            Regexp('^[A-Za-z][A-Za-z0-9_.]*$',
                            0, 'логин должен состоять только из букв')],
                            render_kw={"class": "validate"})
    password = PasswordField('пароль', validators=[Required(),
                            EqualTo('password2',
                            message='Пароли должны совпадать.')],
                            render_kw={"class": "validate"})
    password2 = PasswordField('подтвердите пароль',
                              validators=[Required()],
                              render_kw={"class": "validate"})
    submit = SubmitField('Регистрация', render_kw={"class": "btn waves-effect waves-light btn-large auth-button"})

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Такой пользователь уже существует')


class AddCSForm(FlaskForm):
    first_name = StringField('Имя',validators=[InputRequired(' '),
                             Length(1, 100)],
                             render_kw={"class": "validate"})
    last_name = StringField('Фамилия',validators=[InputRequired(''),
                             Length(1, 100)],
                             render_kw={"class": "validate"})
    middle_name = StringField('Отчество',validators=[InputRequired(''),
                             Length(1, 100)],
                             render_kw={"class": "validate"})
    pos_plan = IntegerField('POS план',validators=[CorrectRequired(),
                             NumberRange(min=0, message='Вы ввели некорректное значение')],
                             render_kw={"class": "validate"})
    pos_fact = IntegerField('POS факт',validators=[CorrectRequired(),
                             NumberRange(min=0, message='Вы ввели некорректное значение')],
                             render_kw={"class": "validate"})
    nps_plan = FloatField('NPS план',validators=[CorrectRequired(),
                             NumberRange(min=0.00, message='Вы ввели некорректное значение')],
                             render_kw={"class": "validate"})
    nps_fact = FloatField('NPS факт',validators=[CorrectRequired(),
                             NumberRange(min=0, message='Вы ввели некорректное значение')],
                             render_kw={"class": "validate"})
    refund_fz = BooleanField()
    fz_plan = FloatField('ФЗ план',validators=[CorrectRequired(),
                             NumberRange(min=0.00, message='Вы ввели некорректное значение')],
                             render_kw={"class": "validate"})
    fz_fact = FloatField('ФЗ факт',validators=[CorrectRequired(),
                             NumberRange(min=0, message='Вы ввели некорректное значение')],
                             render_kw={"class": "validate"})
    sms_plan = FloatField('SMS план',validators=[CorrectRequired(),
                             NumberRange(min=0.00, message='Вы ввели некорректное значение')],
                             render_kw={"class": "validate"})
    sms_fact = FloatField('SMS факт',validators=[CorrectRequired(),
                             NumberRange(min=0, message='Вы ввели некорректное значение')],
                             render_kw={"class": "validate"})
    kr_plan = IntegerField('Карта Свобода план',validators=[CorrectRequired(),
                             NumberRange(min=0, message='Вы ввели некорректное значение')],
                             render_kw={"class": "validate"})
    kr_fact = IntegerField('Карта Свобода факт',validators=[CorrectRequired(),
                             NumberRange(min=0, message='Вы ввели некорректное значение')],
                             render_kw={"class": "validate"})
    box_plan = IntegerField('BOX план',validators=[CorrectRequired(),
                             NumberRange(min=0, message='Вы ввели некорректное значение')],
                             render_kw={"class": "validate"})
    box_fact = IntegerField('BOX факт',validators=[CorrectRequired(),
                             NumberRange(message='Вы ввели некорректное значение')],
                             render_kw={"class": "validate"})
    ops_plan = IntegerField('ОПС план',validators=[CorrectRequired(),
                             NumberRange(min=0, message='Вы ввели некорректное значение')],
                             render_kw={"class": "validate"})
    ops_fact = IntegerField('ОПС факт',validators=[CorrectRequired(),
                             NumberRange(min=0, message='Вы ввели некорректное значение')],
                             render_kw={"class": "validate"})
    submit = SubmitField('Добавить КС', render_kw={"class": "btn waves-effect waves-light btn-large add-button"})

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        fields = [
            self.pos_plan,
            self.pos_fact,
            self.nps_plan,
            self.nps_fact,
            self.fz_plan,
            self.fz_fact,
            self.sms_plan,
            self.sms_fact,
            self.kr_plan,
            self.kr_fact,
            self.box_plan,
            self.ops_plan,
            self.ops_fact,
        ]

        for field in fields:
            if not isinstance(field.data, (int, float)):
                field.errors.append('Вы ввели некорректное значение')
                return False
        return True


class CreateRatingForm(FlaskForm):
    employees_choices = SelectMultipleField('Выбор КС', choices=[], coerce=int)
    pos_weight = IntegerRangeField('Вес POS', default=35, render_kw={"min": 0, "max": 100})
    nps_weight = IntegerRangeField('Вес NPS', default=9, render_kw={"min": 0, "max": 100})
    fz_weight = IntegerRangeField('Вес ФЗ', default=15, render_kw={"min": 0, "max": 100})
    refund_fz_weight = IntegerRangeField('Вес Возврат ФЗ', default=9, render_kw={"min": 0, "max": 100})
    sms_weight = IntegerRangeField('Вес SMS', default=5, render_kw={"min": 0, "max": 100})
    kr_weight = IntegerRangeField('Вес Карта Свобода', default=9, render_kw={"min": 0, "max": 100})
    box_weight = IntegerRangeField('Вес BOX', default=9, render_kw={"min": 0, "max": 100})
    ops_weight = IntegerRangeField('Вес ОПС', default=9, render_kw={"min": 0, "max": 100})
    submit = SubmitField('Создать рейтинг', render_kw={"class": "btn waves-effect waves-light btn-large add-button"})

    def validate(self):
        rv = FlaskForm.validate(self)

        if not self.employees_choices.data:
            self.employees_choices.errors.append('Необходимо добавить КС')
            return False
        return True
