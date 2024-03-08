import sqlite3

# Connexion à la base de données SQLite (elle sera créée si elle n'existe pas)
conn = sqlite3.connect('discord_nicknames.db')
cursor = conn.cursor()

# Création de la table
cursor.execute('''
CREATE TABLE IF NOT EXISTS nicknames (
    user_id INTEGER PRIMARY KEY,
    original_nickname TEXT NOT NULL
)
''')

conn.commit()  # Appliquer les changements
conn.close()  # Fermer la connexion à la base de données
