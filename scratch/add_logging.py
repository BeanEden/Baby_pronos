import os

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add SiteLog model
sitelog_model = """class SiteLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    level = db.Column(db.String(20), default='INFO')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    message = db.Column(db.Text, nullable=False)
    user_rel = db.relationship('User', backref='logs')

def log_event(message, level='INFO', user_id=None):
    try:
        new_log = SiteLog(message=message, level=level, user_id=user_id)
        db.session.add(new_log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()

class FormConfig(db.Model):"""

if 'class SiteLog' not in content:
    content = content.replace('class FormConfig(db.Model):', sitelog_model)

# 2. Add logging to /register
register_str = """        new_user = User(username=username, password_hash=password_hash, category=category, is_admin=is_admin)
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        log_event(f"Nouvel utilisateur inscrit : {username}", user_id=new_user.id)
        flash('Inscription réussie.', 'success')
        return redirect(url_for('guess'))"""

old_register_str = """        new_user = User(username=username, password_hash=password_hash, category=category, is_admin=is_admin)
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        flash('Inscription réussie.', 'success')
        return redirect(url_for('guess'))"""

content = content.replace(old_register_str, register_str)

# 3. Add logging to /login
login_str = """            login_user(user)
            log_event(f"Connexion réussie : {user.username}", user_id=user.id)
            return redirect(url_for('guess'))"""
old_login_str = """            login_user(user)
            return redirect(url_for('guess'))"""
content = content.replace(old_login_str, login_str)

# 4. Add logging to /guess (creation/update)
guess_str = """        else:
            log_event(f"Pronostic enregistré/modifié", user_id=current_user.id)
            flash('Pronostic enregistré avec succès !', 'success')
            return redirect(url_for('table'))
    elif form.errors:
        flash('Erreur lors de la sauvegarde du pronostic.', 'danger')"""
old_guess_str = """        else:
            flash('Erreur lors de la sauvegarde du pronostic.', 'danger')
            return redirect(url_for('table'))
    elif form.errors:
        flash('Erreur lors de la sauvegarde du pronostic.', 'danger')"""
content = content.replace(old_guess_str, guess_str)

# Try another version of old_guess_str if the previous one didn't match exactly
old_guess_str2 = """        else:
            flash('Pronostic enregistré avec succès !', 'success')
            return redirect(url_for('table'))
    elif form.errors:
        flash('Erreur lors de la sauvegarde du pronostic.', 'danger')"""
if old_guess_str2 in content:
    content = content.replace(old_guess_str2, guess_str)


# 5. Add routes for /admin/logs and /admin/logs/export
logs_routes = """
@app.route('/admin/logs')
@login_required
def admin_logs():
    if not current_user.is_admin:
        flash('Accès refusé.', 'danger')
        return redirect(url_for('index'))
    logs = SiteLog.query.order_by(SiteLog.timestamp.desc()).limit(500).all()
    return render_template('admin_logs.html', logs=logs)

@app.route('/admin/logs/export')
@login_required
def export_logs_csv():
    if not current_user.is_admin:
        flash('Accès refusé.', 'danger')
        return redirect(url_for('index'))
    
    logs = SiteLog.query.order_by(SiteLog.timestamp.desc()).all()
    
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Date', 'Heure', 'Niveau', 'Utilisateur', 'Message'])
    
    for l in logs:
        cw.writerow([
            l.id,
            l.timestamp.strftime('%Y-%m-%d'),
            l.timestamp.strftime('%H:%M:%S'),
            l.level,
            l.user_rel.username if l.user_rel else 'Système',
            l.message
        ])
    
    output = si.getvalue()
    si.close()
    
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=logs_site.csv"}
    )
"""

if '@app.route(\'/admin/logs\')' not in content:
    # insert before @app.route('/admin/simulator')
    content = content.replace("@app.route('/admin/simulator')", logs_routes + "\n@app.route('/admin/simulator')")


with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
