import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField, FloatField, TextAreaField, BooleanField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Optional

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'my_super_secret_key_baby_shower')

database_url = os.environ.get('DATABASE_URL', 'sqlite:///baby_shower.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
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
    category = db.Column(db.String(50), nullable=True)
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

class ScoringRule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    base_points = db.Column(db.Integer, nullable=False)
    decrement_per_rank = db.Column(db.Integer, nullable=False)
    exact_bonus = db.Column(db.Integer, default=0, nullable=False)

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

class FormConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    show_dob = db.Column(db.Boolean, default=True)
    show_sex = db.Column(db.Boolean, default=True)
    show_first_name = db.Column(db.Boolean, default=True)
    show_height = db.Column(db.Boolean, default=True)
    show_weight = db.Column(db.Boolean, default=True)
    show_skin_color = db.Column(db.Boolean, default=True)
    show_eye_color = db.Column(db.Boolean, default=True)
    show_hair_color = db.Column(db.Boolean, default=True)
    show_hints = db.Column(db.Boolean, default=True)
    
    lock_sex = db.Column(db.Boolean, default=False)
    anonymous_mode = db.Column(db.Boolean, default=False)
    show_category = db.Column(db.Boolean, default=True)
    
    prize_text = db.Column(db.Text, nullable=True)
    rules_text = db.Column(db.Text, nullable=True)
    
    # Table visibility toggles
    table_show_dob = db.Column(db.Boolean, default=True)
    table_show_sex = db.Column(db.Boolean, default=True)
    table_show_first_name = db.Column(db.Boolean, default=True)
    table_show_height = db.Column(db.Boolean, default=True)
    table_show_weight = db.Column(db.Boolean, default=True)
    table_show_skin_color = db.Column(db.Boolean, default=True)
    table_show_eye_color = db.Column(db.Boolean, default=True)
    table_show_hair_color = db.Column(db.Boolean, default=True)
    
    # Page access toggles
    enable_stats_page = db.Column(db.Boolean, default=True)
    enable_table_page = db.Column(db.Boolean, default=True)
    
    # Home page config
    welcome_message = db.Column(db.Text, nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Forms
class RegistrationForm(FlaskForm):
    first_name = StringField('Prénom', validators=[DataRequired()])
    last_name = StringField('Nom', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[DataRequired(), EqualTo('password')])
    category = SelectField('Catégorie', choices=[('Amis', 'Amis'), ('Collègues', 'Collègues'), ('Famille', 'Famille')], validators=[DataRequired()])
    submit = SubmitField('S\'inscrire')

class LoginForm(FlaskForm):
    username = StringField('Prénom Nom', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')

class GuessForm(FlaskForm):
    dob = DateField('Date de naissance (estimée)', format='%Y-%m-%d', validators=[Optional()])
    sex = SelectField('Sexe', choices=[('Fille', 'Fille'), ('Garçon', 'Garçon'), ('Surprise', 'Surprise')], validators=[Optional()])
    first_name = StringField('Prénom', validators=[Optional()])
    height = FloatField('Taille (cm)', validators=[Optional()])
    weight = FloatField('Poids (kg)', validators=[Optional()])
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

class ScoringRuleForm(FlaskForm):
    category = SelectField('Catégorie', choices=[
        ('Date prévue', 'Date prévue'),
        ('Sexe', 'Sexe'),
        ('Prénom', 'Prénom'),
        ('Taille', 'Taille'),
        ('Poids', 'Poids'),
        ('Couleur de peau', 'Couleur de peau'),
        ('Couleur des yeux', 'Couleur des yeux'),
        ('Couleur des cheveux', 'Couleur des cheveux')
    ], validators=[DataRequired()])
    base_points = IntegerField('Points pour le plus proche (ou correct)', validators=[DataRequired()])
    decrement_per_rank = IntegerField('Points perdus par rang d\'écart (ex: 5)', validators=[Optional()])
    exact_bonus = IntegerField('Bonus si valeur exacte (ex: 10)', validators=[Optional()])
    submit_rule = SubmitField('Ajouter la règle')

class CalculatorForm(FlaskForm):
    dob = DateField('Date de naissance réelle', format='%Y-%m-%d', validators=[DataRequired()])
    sex = SelectField('Sexe réel', choices=[('Fille', 'Fille'), ('Garçon', 'Garçon')], validators=[DataRequired()])
    first_name = StringField('Prénom réel', validators=[DataRequired()])
    height = FloatField('Taille réelle (cm)', validators=[DataRequired()])
    weight = FloatField('Poids réel (kg)', validators=[DataRequired()])
    skin_color = SelectField('Couleur de peau', choices=[('', '---'), ('Blanche', 'Blanche'), ('Mate', 'Mate'), ('Noire', 'Noire'), ('Métissée', 'Métissée'), ('Autre', 'Autre')], validators=[Optional()])
    eye_color = SelectField('Couleur des yeux', choices=[('', '---'), ('Marrons', 'Marrons'), ('Bleus', 'Bleus'), ('Verts', 'Verts'), ('Noisette', 'Noisette'), ('Gris', 'Gris'), ('Autre', 'Autre')], validators=[Optional()])
    hair_color = SelectField('Couleur des cheveux', choices=[('', '---'), ('Bruns', 'Bruns'), ('Châtains', 'Châtains'), ('Blonds', 'Blonds'), ('Roux', 'Roux'), ('Noirs', 'Noirs'), ('Chauve', 'Chauve (sans cheveux)'), ('Autre', 'Autre')], validators=[Optional()])
    submit = SubmitField('Calculer les résultats')

class FormConfigForm(FlaskForm):
    show_dob = BooleanField('Date de naissance')
    show_sex = BooleanField('Sexe')
    show_first_name = BooleanField('Prénom')
    show_height = BooleanField('Taille')
    show_weight = BooleanField('Poids')
    show_skin_color = BooleanField('Couleur de peau')
    show_eye_color = BooleanField('Couleur des yeux')
    show_hair_color = BooleanField('Couleur des cheveux')
    show_hints = BooleanField('Afficher les indices')
    lock_sex = BooleanField('Bloquer le Sexe (force la valeur définie en haut)')
    anonymous_mode = BooleanField('Mode anonyme (masquer les noms)')
    show_category = BooleanField('Afficher la catégorie des participants')
    prize_text = TextAreaField('Ce qui est à gagner')
    rules_text = TextAreaField('Règles de comptabilisation')
    
    # New table visibility fields
    table_show_dob = BooleanField('Date de naissance')
    table_show_sex = BooleanField('Sexe')
    table_show_first_name = BooleanField('Prénom')
    table_show_height = BooleanField('Taille')
    table_show_weight = BooleanField('Poids')
    table_show_skin_color = BooleanField('Couleur de peau')
    table_show_eye_color = BooleanField('Couleur des yeux')
    table_show_hair_color = BooleanField('Couleur des cheveux')
    
    # Access config
    enable_stats_page = BooleanField('Activer la page Statistiques')
    enable_table_page = BooleanField('Activer la page Tableau public')
    welcome_message = TextAreaField('Message de bienvenue')
    
    submit_config = SubmitField('Enregistrer la configuration')

@app.context_processor
def inject_config():
    form_config = FormConfig.query.first()
    if not form_config:
        form_config = FormConfig()
    return dict(config=form_config)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/table')
def public_table():
    form_config = FormConfig.query.first()
    if not form_config:
        form_config = FormConfig()
    if not form_config.enable_table_page and not (current_user.is_authenticated and current_user.is_admin):
        flash('Le tableau des pronostics n\'est pas disponible.', 'warning')
        return redirect(url_for('index'))
        
    guesses = Guess.query.all()
    return render_template('index.html', guesses=guesses, config=form_config)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        username_val = f"{form.first_name.data.strip()} {form.last_name.data.strip()}"
        existing_user = User.query.filter_by(username=username_val).first()
        if existing_user:
            flash('Ce prénom et nom sont déjà enregistrés.', 'danger')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        is_admin = False # Admin account is already created, new users are not admins
        new_user = User(username=username_val, password_hash=hashed_password, is_admin=is_admin, category=form.category.data)
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
    clues = Clue.query.all()
    # Group clues by theme
    clues_by_theme = {}
    for clue in clues:
        if clue.theme not in clues_by_theme:
            clues_by_theme[clue.theme] = []
        clues_by_theme[clue.theme].append(clue)
        
    for theme in clues_by_theme:
        clues_by_theme[theme].sort(key=lambda c: str(c.value).lower())
    
    # Sort themes based on priority: Terme, Taille, Poids, Prénom, then alphabetical
    def theme_priority(theme_name):
        t = theme_name.lower()
        if 'terme' in t or 'date' in t: return 1
        if 'taille' in t: return 2
        if 'poids' in t: return 3
        if 'prénom' in t or 'prenom' in t: return 4
        return 5

    sorted_themes = sorted(clues_by_theme.keys(), key=lambda x: (theme_priority(x), x))
    sorted_clues_by_theme = {k: clues_by_theme[k] for k in sorted_themes}

    return render_template('info.html', clues_by_theme=sorted_clues_by_theme, baby_info=baby_info)

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
        
    form_config = FormConfig.query.first()
    if not form_config:
        form_config = FormConfig()
        db.session.add(form_config)
        db.session.commit()

    clue_form = ClueForm()
    date_form = DueDateForm()
    config_form = FormConfigForm()
    scoring_rule_form = ScoringRuleForm()
    
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
        
    if scoring_rule_form.submit_rule.data and scoring_rule_form.validate_on_submit():
        new_rule = ScoringRule(
            category=scoring_rule_form.category.data,
            base_points=scoring_rule_form.base_points.data,
            decrement_per_rank=scoring_rule_form.decrement_per_rank.data or 0,
            exact_bonus=scoring_rule_form.exact_bonus.data or 0
        )
        db.session.add(new_rule)
        db.session.commit()
        flash('Règle de comptabilisation ajoutée.', 'success')
        return redirect(url_for('admin_info'))
        
    if config_form.submit_config.data and config_form.validate_on_submit():
        form_config.show_dob = config_form.show_dob.data
        form_config.show_sex = config_form.show_sex.data
        form_config.show_first_name = config_form.show_first_name.data
        form_config.show_height = config_form.show_height.data
        form_config.show_weight = config_form.show_weight.data
        form_config.show_skin_color = config_form.show_skin_color.data
        form_config.show_eye_color = config_form.show_eye_color.data
        form_config.show_hair_color = config_form.show_hair_color.data
        form_config.show_hints = config_form.show_hints.data
        form_config.lock_sex = config_form.lock_sex.data
        form_config.anonymous_mode = config_form.anonymous_mode.data
        form_config.show_category = config_form.show_category.data
        form_config.prize_text = config_form.prize_text.data
        form_config.rules_text = config_form.rules_text.data
        
        form_config.table_show_dob = config_form.table_show_dob.data
        form_config.table_show_sex = config_form.table_show_sex.data
        form_config.table_show_first_name = config_form.table_show_first_name.data
        form_config.table_show_height = config_form.table_show_height.data
        form_config.table_show_weight = config_form.table_show_weight.data
        form_config.table_show_skin_color = config_form.table_show_skin_color.data
        form_config.table_show_eye_color = config_form.table_show_eye_color.data
        form_config.table_show_hair_color = config_form.table_show_hair_color.data
        
        form_config.enable_stats_page = config_form.enable_stats_page.data
        form_config.enable_table_page = config_form.enable_table_page.data
        form_config.welcome_message = config_form.welcome_message.data
        
        db.session.commit()
        flash('Configuration du formulaire mise à jour.', 'success')
        return redirect(url_for('admin_info'))

    # Populate forms
    if request.method == 'GET':
        date_form.due_date.data = baby_info.due_date
        date_form.sex.data = baby_info.sex
        
        config_form.show_dob.data = form_config.show_dob
        config_form.show_sex.data = form_config.show_sex
        config_form.show_first_name.data = form_config.show_first_name
        config_form.show_height.data = form_config.show_height
        config_form.show_weight.data = form_config.show_weight
        config_form.show_skin_color.data = form_config.show_skin_color
        config_form.show_eye_color.data = form_config.show_eye_color
        config_form.show_hair_color.data = form_config.show_hair_color
        config_form.show_hints.data = form_config.show_hints
        config_form.lock_sex.data = form_config.lock_sex
        config_form.anonymous_mode.data = form_config.anonymous_mode
        config_form.show_category.data = form_config.show_category
        config_form.prize_text.data = form_config.prize_text
        config_form.rules_text.data = form_config.rules_text
        
        config_form.table_show_dob.data = form_config.table_show_dob
        config_form.table_show_sex.data = form_config.table_show_sex
        config_form.table_show_first_name.data = form_config.table_show_first_name
        config_form.table_show_height.data = form_config.table_show_height
        config_form.table_show_weight.data = form_config.table_show_weight
        config_form.table_show_skin_color.data = form_config.table_show_skin_color
        config_form.table_show_eye_color.data = form_config.table_show_eye_color
        config_form.table_show_hair_color.data = form_config.table_show_hair_color
        
        config_form.enable_stats_page.data = form_config.enable_stats_page
        config_form.enable_table_page.data = form_config.enable_table_page
        config_form.welcome_message.data = form_config.welcome_message
        
    scoring_rules = ScoringRule.query.all()
        
    return render_template('admin_info.html', form=clue_form, date_form=date_form, config_form=config_form, scoring_rule_form=scoring_rule_form, clues=clues, themes=themes, scoring_rules=scoring_rules)

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

@app.route('/admin/scoring/delete/<int:rule_id>', methods=['POST'])
@login_required
def delete_scoring_rule(rule_id):
    if not current_user.is_admin:
        flash('Accès refusé.', 'danger')
        return redirect(url_for('index'))
    rule = ScoringRule.query.get_or_404(rule_id)
    db.session.delete(rule)
    db.session.commit()
    flash('Règle supprimée.', 'success')
    return redirect(url_for('admin_info'))

@app.route('/admin/info/edit/<int:clue_id>', methods=['GET', 'POST'])
@login_required
def edit_clue(clue_id):
    if not current_user.is_admin:
        flash('Accès non autorisé.', 'danger')
        return redirect(url_for('index'))
    
    clue = Clue.query.get_or_404(clue_id)
    form = ClueForm()
    
    if form.validate_on_submit():
        clue.theme = form.theme.data
        clue.value = form.value.data
        clue.relation_link = form.relation_link.data
        clue.relative_name = form.relative_name.data
        db.session.commit()
        flash('Indice mis à jour avec succès.', 'success')
        return redirect(url_for('admin_info'))
        
    elif request.method == 'GET':
        form.theme.data = clue.theme
        form.value.data = clue.value
        form.relation_link.data = clue.relation_link
        form.relative_name.data = clue.relative_name
        
    themes_query = db.session.query(Clue.theme).distinct().all()
    themes = [t[0] for t in themes_query]
        
    return render_template('edit_clue.html', form=form, themes=themes)

@app.route('/guess', methods=['GET', 'POST'])
@login_required
def guess():
    form = GuessForm()
    existing_guess = Guess.query.filter_by(user_id=current_user.id).first()
    
    # Get hints & config
    baby_info = BabyInfo.query.first()
    prenom_clues = Clue.query.filter_by(theme='Prénom').all()
    form_config = FormConfig.query.first()
    if not form_config:
        form_config = FormConfig()
    
    if form.validate_on_submit():
        # Force sex if locked
        final_sex = baby_info.sex if (form_config.lock_sex and baby_info and baby_info.sex) else form.sex.data
        
        if existing_guess:
            # Update existing
            existing_guess.dob = form.dob.data
            existing_guess.sex = final_sex
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
                sex=final_sex,
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
        
    # Pre-fill sex if locked (even for existing guesses, we overwrite their view)
    if form_config.lock_sex and baby_info and baby_info.sex:
        form.sex.data = baby_info.sex
        
    scoring_rules = ScoringRule.query.all()
        
    return render_template('guess_form.html', form=form, existing=bool(existing_guess), baby_info=baby_info, prenom_clues=prenom_clues, config=form_config, scoring_rules=scoring_rules)
@app.route('/stats')
def stats():
    form_config = FormConfig.query.first()
    if not form_config:
        form_config = FormConfig()
    
    if not form_config.enable_stats_page and not (current_user.is_authenticated and current_user.is_admin):
        flash('Les statistiques ne sont pas encore disponibles.', 'warning')
        return redirect(url_for('index'))
        
    guesses = Guess.query.all()
    # Prepare data for ECharts
    data = []
    for g in guesses:
        data.append({
            'dob': g.dob.strftime('%Y-%m-%d') if g.dob else None,
            'weight': g.weight,
            'height': g.height,
            'first_name': g.first_name,
            'category': g.user.category if g.user and g.user.category else 'Autre'
        })
    import json
    baby_info = BabyInfo.query.first()
    actual_due_date = baby_info.due_date.strftime('%Y-%m-%d') if baby_info and baby_info.due_date else None
    return render_template('stats.html', stats_data=json.dumps(data), actual_due_date=actual_due_date)

import csv
from io import StringIO
from flask import Response
from datetime import datetime

@app.route('/admin/export/csv')
@login_required
def export_csv():
    if not current_user.is_admin:
        flash('Accès refusé.', 'danger')
        return redirect(url_for('index'))
        
    guesses = Guess.query.all()
    
    # Create CSV in memory
    si = StringIO()
    cw = csv.writer(si)
    
    # Write headers
    cw.writerow([
        'Nom', 'Categorie_Utilisateur', 'Date_Prevue', 'Sexe', 'Prenom', 
        'Taille', 'Poids', 'Couleur_Peau', 'Couleur_Yeux', 'Couleur_Cheveux', 'Mot_De_Passe_Hash'
    ])
    
    # Write data
    for g in guesses:
        cw.writerow([
            g.user.username,
            g.user.category or '',
            g.dob.strftime('%Y-%m-%d') if g.dob else '',
            g.sex,
            g.first_name,
            g.height,
            g.weight,
            g.skin_color or '',
            g.eye_color or '',
            g.hair_color or '',
            g.user.password_hash
        ])
        
    output = si.getvalue()
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=sauvegarde_pronostics.csv"}
    )

@app.route('/admin/import/csv', methods=['POST'])
@login_required
def import_csv():
    if not current_user.is_admin:
        flash('Accès refusé.', 'danger')
        return redirect(url_for('index'))
        
    if 'csv_file' not in request.files:
        flash('Aucun fichier envoyé.', 'danger')
        return redirect(url_for('admin_info'))
        
    file = request.files['csv_file']
    if file.filename == '':
        flash('Aucun fichier sélectionné.', 'danger')
        return redirect(url_for('admin_info'))
        
    if file and file.filename.endswith('.csv'):
        stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        
        headers = next(csv_input, None)
        if not headers or headers[0] != 'Nom':
            flash('Le format du CSV est invalide. Vérifiez que la première colonne est "Nom".', 'danger')
            return redirect(url_for('admin_info'))
            
        success_count = 0
        for row in csv_input:
            if len(row) < 11:
                continue
                
            username = row[0]
            category = row[1]
            dob_str = row[2]
            sex = row[3]
            first_name = row[4]
            height_str = row[5]
            weight_str = row[6]
            skin = row[7]
            eye = row[8]
            hair = row[9]
            pwd_hash = row[10]
            
            # Check or create User
            user = User.query.filter_by(username=username).first()
            if not user:
                user = User(
                    username=username,
                    password_hash=pwd_hash or generate_password_hash('password123', method='pbkdf2:sha256'),
                    category=category,
                    is_admin=False
                )
                db.session.add(user)
                db.session.commit()
            
            # Check or create Guess
            guess = Guess.query.filter_by(user_id=user.id).first()
            try:
                dob = datetime.strptime(dob_str, '%Y-%m-%d').date() if dob_str else None
                height = float(height_str) if height_str else 0.0
                weight = float(weight_str) if weight_str else 0.0
            except ValueError:
                continue
                
            if guess:
                guess.dob = dob
                guess.sex = sex
                guess.first_name = first_name
                guess.height = height
                guess.weight = weight
                guess.skin_color = skin
                guess.eye_color = eye
                guess.hair_color = hair
            else:
                guess = Guess(
                    user_id=user.id,
                    dob=dob,
                    sex=sex,
                    first_name=first_name,
                    height=height,
                    weight=weight,
                    skin_color=skin,
                    eye_color=eye,
                    hair_color=hair
                )
                db.session.add(guess)
                
            success_count += 1
            
        db.session.commit()
        flash(f'Importation réussie ! {success_count} pronostics traités.', 'success')
        return redirect(url_for('admin_info'))
        
    flash('Fichier invalide. Veuillez importer un fichier .csv', 'danger')
    return redirect(url_for('admin_info'))



@app.route('/admin/results', methods=['GET', 'POST'])
@login_required
def admin_results():
    if not current_user.is_admin:
        flash('Accès refusé.', 'danger')
        return redirect(url_for('index'))
        
    form = CalculatorForm()
    results = None
    
    if form.validate_on_submit():
        guesses = Guess.query.all()
        rules_raw = ScoringRule.query.all()
        rules = {r.category: r for r in rules_raw}
        
        # Initialize results dictionary per user
        user_scores = {}
        for g in guesses:
            user_scores[g.user_id] = {
                'user': g.user,
                'guess': g,
                'total_score': 0,
                'details': {}
            }
            
        # Helper for exact match scoring
        def score_exact(category_name, true_val, guess_attr, transform=lambda x: x):
            if category_name not in rules: return
            rule = rules[category_name]
            for g in guesses:
                guess_val = getattr(g, guess_attr)
                score = 0
                if guess_val and true_val and transform(guess_val) == transform(true_val):
                    score = rule.base_points + rule.exact_bonus
                user_scores[g.user_id]['details'][category_name] = score
                user_scores[g.user_id]['total_score'] += score

        # Score exact matches
        score_exact('Sexe', form.sex.data, 'sex')
        score_exact('Prénom', form.first_name.data, 'first_name', lambda x: str(x).strip().lower() if x else '')
        score_exact('Couleur de peau', form.skin_color.data, 'skin_color')
        score_exact('Couleur des yeux', form.eye_color.data, 'eye_color')
        score_exact('Couleur des cheveux', form.hair_color.data, 'hair_color')
        
        # Helper for ranked scoring (numbers/dates)
        def score_ranked(category_name, true_val, guess_attr, diff_func):
            if category_name not in rules or true_val is None: return
            rule = rules[category_name]
            
            # Calculate diffs
            diffs = []
            for g in guesses:
                guess_val = getattr(g, guess_attr)
                if guess_val is not None:
                    d = diff_func(guess_val, true_val)
                    diffs.append((d, g.user_id))
                else:
                    user_scores[g.user_id]['details'][category_name] = 0
            
            # Sort by diff (ascending)
            diffs.sort(key=lambda x: x[0])
            
            current_rank = 1
            last_diff = None
            for idx, (d, uid) in enumerate(diffs):
                if last_diff is not None and d > last_diff:
                    current_rank = idx + 1 # standard competition ranking (1, 2, 2, 4)
                last_diff = d
                
                points = rule.base_points - ((current_rank - 1) * rule.decrement_per_rank)
                points = max(0, points) # No negative points
                
                if d == 0:
                    points += rule.exact_bonus
                    
                user_scores[uid]['details'][category_name] = points
                user_scores[uid]['total_score'] += points
                
        # Score ranked matches
        score_ranked('Taille', form.height.data, 'height', lambda g, t: abs(g - t))
        score_ranked('Poids', form.weight.data, 'weight', lambda g, t: abs(g - t))
        score_ranked('Date prévue', form.dob.data, 'dob', lambda g, t: abs((g - t).days))
        
        # Format results for template
        results_list = list(user_scores.values())
        results_list.sort(key=lambda x: x['total_score'], reverse=True)
        
        # Assign final ranking
        final_rank = 1
        last_score = None
        for idx, res in enumerate(results_list):
            if last_score is not None and res['total_score'] < last_score:
                final_rank = idx + 1
            res['rank'] = final_rank
            last_score = res['total_score']
            
        results = {
            'list': results_list,
            'categories': list(rules.keys())
        }

    return render_template('results.html', form=form, results=results)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
