import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

if not content.startswith('"""'):
    content = '"""\nModule principal de l\'application Baby Shower.\nContient les modèles de base de données, les formulaires Web et les routes pour gérer les pronostics, les utilisateurs et l\'administration.\n"""\n' + content

docstrings = {
    'class User': '"""Modèle de base de données représentant un utilisateur (participant ou admin)."""',
    'class BabyInfo': '"""Modèle stockant les informations réelles du bébé (terme, sexe, etc.)."""',
    'class Clue': '"""Modèle représentant un indice donné aux participants."""',
    'class ScoringRule': '"""Modèle définissant les règles de calcul des points pour le classement."""',
    'class Guess': '"""Modèle représentant le pronostic d\'un participant."""',
    'class SiteLog': '"""Modèle stockant l\'historique des actions (logs) de l\'application."""',
    'class FormConfig': '"""Modèle stockant la configuration globale (visibilité, affichage, couleurs)."""',
    'class RegistrationForm': '"""Formulaire d\'inscription pour les nouveaux utilisateurs."""',
    'class LoginForm': '"""Formulaire de connexion."""',
    'class GuessForm': '"""Formulaire de saisie d\'un pronostic pour le bébé."""',
    'class ClueForm': '"""Formulaire d\'ajout et de modification d\'un indice (admin)."""',
    'class DueDateForm': '"""Formulaire pour mettre à jour les informations de naissance (admin)."""',
    'class ScoringRuleForm': '"""Formulaire de paramétrage du barème de points (admin)."""',
    'class FormConfigForm': '"""Formulaire de configuration globale de l\'application (admin)."""',
    'def log_event': '"""\n    Enregistre un événement dans la table SiteLog.\n    :param message: Le message à logger.\n    :param level: Niveau d\'alerte (INFO, WARNING, etc.).\n    :param user_id: ID de l\'utilisateur concerné (optionnel).\n    """',
    'def load_user': '"""Charge un utilisateur depuis la session pour Flask-Login."""',
    'def inject_config': '"""Injecte la configuration globale dans tous les templates Jinja2."""',
    'def index': '"""Affiche la page d\'accueil et gère la création/mise à jour d\'un pronostic."""',
    'def public_table': '"""Affiche le tableau public des pronostics de tous les participants."""',
    'def toggle_view': '"""Bascule l\'affichage des pronostics (liste ou grille) dans la session."""',
    'def toggle_hide_guess': '"""Permet à l\'admin de masquer ou d\'afficher un pronostic public."""',
    'def delete_guess': '"""Permet à l\'admin de supprimer le pronostic d\'un utilisateur."""',
    'def register': '"""Gère l\'inscription d\'un nouvel utilisateur."""',
    'def login': '"""Gère la connexion d\'un utilisateur."""',
    'def logout': '"""Déconnecte l\'utilisateur actuel."""',
    'def info': '"""Affiche la liste des indices publics et les informations sur le bébé."""',
    'def admin_info': '"""Tableau de bord d\'administration : configuration, logs, règles, et indices."""',
    'def admin_results': '"""Affiche le classement final calculé d\'après le barème et les informations du bébé."""',
    'def export_csv': '"""Exporte tous les utilisateurs et pronostics en fichier CSV."""',
    'def import_csv': '"""Importe et restaure les données (utilisateurs, pronostics) depuis un CSV."""'
}

lines = content.split('\n')
new_lines = []

for i, line in enumerate(lines):
    new_lines.append(line)
    stripped = line.strip()
    
    if i + 1 < len(lines) and lines[i+1].strip().startswith('"""'):
        continue
        
    for key, doc in docstrings.items():
        if stripped.startswith(key + '(') or stripped.startswith(key + ':'):
            indent = line[:len(line) - len(line.lstrip())]
            doc_lines = doc.split('\n')
            for dline in doc_lines:
                new_lines.append(f"{indent}    {dline}")
            break

with open('app.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))
