from import_from_tournify.import_from_tournify import KeysPL
from results.update import update_wyniki

if __name__ == '__main__':
    filename = "Harmonogram meczowy - Mój Turniej 18.xlsx"

    teams = [
        ('Maciek', "Hiszpania", 5),
        ('Wojtek', "Polska", 4),
        ('Alek', "Czechy", 4),
        ('Domin', "Niemcy", 5),
        ('Bartek', "Francja", 5),
    ]

    tournament = "18"

    update_wyniki(filename, teams, tournament, keys=KeysPL())
