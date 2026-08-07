from import_from_tournify.import_from_tournify import KeysPL
from results.update import update_wyniki

if __name__ == '__main__':
    filename = "Harmonogram meczowy - Mój Turniej 19.xlsx"

    teams = [
        ('Maciek', "Chorwacja", 4.5),
        ('Wojtek', "Meksyk", 4),
        ('Alek', "Norwegia", 4),
        ('Domin', "Maroko", 4.5),
        ('Bartek', "Hiszpania", 5),
    ]

    tournament = "19"

    update_wyniki(filename, teams, tournament, keys=KeysPL())
