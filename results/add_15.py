from results.update import update_wyniki

if __name__ == '__main__':
    filename = "Match schedule - Mój Turniej 15.xlsx"

    teams = [
        ('Maciek', "Villareal", 4.5),
        ('Wojtek', "Al-ahli", 3.5),
        ('Alek', "Dinamo Zagreb", 3.5),
        ('Domin', "M'gladbach", 4),
        ('Bartek', "PSG", 5),
    ]

    tournament = "15"

    update_wyniki(filename, teams, tournament)