array_nomi_p = (['Canaglia', 'Elementale'], ['Canaglia', 'Elementale', 'Elementale', 'Elementale'])
array_stats_p = ([(4, 1), (4, 3)], [(3, 4), (2, 2), (3, 2), (2, 3)])
array_of_abilities_p = (['sd', 'pvsdrn'], ['', 'sd', '', 'vl'])
array_of_deathrattles_p = ([['gh'], ['gh']], [[], [], [], []])
array = []
number = 1000

#funzione utile solo a velocizzare il processo di scrittura dell'array con tutti i servitori sul campo a inizio battaglia, chiedendo il tutto all'esecutore del programma tramite diversi input.
def ask_array(names):
    global array_nomi_p, array_stats_p, array_of_abilities_p, array_of_deathrattles_p, array
    array_nomi_p = [[], []]
    array_stats_p = [[], []]
    array_of_abilities_p = [[], []]
    array_of_deathrattles_p = [[], []]
    num = input("Quanti servitori sul tuo lato del campo, quanti su quello avversario? ")
    num_f, num_e = int(num.split(",")[0]), int(num.split(", ")[1])
    array_nomi_p[0], array_nomi_p[1] = [0] * num_f, [0] * num_e
    array_stats_p[0], array_stats_p[1] = [0] * num_f, [0] * num_e
    array_of_abilities_p[0], array_of_abilities_p[1] = [0] * num_f, [0] * num_e
    array_of_deathrattles_p[0], array_of_deathrattles_p[1] = [0] * num_f, [0] * num_e
    array_nomi_p, array_stats_p, array_of_abilities_p, array_of_deathrattles_p = tuple(array_nomi_p), tuple(array_stats_p), tuple(
        array_of_abilities_p), tuple(array_of_deathrattles_p)
    print("Inserisci il nome dei tuoi servitori ")
    array = []
    array2 = names[:]
    list_abilities = ["", "pv", "sd", "vl", "rn", "fv", "sfv"]
    list_deathrattles = ['gsd', 'sd2', 'da', 'sg', 'dr', 'ba', 'br', 'st']
    for element in names:
        array2[array2.index(element)] = element.lower()
    for i in range(1, len(array_nomi_p[0]) + 1):
        nome = input("Inserisci il nome del servitore numero " + str(i) + ": ").lower()
        while 1:
            array = []
            for element in names:
                if nome in element.lower():
                    array.append(element)
            if len(array) == 1:
                nome = array[0]
                break
            elif len(array) < 1:
                nome = input(
                    "Non è stata trovata alcuna carta avente nome simile, reinserisci il nome adesso per favore: ")
            else:
                nome = array[int(input(
                    "Sono state trovate le seguenti carte, indica la posizione in questo array di quella che intendevi: " + str(
                        array) + " "))]
                break
        print(nome)
        array_nomi_p[0][i - 1] = nome
        print(array_nomi_p)
    print("Inserisci il nome dei servitori nemici ")
    for i in range(1, len(array_nomi_p[1]) + 1):
        nome = input("Inserisci il nome del servitore numero " + str(i) + ": ").lower()
        while 1:
            array = []
            for element in names:
                if nome in element.lower():
                    array.append(element)
            if len(array) == 1:
                nome = array[0]
                break
            elif len(array) < 1:
                nome = input(
                    "Non è stata trovata alcuna carta avente nome simile, reinserisci il nome adesso per favore: ")
            else:
                nome = array[int(input(
                    "Sono state trovate le seguenti carte, indica la posizione in questo array di quella che intendevi: " + str(
                        array) + " "))]
                break
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
    print("Inserisci le abilità dei tuoi servitori, ricordati che le abilità possono essere così scritte: " + str(
        list_abilities))
    for i in range(1, len(array_of_abilities_p[0]) + 1):
        abilities = input("Inserisci le abilità del servitore numero " + str(i) + ": ")
        array_of_abilities_p[0][i - 1] = abilities
    print("Inserisci le abilità dei servitori nemici, ricordati che le abilità possono essere così scritti: " + str(
        list_abilities))
    for i in range(1, len(array_of_abilities_p[1]) + 1):
        abilities = input("Inserisci le abilità del servitore numero " + str(i) + ": ")
        array_of_abilities_p[1][i - 1] = abilities
    print("Inserisci i rantoli di morte dei tuoi servitori, ricordati che i rantoli di morte possono essere così scritti: " + str(
        list_deathrattles))
    for i in range(1, len(array_of_deathrattles_p[0]) + 1):
        rantoli_di_morte = input("Inserisci i rantoli di morte del servitore numero " + str(i) + ": ")
        if not rantoli_di_morte == "":
            rantoli_di_morte = rantoli_di_morte.split(', ')
            array_of_deathrattles_p[0][i - 1] = rantoli_di_morte
        else:
            array_of_deathrattles_p[0][i - 1] = [""]
    print("Inserisci i rantoli di morte dei servitori nemici, ricordati che i rantoli di morte possono essere così scritti: " + str(
        list_abilities))
    for i in range(1, len(array_of_deathrattles_p[1]) + 1):
        rantoli_di_morte = input("Inserisci i rantoli di morte del servitore numero " + str(i) + ": ")
        if not rantoli_di_morte == "":
            rantoli_di_morte = rantoli_di_morte.split(', ')
            array_of_deathrattles_p[1][i - 1] = rantoli_di_morte
        else:
            array_of_deathrattles_p[1][i - 1] = [""]
