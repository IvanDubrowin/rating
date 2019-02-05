from flask import render_template, redirect, session, url_for, request, g, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from main_app import app, db
from .models import User, CS, Rating, ArchiveCS
from .forms import LoginForm, RegistrationForm, AddCSForm, CreateRatingForm

@app.route('/')
def index():
    if g.user is None or not g.user.is_authenticated:
        return redirect('login')
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
    return render_template("login.html", form = form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.create(username=form.username.data,
                           password=form.password.data)
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/employees', methods=['GET', 'POST'])
@login_required
def employees():
    page = request.args.get('page', 1, type=int)
    query = CS.query.filter_by(
                        user_id=current_user.get_id()).\
                        paginate(page=page, per_page=10)
    return render_template('employees.html', items=query)

@app.route('/employees/add_cs', methods=['GET', 'POST'])
@login_required
def add_cs():
    form = AddCSForm()
    if form.validate_on_submit():
        user = CS.create(first_name=form.first_name.data,
                         last_name=form.last_name.data,
                         middle_name=form.middle_name.data,
                         pos_plan=form.pos_plan.data,
                         pos_fact=form.pos_fact.data,
                         nps_plan=form.nps_plan.data,
                         nps_fact=form.nps_fact.data,
                         refund_fz=form.refund_fz.data,
                         fz_plan=form.fz_plan.data,
                         fz_fact=form.fz_fact.data,
                         sms_plan=form.sms_plan.data,
                         sms_fact=form.sms_fact.data,
                         kr_plan=form.kr_plan.data,
                         kr_fact=form.kr_fact.data,
                         box_plan=form.box_plan.data,
                         box_fact=form.box_fact.data,
                         ops_plan=form.ops_plan.data,
                         ops_fact=form.ops_fact.data,
                         user_id=current_user.get_id(),
                         )
        return redirect(url_for('employees'))
    return render_template('add_cs.html', form=form)

@app.route('/employees/edit_cs/<id>', methods=['GET', 'POST'])
@login_required
def edit_cs(id):
    form = AddCSForm()
    cs = CS.query.filter_by(id=id, user_id=current_user.get_id()).first()
    if cs is not None:
        if form.validate_on_submit():
            cs.update(first_name=form.first_name.data,
                      last_name=form.last_name.data,
                      middle_name=form.middle_name.data,
                      pos_plan=form.pos_plan.data,
                      pos_fact=form.pos_fact.data,
                      nps_plan=form.nps_plan.data,
                      nps_fact=form.nps_fact.data,
                      refund_fz=form.refund_fz.data,
                      fz_plan=form.fz_plan.data,
                      fz_fact=form.fz_fact.data,
                      sms_plan=form.sms_plan.data,
                      sms_fact=form.sms_fact.data,
                      kr_plan=form.kr_plan.data,
                      kr_fact=form.kr_fact.data,
                      box_plan=form.box_plan.data,
                      box_fact=form.box_fact.data,
                      ops_plan=form.ops_plan.data,
                      ops_fact=form.ops_fact.data,)
            return redirect(url_for('employees'))
        return render_template('edit_cs.html', form=form, cs=cs)
    else:
        return redirect(url_for('employees'))

@app.route('/employees/delete_cs', methods=['POST'])
@login_required
def delete_cs():
    id = request.form['cs_id']
    cs = CS.query.get_or_404(id)
    cs.delete()
    return jsonify(status="success")

@app.route('/create_rating', methods=['GET', 'POST'])
@login_required
def create_rating():
    form = CreateRatingForm()
    form.employees_choices.choices =[
        (x.id, x.fio) for x in CS.query.filter_by(user_id=current_user.get_id()).all()
        ]
    if form.validate_on_submit():
        employees = [CS.query.filter_by(id=cs).first() for cs in form.employees_choices.data]
        archive_employees = [ArchiveCS.create(**cs.serialize) for cs in employees]
        rating = Rating.create(
            pos_weight=form.pos_weight.data,
            nps_weight=form.nps_weight.data,
            fz_weight=form.fz_weight.data,
            refund_fz_weight=form.refund_fz_weight.data,
            sms_weight=form.sms_weight.data,
            kr_weight=form.kr_weight.data,
            box_weight=form.box_weight.data,
            ops_weight=form.ops_weight.data,
            user_id=current_user.get_id(),
            employees=archive_employees)
        return redirect(url_for('rating', id=rating.id))
    return render_template('create_rating.html', form=form)

@app.route('/rating/<id>', methods=['GET', 'POST'])
@login_required
def rating(id):
    rating = Rating.query.filter_by(id=id, user_id=current_user.get_id()).first()
    if rating is not None:
        #cs = CS.query.filter_by(rating_id=id).all()
        return render_template('rating.html')
    return redirect(url_for('index'))
