import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField, FloatField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Optional

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_super_secret_key_baby_shower'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baby_shower.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    guess = db.relationship('Guess', backref='user', uselist=False)

class BabyInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    due_date = db.Column(db.Date, nullable=True)
    sex = db.Column(db.String(50), nullable=True)

class Clue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(150), nullable=False)
    value = db.Column(db.String(255), nullable=False)
    relation_link = db.Column(db.String(100), nullable=True) # e.g. Parents, Grands-parents
    relative_name = db.Column(db.String(150), nullable=True) # e.g. Maman, Soeur du père

class Guess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    sex = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    height = db.Column(db.Float, nullable=False) # cm
    weight = db.Column(db.Float, nullable=False) # kg
    skin_color = db.Column(db.String(100), nullable=True)
    eye_color = db.Column(db.String(100), nullable=True)
    hair_color = db.Column(db.String(100), nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Forms
class RegistrationForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('S\'inscrire')

class LoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')

class GuessForm(FlaskForm):
    dob = DateField('Date de naissance (estimée)', format='%Y-%m-%d', validators=[DataRequired()])
    sex = SelectField('Sexe', choices=[('Fille', 'Fille'), ('Garçon', 'Garçon'), ('Surprise', 'Surprise')], validators=[DataRequired()])
    first_name = StringField('Prénom', validators=[DataRequired()])
    height = FloatField('Taille (cm)', validators=[DataRequired()])
    weight = FloatField('Poids (kg)', validators=[DataRequired()])
    skin_color = SelectField('Couleur de peau (optionnel)', choices=[('', '---'), ('Blanche', 'Blanche'), ('Mate', 'Mate'), ('Noire', 'Noire'), ('Métissée', 'Métissée'), ('Autre', 'Autre')], validators=[Optional()])
    eye_color = SelectField('Couleur des yeux (optionnel)', choices=[('', '---'), ('Marrons', 'Marrons'), ('Bleus', 'Bleus'), ('Verts', 'Verts'), ('Noisette', 'Noisette'), ('Gris', 'Gris'), ('Autre', 'Autre')], validators=[Optional()])
    hair_color = SelectField('Couleur des cheveux (optionnel)', choices=[('', '---'), ('Bruns', 'Bruns'), ('Châtains', 'Châtains'), ('Blonds', 'Blonds'), ('Roux', 'Roux'), ('Noirs', 'Noirs'), ('Chauve', 'Chauve (sans cheveux)'), ('Autre', 'Autre')], validators=[Optional()])
    submit = SubmitField('Enregistrer le pronostic')

class ClueForm(FlaskForm):
    theme = StringField('Thème (ex: Prénom, Couleur des yeux, ...)', validators=[DataRequired()])
    value = StringField('Valeur', validators=[DataRequired()])
    relation_link = SelectField('Lien de parenté', choices=[('', '---'), ('Parents', 'Parents'), ('Grands-parents', 'Grands-parents'), ('Oncles/Tantes', 'Oncles/Tantes'), ('Cousins', 'Cousins'), ('Autre', 'Autre')], validators=[Optional()])
    relative_name = StringField('Parent associé (ex: Maman, Sœur du père)', validators=[Optional()])
    submit_clue = SubmitField('Ajouter l\'indice')

class DueDateForm(FlaskForm):
    due_date = DateField('Terme prévu', format='%Y-%m-%d', validators=[Optional()])
    sex = SelectField('Sexe du bébé', choices=[('', '---'), ('Fille', 'Fille'), ('Garçon', 'Garçon')], validators=[Optional()])
    submit_date = SubmitField('Mettre à jour les informations')

# Routes
@app.route('/')
def index():
    guesses = Guess.query.all()
    return render_template('index.html', guesses=guesses)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Ce nom d\'utilisateur est déjà pris.', 'danger')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        is_admin = (form.username.data.lower() == 'admin')
        new_user = User(username=form.username.data, password_hash=hashed_password, is_admin=is_admin)
        db.session.add(new_user)
        db.session.commit()
        flash('Votre compte a été créé ! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Connexion réussie.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Échec de la connexion. Veuillez vérifier votre nom d\'utilisateur et votre mot de passe.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/info')
def info():
    baby_info = BabyInfo.query.first()
    clues = Clue.query.order_by(Clue.theme).all()
    # Group clues by theme
    clues_by_theme = {}
    for clue in clues:
        if clue.theme not in clues_by_theme:
            clues_by_theme[clue.theme] = []
        clues_by_theme[clue.theme].append(clue)
    return render_template('info.html', clues_by_theme=clues_by_theme, baby_info=baby_info)

@app.route('/admin/info', methods=['GET', 'POST'])
@login_required
def admin_info():
    if not current_user.is_admin:
        flash('Accès non autorisé.', 'danger')
        return redirect(url_for('index'))
    
    themes_query = db.session.query(Clue.theme).distinct().all()
    themes = [t[0] for t in themes_query]

    clues = Clue.query.all()
    baby_info = BabyInfo.query.first()
    if not baby_info:
        baby_info = BabyInfo()
        db.session.add(baby_info)
        db.session.commit()

    clue_form = ClueForm()
    date_form = DueDateForm()
    
    if clue_form.submit_clue.data and clue_form.validate_on_submit():
        new_clue = Clue(
            theme=clue_form.theme.data,
            value=clue_form.value.data,
            relation_link=clue_form.relation_link.data,
            relative_name=clue_form.relative_name.data
        )
        db.session.add(new_clue)
        db.session.commit()
        flash('Indice ajouté avec succès.', 'success')
        return redirect(url_for('admin_info'))
        
    if date_form.submit_date.data and date_form.validate_on_submit():
        baby_info.due_date = date_form.due_date.data
        baby_info.sex = date_form.sex.data
        db.session.commit()
        flash('Les informations ont été mises à jour.', 'success')
        return redirect(url_for('admin_info'))

    # Populate date_form
    if request.method == 'GET':
        date_form.due_date.data = baby_info.due_date
        date_form.sex.data = baby_info.sex
        
    return render_template('admin_info.html', form=clue_form, date_form=date_form, clues=clues, themes=themes)

@app.route('/admin/info/delete/<int:clue_id>', methods=['POST'])
@login_required
def delete_clue(clue_id):
    if not current_user.is_admin:
        flash('Accès non autorisé.', 'danger')
        return redirect(url_for('index'))
    
    clue = Clue.query.get_or_404(clue_id)
    db.session.delete(clue)
    db.session.commit()
    flash('Indice supprimé.', 'success')
    return redirect(url_for('admin_info'))

@app.route('/guess', methods=['GET', 'POST'])
@login_required
def guess():
    form = GuessForm()
    existing_guess = Guess.query.filter_by(user_id=current_user.id).first()
    
    if form.validate_on_submit():
        if existing_guess:
            # Update existing
            existing_guess.dob = form.dob.data
            existing_guess.sex = form.sex.data
            existing_guess.first_name = form.first_name.data
            existing_guess.height = form.height.data
            existing_guess.weight = form.weight.data
            existing_guess.skin_color = form.skin_color.data
            existing_guess.eye_color = form.eye_color.data
            existing_guess.hair_color = form.hair_color.data
            flash('Votre pronostic a été mis à jour !', 'success')
        else:
            # Create new
            new_guess = Guess(
                user_id=current_user.id,
                dob=form.dob.data,
                sex=form.sex.data,
                first_name=form.first_name.data,
                height=form.height.data,
                weight=form.weight.data,
                skin_color=form.skin_color.data,
                eye_color=form.eye_color.data,
                hair_color=form.hair_color.data
            )
            db.session.add(new_guess)
            flash('Votre pronostic a été enregistré !', 'success')
        
        db.session.commit()
        return redirect(url_for('index'))
    
    elif request.method == 'GET' and existing_guess:
        # Populate form with existing data
        form.dob.data = existing_guess.dob
        form.sex.data = existing_guess.sex
        form.first_name.data = existing_guess.first_name
        form.height.data = existing_guess.height
        form.weight.data = existing_guess.weight
        form.skin_color.data = existing_guess.skin_color
        form.eye_color.data = existing_guess.eye_color
        form.hair_color.data = existing_guess.hair_color
        
    # Get hints
    baby_info = BabyInfo.query.first()
    prenom_clues = Clue.query.filter_by(theme='Prénom').all()
        
    return render_template('guess_form.html', form=form, existing=bool(existing_guess), baby_info=baby_info, prenom_clues=prenom_clues)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
