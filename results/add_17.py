from import_from_tournify.import_from_tournify import KeysPL
from results.update import update_wyniki

if __name__ == '__main__':
    filename = "Harmonogram meczowy - Mój Turniej 17.xlsx"

    teams = [
        ('Maciek', "Chelsea", 4.5),
        ('Wojtek', "Ajax", 4),
        ('Alek', "Torino", 4),
        ('Domin', "Borussia Dortmund", 4.5),
        ('Bartek', "Barcelona", 5),
    ]

    tournament = "17"

    update_wyniki(filename, teams, tournament, keys=KeysPL())
