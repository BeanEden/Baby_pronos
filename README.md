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

### 2. Déployer sur Vercel
1. Créez un compte gratuit sur [Vercel](https://vercel.com/) et connectez-y votre compte GitHub.
2. Cliquez sur **Add New... > Project** et importez votre dépôt GitHub "Baby Pronos".
3. Dans la section **Environment Variables** (avant de cliquer sur Deploy), ajoutez la variable suivante :
   - `SECRET_KEY` : Saisissez une phrase secrète complexe (ex: `ma_clef_secrete_12345!`). Elle est indispensable pour sécuriser les mots de passe de vos participants.
4. Cliquez sur **Deploy**. (Le déploiement va se terminer, mais le site ne fonctionnera pas encore car il n'a pas de base de données).

### 3. Activer la Base de Données (Vercel Storage)
Vercel propose des bases de données gratuites intégrées.
1. Depuis le tableau de bord de votre projet Vercel, allez dans l'onglet **Storage**.
2. Cliquez sur **Create Database** et choisissez **Postgres**.
3. Acceptez les conditions, donnez un nom à votre base (ex: *baby-pronos-db*) et choisissez la région la plus proche de chez vous (ex: Frankfurt ou Paris).
4. Une fois créée, cliquez sur **Connect Project** pour lier la base de données à votre projet Baby Pronos.
5. Vercel a désormais automatiquement ajouté la variable `POSTGRES_URL` à votre projet !
6. Allez dans l'onglet **Deployments** de votre projet Vercel, cliquez sur les trois petits points à côté de votre dernier déploiement, et choisissez **Redeploy**.

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
