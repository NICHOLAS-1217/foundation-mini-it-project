from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User, Admin
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, RemoveItemForm, AdminLoginForm, AdminRegisterForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/swimming')
def swimming_page():
    return render_template('Swimming.html')

@app.route('/yoga')
def yoga_page():
    return render_template('Yoga.html')

@app.route('/gymnastics')
def gymnastics_page():
    return render_template('Gymnastics.html')

@app.route('/gym')
def gym_page():
    return render_template('Gym.html')

@app.route('/dancing')
def dancing_page():
    return render_template('Dancing.html')

@app.route('/ballgames')
def ballgames_page():
    return render_template('Ball_Games.html')

@app.route('/profile')
@login_required
def profile_page():
    return render_template('profile.html')

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

@app.route('/shoppingcart', methods=['GET', 'POST'])
@login_required
def shoppingcart_page():
    purchase_form = PurchaseItemForm()
    removing_form = RemoveItemForm()
    if request.method == "POST":
        #Purchase Item Logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! You purchased {p_item_object.name} for RM{p_item_object.price}", category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!", category='danger')
        #Remove Item Logic
        removed_item = request.form.get('removed_item')
        s_item_object = Item.query.filter_by(name=removed_item).first()
        if s_item_object:
            if current_user.can_remove(s_item_object):
                s_item_object.remove(current_user)
                flash(f"Congratulations! You removed {s_item_object.name} back to market!", category='success')
            else:
                flash(f"Something went wrong with removing {s_item_object.name}", category='danger')

        return redirect(url_for('shoppingcart_page'))

    if request.method == "GET":
        items = Item.query.filter_by()
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('shoppingcart.html', items=items, purchase_form=purchase_form, owned_items=owned_items, removing_form=removing_form)

@app.route('/timetable')
def timetable_page():
    owned_items = Item.query.filter_by(owner=current_user.id)
    return render_template('timetable.html', owned_items=owned_items)

@app.route('/userlist')
def userlist_page():
    user_list = User.query.filter_by()
    return render_template('userlist.html', user_list=user_list)

@app.route('/people')
def people_page():
    user_list = User.query.filter_by()
    return render_template('people.html', user_list=user_list)


@app.route('/courses')
def courses_page():
    item_list = Item.query.filter_by()
    return render_template('courses.html', item_list=item_list)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('shoppingcart_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/adminregister', methods=['GET', 'POST'])
def adminregister_page():
    form = AdminRegisterForm()
    if form.validate_on_submit():
        user_to_create = Admin(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('admin_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('adminregister.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('shoppingcart_page'))

        else:
            flash('Username and password are not match! Please try again', category='danger')
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin_page():
    form = AdminLoginForm()
    if form.validate_on_submit():
        attempted_admin = Admin.query.filter_by(username=form.username.data).first()
        if attempted_admin and attempted_admin.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_admin)
            flash(f'Success! You are logged in as: {attempted_admin.username}', category='success')
            return redirect(url_for('admin_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')
            return render_template('adminlogin.html', form=form)

    return render_template('adminlogin.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))



