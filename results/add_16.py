from results.update import update_wyniki

if __name__ == '__main__':
    filename = "Match schedule - Mój Turniej 16.xlsx"

    teams = [
        ('Maciek', "Chorwacja", 4.5),
        ('Wojtek', "Węgry", 3.5),
        ('Alek', "Irlandia", 3.5),
        ('Domin', "Ghana", 4),
        ('Bartek', "Argentyna", 5),
    ]

    tournament = "16"

    update_wyniki(filename, teams, tournament)