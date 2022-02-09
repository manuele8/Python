array_nomi_p = (["Alacromatica Evolutiva", "Accolito di C'thun", "Imp Rivoltante", "Canaglia"],
                ["Gatto Soriano", "Gatto Soriano", "Canaglia", "Iena Rovistatrice"])
array_stats_p = ([(3, 4), (3, 2), (1, 1), (1, 1)], [(3, 1), (3, 1), (2, 2), (1, 1)])
array_of_abilities_p = (["", "sd", "", "rn"], ["sd", "sd", "pv", "rn"])
number = 10000

def ask_array(names):
    global array_nomi_p, array_stats_p, array_of_abilities_p
    array_nomi_p = [[], []]
    array_stats_p = [[], []]
    array_of_abilities_p = [[], []]
    num = input("Quanti servitori sul tuo lato del campo, quanti su quello avversario? ")
    num_f, num_e = int(num.split(",")[0]), int(num.split(", ")[1])
    array_nomi_p[0], array_nomi_p[1] = [0] * num_f, [0] * num_e
    array_stats_p[0], array_stats_p[1] = [0] * num_f, [0] * num_e
    array_of_abilities_p[0], array_of_abilities_p[1] = [0] * num_f, [0] * num_e
    array_nomi_p, array_stats_p, array_of_abilities_p = tuple(array_nomi_p), tuple(array_stats_p), tuple(
        array_of_abilities_p)
    print(array_stats_p)
    print(array_nomi_p)
    print(array_of_abilities_p)
    print("Inserisci il nome dei tuoi servitori ")
    for i in range(1, len(array_nomi_p[0]) + 1):
        nome = input("Inserisci il nome del servitore numero " + str(i) + ": ")
        if nome not in names:
            pass
        array_nomi_p[0][i - 1] = nome
    print("Inserisci il nome dei servitori nemici ")
    for i in range(1, len(array_nomi_p[1]) + 1):
        nome = input("Inserisci il nome del servitore numero " + str(i) + ": ")
        array_nomi_p[1][i - 1] = nome
    print("Inserisci le stats dei tuoi servitori ")
    for i in range(1, len(array_stats_p[0]) + 1):
        stats = input("Inserisci le stats del servitore numero " + str(i) + ": ")
        stats_a, stats_h = int(stats.split(', ')[0]), int(stats.split(', ')[1])
        stats = (stats_a, stats_h)
        array_stats_p[0][i - 1] = stats
    print("Inserisci le stats dei servitori nemici ")
    for i in range(1, len(array_stats_p[1]) + 1):
        stats = input("Inserisci le stats del servitore numero " + str(i) + ": ")
        stats_a, stats_h = int(stats.split(', ')[0]), int(stats.split(', ')[1])
        stats = (stats_a, stats_h)
        array_stats_p[1][i - 1] = stats
    print("Inserisci le abilità dei tuoi servitori ")
    for i in range(1, len(array_of_abilities_p[0]) + 1):
        abilities = input("Inserisci le abilità del servitore numero " + str(i) + ": ")
        array_of_abilities_p[0][i - 1] = abilities
    print("Inserisci le abilità dei servitori nemici ")
    for i in range(1, len(array_of_abilities_p[1]) + 1):
        abilities = input("Inserisci le abilità del servitore numero " + str(i) + ": ")
        array_of_abilities_p[1][i - 1] = abilities

