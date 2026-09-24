# Baby Pronos 🍼

Une application web interactive et ludique permettant à vos proches de faire des pronostics sur la naissance de votre futur bébé (date, heure, sexe, taille, poids, etc.).

## Fonctionnalités 🌟

- **Pronostics complets** : Les participants peuvent deviner de nombreuses caractéristiques (sexe, date, heure, prénom, taille, poids, couleurs des yeux/cheveux/peau).
- **Tableau de bord administrateur complet** : 
  - Configuration globale de l'application (masquage/affichage des champs).
  - Personnalisation dynamique des couleurs de l'application.
  - Gestion des utilisateurs et des pronostics (suppression, masquage).
  - Gestion d'un système de points et de barèmes personnalisables.
  - Ajout et édition d'indices pour guider les participants.
  - Sauvegarde et restauration des données via export/import CSV.
- **Classement automatique** : Une page dédiée affiche les scores et le classement de tous les participants en fonction des règles définies par l'administrateur.
- **Page de statistiques** : Visualisation globale des tendances des pronostics (histogrammes, répartitions).
- **Design moderne et responsive** : Interface adaptative pour mobile et ordinateur, avec support de thèmes personnalisés.

## Technologies Utilisées 🛠️

- **Backend** : Python, Flask, Flask-Login, Flask-Migrate
- **Base de données** : PostgreSQL (via SQLAlchemy)
- **Frontend** : HTML5, CSS3 natif, JavaScript (Chart.js pour les graphiques, DataTables pour les tableaux)
- **Déploiement** : Vercel

## Tutoriel de Déploiement (Vercel) 🚀

Vous souhaitez héberger votre propre version de Baby Pronos gratuitement ? Voici les étapes pour déployer l'application sur Vercel avec une base de données propre (PostgreSQL).

### 1. Préparer le code
1. Créez un compte sur [GitHub](https://github.com/) (si ce n'est pas déjà fait).
2. **Forkez** ce dépôt : cliquez sur le bouton **"Fork"** en haut à droite de cette page GitHub. Cela va créer une copie exacte du projet sur votre propre compte, que vous pourrez modifier et lier à Vercel sans affecter l'original.

### 2. Créer une Base de Données PostgreSQL
1. Créez un compte gratuit sur un fournisseur PostgreSQL comme [Supabase](https://supabase.com/) ou [Neon](https://neon.tech/).
2. Créez un nouveau projet/base de données.
3. Récupérez l'URL de connexion (de type `postgresql://user:password@host:port/dbname`). 
*(Note: Si vous utilisez Supabase, veillez à utiliser le port de transaction adapté ou ajoutez `?sslmode=require` si nécessaire).*

### 3. Déployer sur Vercel
1. Créez un compte gratuit sur [Vercel](https://vercel.com/) et connectez-y votre compte GitHub.
2. Cliquez sur **Add New... > Project** et importez votre dépôt GitHub "Baby Pronos".
3. Dans la section **Environment Variables** (avant de cliquer sur Deploy), ajoutez les deux variables suivantes :
   - `DATABASE_URL` : Collez l'URL de connexion PostgreSQL générée à l'étape 2.
   - `SECRET_KEY` : Saisissez une phrase secrète complexe (ex: `ma_clef_secrete_12345!`). Elle est indispensable pour sécuriser les mots de passe.
4. Cliquez sur **Deploy** et patientez.

### 4. Initialisation Automatique
Lors de la toute première ouverture de votre site web généré par Vercel :
1. L'application va détecter que la base de données est vide et **créera automatiquement toutes les tables**.
2. **Créez le tout premier compte** (via la page "Participer" / Inscription) : le premier compte créé devient automatiquement l'**Administrateur** du site !
3. Accédez ensuite à l'onglet "Administration" pour configurer les couleurs, les barèmes et les champs visibles pour vos proches.


## Auteur et Droits d'Utilisation ⚠️

Ce projet a été imaginé et réalisé par **Jean-Corentin Loirat**.

**Condition d'utilisation :**
Tout usage de cette application, de son code source ou de ses composants à des fins commerciales ou financières est **strictement interdit** sans l'accord préalable et explicite de l'auteur.

---
*Réalisé avec ❤️ pour de beaux moments en famille.*
