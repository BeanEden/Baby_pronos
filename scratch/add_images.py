content = open('README.md', 'r', encoding='utf-8').read()

import re

# Insert accueil.png before ## Fonctionnalités
content = content.replace(
    '## Fonctionnalités 🌟',
    '<a href="images_git_hub/accueil.png"><img src="images_git_hub/accueil.png" width="800"></a>\n\n## Fonctionnalités 🌟'
)

# Insert fork_button.png
content = content.replace(
    '2. **Forkez** ce dépôt : cliquez sur le bouton **"Fork"** en haut à droite de cette page GitHub. Cela va créer une copie exacte du projet sur votre propre compte, que vous pourrez modifier et lier à Vercel sans affecter l\'original.',
    '2. **Forkez** ce dépôt : cliquez sur le bouton **"Fork"** en haut à droite de cette page GitHub. Cela va créer une copie exacte du projet sur votre propre compte, que vous pourrez modifier et lier à Vercel sans affecter l\'original.\n   <br><a href="images_git_hub/fork_button.png"><img src="images_git_hub/fork_button.png" width="300"></a>'
)

# Insert vercel_init.png
content = content.replace(
    '2. Cliquez sur **Add New... > Project** et importez votre dépôt GitHub "Baby Pronos".',
    '2. Cliquez sur **Add New... > Project** et importez votre dépôt GitHub "Baby Pronos".\n   <br><a href="images_git_hub/vercel_init.png"><img src="images_git_hub/vercel_init.png" width="300"></a>'
)

# Insert vercel_init_environment variable.png
content = content.replace(
    '   - `SECRET_KEY` : Saisissez une phrase secrète complexe (ex: `ma_clef_secrete_12345!`). Elle est indispensable pour sécuriser les mots de passe de vos participants.',
    '   - `SECRET_KEY` : Saisissez une phrase secrète complexe (ex: `ma_clef_secrete_12345!`). Elle est indispensable pour sécuriser les mots de passe de vos participants.\n   <br><a href="images_git_hub/vercel_init_environment variable.png"><img src="images_git_hub/vercel_init_environment variable.png" width="300"></a>'
)

# Insert vercel_storage.png
content = content.replace(
    '1. Depuis le tableau de bord de votre projet Vercel, allez dans l\'onglet **Storage**.',
    '1. Depuis le tableau de bord de votre projet Vercel, allez dans l\'onglet **Storage**.\n   <br><a href="images_git_hub/vercel_storage.png"><img src="images_git_hub/vercel_storage.png" width="300"></a>'
)

# Insert vercel_storage_2.png
content = content.replace(
    '2. Cliquez sur **Create Database** et choisissez **Postgres**.',
    '2. Cliquez sur **Create Database** et choisissez **Postgres**.\n   <br><a href="images_git_hub/vercel_storage_2.png"><img src="images_git_hub/vercel_storage_2.png" width="300"></a>'
)

# Insert vercel_storage_3.png
content = content.replace(
    '3. Acceptez les conditions, donnez un nom à votre base (ex: *baby-pronos-db*) et choisissez la région la plus proche de chez vous (ex: Frankfurt ou Paris).',
    '3. Acceptez les conditions, donnez un nom à votre base (ex: *baby-pronos-db*) et choisissez la région la plus proche de chez vous (ex: Frankfurt ou Paris).\n   <br><a href="images_git_hub/vercel_storage_3.png"><img src="images_git_hub/vercel_storage_3.png" width="300"></a>'
)

# Insert vercel_storage_4.png
content = content.replace(
    '4. Une fois créée, cliquez sur **Connect Project** pour lier la base de données à votre projet Baby Pronos.',
    '4. Une fois créée, cliquez sur **Connect Project** pour lier la base de données à votre projet Baby Pronos.\n   <br><a href="images_git_hub/vercel_storage_4.png"><img src="images_git_hub/vercel_storage_4.png" width="300"></a>'
)

# Insert vercel_storage_5.png
content = content.replace(
    '5. Vercel a désormais automatiquement ajouté la variable `POSTGRES_URL` à votre projet !',
    '5. Vercel a désormais automatiquement ajouté la variable `POSTGRES_URL` à votre projet !\n   <br><a href="images_git_hub/vercel_storage_5.png"><img src="images_git_hub/vercel_storage_5.png" width="300"></a>'
)

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(content)
