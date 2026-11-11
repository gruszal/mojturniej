from import_from_tournify.import_from_tournify import KeysPL
from results.update import update_wyniki

if __name__ == '__main__':
    filename = "Harmonogram meczowy - Mój Turniej 20.xlsx"

    teams = [
        ('Maciek', "Korona Kielce", 2.5),
        ('Wojtek', "Legia Warszawa", 2.5),
        ('Alek', "Radomiak Radom", 2.5),
        ('Domin', "Raków Częstochowa", 3),
        ('Bartek', "Lech Poznań", 3.5),
    ]

    tournament = "20"

    update_wyniki(filename, teams, tournament, keys=KeysPL())
