import random
import Variables
#import Rantoli_di_Morte


class Personaggio:
    # definisci il personaggio
    def __init__(self, nome, tipo, attacco, salute, abilities, rantoli_di_morte):
        self.nome = nome
        self.tipo = tipo
        self.salute = salute
        self.max_salute = salute
        self.attacco = attacco
        self.abilities = abilities
        self.rantoli_di_morte = rantoli_di_morte

    # funzione attacco tra due, self e obj
    def attacca(self, obj):
        # attacca obj
        # se scudo divino, 0 danni
        if "sd" in self.abilities:
            self.abilities = self.abilities.replace("sd", "")
        else:
            # se no veleno, attacco normale
            if not "vl" in obj.abilities:
                self.salute -= obj.attacco
            # se veleno, morte al tocco
            else:
                self.salute = 0
        # attacca self
        # seconda parte speculare a quanto sopra
        if "sd" in obj.abilities:
            obj.abilities = obj.abilities.replace("sd", "")
        else:
            if not "vl" in self.abilities:
                obj.salute -= self.attacco
            else:
                obj.salute = 0

    # funziona rinascita, il servitore rinasce con salute pari a 1
    # t indica se il servitore è amico (f) o nemico (e)
    def reborn(self, t):
        global r, numero_r, i, nuovo_indice, array_of_deathrattles_locanda2, array_nomi_locanda2
        if t == "f":
            arr = array_personaggi_amici
            arr2 = f_array_of_taunts
        else:
            arr = array_personaggi_nemici
            arr2 = e_array_of_taunts
        # ricerca tra tutti i personaggi nell'elenco, quello avente lo stesso nome del servitore morto e ne crea una copia con uno di salute
        indice = array_nomi.index(self.nome)
        nuovo = personaggi[indice]
        self.rantoli_di_morte = nuovo.rantoli_di_morte
        self.abilities = nuovo.abilities
        self.attacco = nuovo.attacco
        self.max_salute = nuovo.salute
        self.salute = 1
        # la copia non può avere ancora rinascita
        if "rn" in self.abilities:
            self.abilities = self.abilities.replace('rn', '')
        # solo se sono stati evocati nuovi servitori dal minion stesso, la sua copia viene appesa alla destra di questi (prima di altri eventuali servitori)
        if nuovo_indice != None:
            indice = arr.index(self)
            arr.insert(nuovo_indice, arr.pop(indice))
        #se nuovo indice è None vuol dire che non sono stati evocati nuovi servitori e quindi non va appeso da alcuna parte, viene semplicemente sostituito con la copia.
        # se provocazione, viene aggiunto nella lista dei servitori amici o nemici che sia sul campo aventi provocazione
        if "pv" in self.abilities:
            arr2.append(self)


    # funzione di risettaggio della salute massima che non si aggiorna da sola istante per istante, quando la salute aumenta oltre la max la si richiama
    def salute_f(self):
        if self.salute > self.max_salute:
            self.max_salute = self.salute

    # funzione specifica per determinati servitori che incrementano le proprie o le stats di altri servitori in conseguenza di determinati eventi
    def add_stats(self, arr):
        # Iena Rovistatrice
        # se il servitore che sta morendo è una bestia, verifica se ci sono iene rovistatrici nella mia board
        if self.tipo == "Bestia":
            for element in arr:
                # la iena non deve coincidere con il servitore che sta morendo, o meglio è una bestia dunque le altre iene saranno buffate dalla sua morte ma la iena morente non può auto-buffarsi
                if element.nome == "Iena Rovistatrice" and element != self:
                    element.attacco += 2
                    element.salute += 1
                    element.salute_f()
        # Ingannatore Impulsivo

    def aggiornamento_combattimento(self):
        global conto_f, conto_e
        gf, ge = 0, 0
        for element in array_personaggi_amici:
            if element.nome == "Bucaniere Acquanera":
                gf += 1
        for element in array_personaggi_nemici:
            if element.nome == "Bucaniere Acquanera":
                ge += 1
        if gf < conto_f:
            for element in array_personaggi_amici:
                if element.tipo == "Pirata":
                    element.attacco += gf - conto_f
                    if element.attacco < 0:
                        element.attacco = 0
                    if element.salute + gf - conto_f <= 0:
                        element.salute = 1
                    else:
                        element.salute += gf - conto_f
        if ge < conto_e:
            for element in array_personaggi_nemici:
                if element.tipo == "Pirata":
                    element.attacco += ge - conto_e
                    if element.attacco < 0:
                        element.attacco = 0
                    if element.salute + ge - conto_e <= 0:
                        element.salute = 1
                    else:
                        element.salute += ge - conto_e

    def deathrattles(self, arr, element, t):
        if element == "sp":
            self.summon(t, 1, "Pirata")
        if element == "gh":
            self.health_random_buff(arr)
            print("buffato")
        if element == "s2d":
            self.summon(t, 2, "Imp")
        if element == "s1d":
            self.summon(t, 1, "Imp")
        if element == "gd":
            self.give_random_minion_divine_shield(arr)
        if element == "sg":
            self.summon(t, 1, "Golem Danneggiato")
        if element == "st":
            self.summon(t, 1, "Tartaruga")
        if element == "ba":
            self.all_minions_buff(arr)
        if element == "br":
            self.random_buff(arr)

    def summon(self, t, num, name):
        # conto_f e conto_e fanno riferimento a Bucaniere Acquanera, ma questa carta e i suoi effetti vanno rivisti, nuovo indice sarà utile dopo
        global conto_f, conto_e, nuovo_indice
        # visualizza la posizione, nella lista dei nomi di tutti i personaggi, del token in questione
        indice = array_nomi.index(name)
        if t == "f":
            arr = array_personaggi_amici
            arr2 = f_array_of_taunts
            count = conto_f
        else:
            arr = array_personaggi_nemici
            arr2 = e_array_of_taunts
            count = conto_e
        # calcola quanto spazio c'è nell'array degli amici o nemici che sia escludendo il servitore che sta per morire (per questo il -1)
        lu = len(arr) - 1
        # individua la posizione della carta in questione nell'array degli amici o nemici che sia
        indices = arr.index(self)
        # si può leggere come "se c'è uno spazio, allora...", perché se lu < 7 vuol dire che dopo che è morto il servitore ci sono al massimo 6 spazi occupati ergo almeno 1 è libero.
        if lu < 7:
            # 7 - lu è proprio il numero degli spazi liberi, per cui se questo numero è minore di quanto la carta vorrebbe evocare fai qualcosa
            if 7 - lu < num:
                # setta gli spazi liberi pari al numero di servitori evocabili
                num = 7 - lu
                array = [self]
                for i in range(num):
                    # sulla base dell'indice visto prima, crea il token avente le stats e le abilità base del token stesso (ne crea un numero pari a num)
                    if len(array_of_deathrattles[indice]) > 1:
                        raio = []
                        raio.append(array_of_deathrattles[indice][0])
                        personaggio = Personaggio(array_nomi[indice], array_tipi[indice], array_stats[indice][0],
                                                  array_stats[indice][1],
                                                  array_of_abilities[indice], raio)
                    else:
                        personaggio = Personaggio(array_nomi[indice], array_tipi[indice], array_stats[indice][0],
                                                  array_stats[indice][1],
                                                  array_of_abilities[indice], array_of_deathrattles[indice])
                    obj = personaggio
                    array.append(obj)
                    # se hanno provocazione, aggiunge nella lista
                    if "pv" in obj.abilities:
                        arr2.append(obj)
                    # Canaglia - Bucaniere
                    '''if obj.tipo == "Pirata" and count > 0:
                        obj.attacco += count
                        obj.salute += count
                        obj.salute_f()'''
                # prende l'array amici o nemici che sia e dove ci sarebbe la carta che sta per morire ci si mette l'array che contiene tutti i token, e la carta che sta per morire rimane nell'array grazie a self già presente e i token a destra
                arr[indices:indices + 1] = array
                # se ne individua la nuova posizione per la funzione rinascita se necessario, che qui corrisponde subito a destra dell'ultimo servitore creato.
                nuovo_indice = arr.index(array[len(array) - 1])
            else:
                # molto simile a prima solo che qui non c'è problema di spazi vuoti per cui num è il valore di servitori che la carta vorrebbe evocare senza limitazione alcuna
                array = [self]
                for i in range(num):
                    if len(array_of_deathrattles[indice]) > 1:
                        raio = []
                        raio.append(array_of_deathrattles[indice][0])
                        personaggio = Personaggio(array_nomi[indice], array_tipi[indice], array_stats[indice][0],
                                                  array_stats[indice][1],
                                                  array_of_abilities[indice], raio)
                    else:
                        personaggio = Personaggio(array_nomi[indice], array_tipi[indice], array_stats[indice][0],
                                                  array_stats[indice][1],
                                                  array_of_abilities[indice], array_of_deathrattles[indice])
                    obj = personaggio
                    array.append(obj)
                    if "pv" in obj.abilities:
                        arr2.append(obj)
                    '''if obj.tipo == "Pirata" and count > 0:
                        obj.attacco += count
                        obj.salute += count
                        obj.salute_f()'''
                arr[indices:indices + 1] = array
                nuovo_indice = arr.index(array[len(array) - 1])

    def all_minions_buff(self, arr):
        #dà a tutti i servitori diversi da self +1/+1 pertanto è anche richiamata la funzione salute_f che vuole ripristinare la max_health se necessario.
        for element in arr:
            if element != self:
                element.attacco += 1
                element.salute += 1
                element.salute_f()

    def random_buff(self, arr):
        raio = arr[:]
        for element in raio:
            if element.tipo != "Bestia" or element.salute <= 0:
                raio.remove(element)
        if len(raio) > 0:
            elemento = random.choice(raio)
            elemento.attacco += 1
            elemento.salute += 1
            elemento.salute_f()
            elemento.rantoli_di_morte .append('br')
            #print(elemento.nome + ' ' + str(arr.index(elemento)), elemento.rantoli_di_morte)

    def health_random_buff(self, arr):
        #fa una copia dell'array amici o nemici che sia e elimina i servitori che siano morti o debbano esserlo oltre a self.
        #se tale array ha almeno un minion, dà health a un minion scelto randomicamente tra quelli
        raio = arr[:]
        for element in raio:
            if element == self or element.salute <= 0:
                raio.remove(element)
        if len(raio) > 0:
            elemento = random.choice(raio)
            elemento.salute += self.max_salute
            elemento.salute_f()

    def give_random_minion_divine_shield(self, arr):
        #fa una copia dell'array amici o nemici che sia e ne elimina i minion che abbiano già scudo divino e quelli che sono morti o dovrebbero esserlo.
        #se tale array ha almeno un minion, dà scudo divino a un minion scelto randomicamente tra quelli
        raio = arr[:]
        for element in raio:
            if element.salute <= 0 or "sd" in element.abilities:
                raio.remove(element)
        if len(raio) > 0:
            elemento = random.choice(raio)
            elemento.abilities = elemento.abilities + "sd"

    def Triggera_rantolo_di_morte(self, arr, t):
        raio = arr[:]
        for element in raio:
            if element == self or element.rantoli_di_morte == []:
                raio.remove(element)
        if len(raio) > 0:
            elemento = random.choice(raio)
            copia = elemento.rantoli_di_morte[:]
            for element in copia:
                elemento.deathrattles(arr, element, t)

    # solita variabile t che indica se il servitore che muore è amico o meno + variabile s che specifica le situazioni in cui il servitore a morire è quello attaccato, se s è None, è morto il servitore che ha attaccato, altrimenti quello che è stato attaccato
    def morte(self, t, s=None):
        global numero_r, i, value, r, nuovo_indice
        nuovo_indice = None
        if t == "f":
            arr = array_personaggi_amici
            # prs = arr[i]
            or_len = len(arr)
            if "pv" in self.abilities:
                f_array_of_taunts.remove(self)
        else:
            arr = array_personaggi_nemici
            # prs = arr[r]
            or_len = len(arr)
            if "pv" in self.abilities:
                e_array_of_taunts.remove(self)
        # possibili rantoli di morte del servitore, da rivedere in futuro
        for element in self.rantoli_di_morte:
            self.deathrattles(arr, element, t)
        # se dopo i rantoli di morte vi sono 7 servitori o meno (anche 7 dato che non si è ancora rimosso il servitore morto) e il servitore morto ha rinascita, funzione rinascita, nota che nella funzione rinascita c'è già la rimozione del servitore morto per cui se non viene richiamata tale funziona, va eliminato manualmente il servitore
        if len(arr) <= 7 and "rn" in self.abilities:
            self.reborn(t)
            self.aggiornamento_combattimento()
        else:
            # per via di quanto sopra espresso
            arr.remove(self)
        # qui si modifica l'ordine di combattimento dopo la morte del servitore (sono ovviamente solo i casi in cui il servitore morto è quello attaccato)
        # speculare a quanto sotto
        if t == "f" and s != None:
            if numero_r < i:
                if i > 0:
                    i += len(arr) - or_len
        if t == "e" and s != None:
            # numero r indica la posizione del servitore attaccato, r la posizione del servitore che attaccherà
            # interessa solo se viene ucciso un servitore che aveva già attaccato o la cui posizione è inferiore a quello che attaccherà perché in caso contrario l'ordine non cambia
            if numero_r < r:
                if r > 0:
                    r += len(arr) - or_len
array_nomi, array_stats, array_of_deathrattles, array_tipi, array_of_abilities, personaggi, array_of_deathrattles_locanda2, array_nomi_locanda2 = [], [], [], [], [], [], [], []
def Fulfill_Array_Start():
    global array_nomi, array_stats, array_of_deathrattles, array_tipi, personaggi, array_of_abilities, array_of_deathrattles_locanda2, array_nomi_locanda2
    array_nomi_tokens_locanda1 = ["Pirata", "Gatto Soriano", "Imp", "Murloc Esploratore", "Elementale"]
    array_tipi_tokens_locanda1 = ["Pirata", "Bestia", "Demone", "Murloc", "Elementale"]
    array_stats_tokens_locanda1 = [(1, 1), (1, 1), (1, 1), (1, 1), (2, 2)]
    array_of_abilities_tokens_locanda1 = ["", "", "", "", ""]
    array_of_deathrattles_tokens_locanda1 = [[], [], [], [], []]
    personaggi_tokens_locanda1 = []
    for i in range(len(array_nomi_tokens_locanda1)):
        personaggio = Personaggio(array_nomi_tokens_locanda1[i], array_tipi_tokens_locanda1[i],
                                  array_stats_tokens_locanda1[i][0], array_stats_tokens_locanda1[i][1],
                                  array_of_abilities_tokens_locanda1[i], array_of_deathrattles_tokens_locanda1[i])
        personaggi_tokens_locanda1.append(personaggio)
    array_nomi_tokens_locanda2 = ["Golem Danneggiato", "Tartaruga"]
    array_tipi_tokens_locanda2 = ["Robot", "Bestia"]
    array_stats_tokens_locanda2 = [(2, 1), (2, 3)]
    array_of_abilities_tokens_locanda2 = ["", "pv"]
    array_of_deathrattles_tokens_locanda2 = [[], []]
    personaggi_tokens_locanda2 = []
    for i in range(len(array_nomi_tokens_locanda2)):
        personaggio = Personaggio(array_nomi_tokens_locanda2[i], array_tipi_tokens_locanda2[i],
                                  array_stats_tokens_locanda2[i][0], array_stats_tokens_locanda2[i][1],
                                  array_of_abilities_tokens_locanda2[i], array_of_deathrattles_tokens_locanda2[i])
        personaggi_tokens_locanda2.append(personaggio)
    def personaggimm():
        array_nomi_locanda1 = ["Accolito di C'thun", "Alacromatica Evolutiva", "Anomalia Ristoratrice",
                               "Cacciatore Pozzaroccia", "Canaglia", "Draghetto Rosso", "Gatto Randagio", "Geomante Lamaspina",
                               "Iena Rovistatrice", "Imp Rivoltante", "Ingannatore Impulsivo", "Mozzo del Mazzo",
                               "Mummia in Miniatura", "Murloc Cacciamaree", "Robocucciolo", "Tessitore dell'Ira",
                               "Vendimentale", "Verrospino Abbronzato"]
        array_tipi_locanda1 = [None, "Drago", "Elementale", "Murloc", "Pirata", "Drago", "Bestia", "Verrospino", "Bestia",
                               "Demone", "Demone", "Pirata", "Robot", "Murloc", "Robot", None, "Elementale", "Verrospino"]
        array_stats_locanda1 = [(2, 2), (1, 3), (1, 4), (2, 3), (3, 1), (1, 2), (1, 1), (3, 1), (2, 2), (1, 1), (2, 2), (2, 2),
                                (1, 2), (2, 1), (2, 1), (1, 3), (2, 2), (1, 2)]
        array_of_abilities_locanda1 = ["pvrn", "", "", "", "", "", "", "", "", "", "", "", "rn", "", "sd", "", "", ""]
        array_of_deathrattles_locanda1 = [[], [], [], [], ['sp'], [], [], [], [], ['s2d'], ['gh'], [], [], [], [], [], [], []]
        personaggi_locanda1 = [Personaggio(nomi, tipi, stats[0], stats[1], abilities, deathrattles) for nomi, tipi, stats, abilities, deathrattles in zip(array_nomi_locanda1, array_tipi_locanda1, array_stats_locanda1, array_of_abilities_locanda1, array_of_deathrattles_locanda1)]

    array_nomi_locanda2 = ["Belva Zannaferrea", "Bucaniere Acquanera", "Campionessa Altruista", "Carceriere",
                           "Cinghiale di Strada", "Comandante Nathrezim", "Condottiero Murloc", "Elementale della Festa",
                           "Ghoul Instabile", "Golem Mietitore", "Grande Capo Scagliafine", "Guardiano dei Glifi",
                           "Maxi-Robobomba", "Profeta dei Cinghiali", "Prole di N'zoth", "Rana Salterina",
                           "Ratto delle Fogne", "Roccia Fusa", "Saurolisco Rabbioso", "Scommettitrice Incallita",
                           "Tazza del Serraglio", "Trafficante di Draghetti", "Vecchio Occhiobuio", "Yo-Ho-Ogre",
                           "Zannatosta", "Macao"]
    array_tipi_locanda2 = ["Robot", "Pirata", None, "Demone", "Verrospino", "Demone", "Murloc", "Elementale", None, "Robot",
                           "Murloc", "Drago", "Robot", None, None, "Bestia", "Bestia", "Elementale", "Bestia", "Pirata",
                           None, None, "Murloc", "Pirata", "Verrospino", "Bestia"]
    array_stats_locanda2 = [(3, 3), (3, 3), (2, 1), (3, 3), (2, 4), (2, 4), (3, 3), (3, 2), (1, 3), (2, 3), (3, 2), (2, 4),
                            (2, 2), (3, 3), (2, 2), (3, 3), (3, 2), (2, 4), (3, 2), (3, 3), (2, 2), (2, 5), (2, 4), (3, 5),
                            (5, 3), (4, 4)]
    array_of_abilities_locanda2 = ["", "", "", "pv", "", "", "", "", "pv", "", "", "", "", "", "", "",
                                   "", "pv", "", "", "", "", "", "pv", "", ""]
    array_of_deathrattles_locanda2 = [[], [], ['gsd'], ['s1d'], [], [], [], [], ['da'], ['sg'], [], [], ['dr'], [], ['ba'], ['br'], ['st'],
                                      [], [], [], [], [], [], [], [], []]
    personaggi_locanda2 = []
    for i in range(len(array_nomi_locanda2)):
        personaggio = Personaggio(array_nomi_locanda2[i], array_tipi_locanda2[i], array_stats_locanda2[i][0],
                                  array_stats_locanda2[i][1], array_of_abilities_locanda2[i], array_of_deathrattles_locanda2[i])
        personaggi_locanda2.append(personaggio)
    array_nomi = array_nomi_tokens_locanda1 + array_nomi_tokens_locanda2 + array_nomi_locanda1 + array_nomi_locanda2
    array_tipi = array_tipi_tokens_locanda1 + array_tipi_tokens_locanda2 + array_tipi_locanda1 + array_tipi_locanda2
    array_stats = array_stats_tokens_locanda1 + array_stats_tokens_locanda2 + array_stats_locanda1 + array_stats_locanda2
    array_of_abilities = array_of_abilities_tokens_locanda1 + array_of_abilities_tokens_locanda2 + array_of_abilities_locanda1 + array_of_abilities_locanda2
    array_of_deathrattles = array_of_deathrattles_tokens_locanda1 + array_of_deathrattles_tokens_locanda2 + array_of_deathrattles_locanda1 + array_of_deathrattles_locanda2
    personaggi = personaggi_tokens_locanda1 + personaggi_tokens_locanda2 + personaggi_locanda1 + personaggi_locanda2

taunt = None
nuovo_indice = None
personaggio_momentaneo_f = None
personaggio_momentaneo_e = None
count_lose = 0
count_tie = 0
count_win = 0
count_eccezioni = 0
i = 0
r = 0
numero_r = 0
conto_f = 0
conto_e = 0
value = -1
array_personaggi_amici = []
array_personaggi_nemici = []
f_array_of_taunts = []
e_array_of_taunts = []


def inizio_combattimento():
    global conto_f, conto_e
    conto_f = 0
    conto_e = 0
    for element in array_personaggi_amici:
        if element.nome == "Bucaniere Acquanera":
            conto_f += 1
    for element in array_personaggi_nemici:
        if element.nome == "Bucaniere Acquanera":
            conto_e += 1
    if conto_f > 0:
        for element in array_personaggi_amici:
            if element.tipo == "Pirata":
                if element.nome != "Bucaniere Acquanera":
                    element.attacco += conto_f
                    element.salute += conto_f
                    element.salute_f()
                else:
                    element.attacco += conto_f - 1
                    element.salute += conto_f - 1
                    element.salute_f()
    if conto_e > 0:
        for element in array_personaggi_nemici:
            if element.tipo == "Pirata":
                if element.nome != "Bucaniere Acquanera":
                    element.attacco += conto_e
                    element.salute += conto_e
                    element.salute_f()
                else:
                    element.attacco += conto_e - 1
                    element.salute += conto_e - 1
                    element.salute_f()


# funzione di riempimento array amici e nemici
def Fulfill_Arrays():
    global array_personaggi_amici, array_personaggi_nemici, f_array_of_taunts, e_array_of_taunts, personaggi_locanda1, array_nomi_locanda1, array_stats_locanda1, array_of_abilities_locanda1, array_nomi, array_salute, array_attacco, array_of_abilities
    array_personaggi_amici = []
    array_personaggi_nemici = []
    f_array_of_taunts = []
    e_array_of_taunts = []
    # visualizza i nomi dei servitori scritti da me e li ricerca nell'array con tutti i nomi ufficiali dei servitori, restituendo la posizione in quell'array (indice è quella posizione) poi usa quell'indice per trovare anche stats, abilità, tipo del servitore
    for i in range(len(nomi_array[0])):
        indice = array_nomi.index(nomi_array[0][i])
        personaggio = Personaggio(array_nomi[indice], array_tipi[indice], array_stats[indice][0],
                                  array_stats[indice][1],
                                  array_of_abilities[indice], array_of_deathrattles[indice])
        array_personaggi_amici.append(personaggio)
    # quanto sopra però per i servitori nemici
    for i in range(len(nomi_array[1])):
        indice = array_nomi.index(nomi_array[1][i])
        personaggio = Personaggio(array_nomi[indice], array_tipi[indice], array_stats[indice][0],
                                  array_stats[indice][1],
                                  array_of_abilities[indice], array_of_deathrattles[indice])
        array_personaggi_nemici.append(personaggio)
    # stats_array[0] contiene le stats di tutte le carte amiche, per cui va in loop con ogni elemento in modo da settare l'attacco dei personaggi amici pari a quanto scritto nell'array, similmente per le abilità per cui si aggiunge la variabile indice utile in quanto diverso l'ordine e la lunghezza di quell'array (non si può usare i)
    for i in range(len(stats_array[0])):
        indice = array_nomi.index(array_personaggi_amici[i].nome)
        array_personaggi_amici[i].attacco = stats_array[0][i][0]
        array_personaggi_amici[i].salute = stats_array[0][i][1]
        array_personaggi_amici[i].max_salute = array_personaggi_amici[i].salute
        array_personaggi_amici[i].abilities = array_of_abilities[indice] + abilities_array[0][i]
        array_personaggi_amici[i].rantoli_di_morte = array_of_deathrattles[indice] + deathrattles_array[0][i]
    # simile a quanto sopra, ma per i nemici
    for i in range(len(stats_array[1])):
        indice = array_nomi.index(array_personaggi_nemici[i].nome)
        array_personaggi_nemici[i].attacco = stats_array[1][i][0]
        array_personaggi_nemici[i].salute = stats_array[1][i][1]
        array_personaggi_nemici[i].max_salute = array_personaggi_nemici[i].salute
        array_personaggi_nemici[i].abilities = array_of_abilities[indice] + abilities_array[1][i]
        array_personaggi_nemici[i].rantoli_di_morte = array_of_deathrattles[indice] + deathrattles_array[1][i]
    # se provocazione aggiunge nelle liste dei servitori con provocazione
    for element in array_personaggi_amici:
        if "pv" in element.abilities:
            f_array_of_taunts.append(element)
    for element in array_personaggi_nemici:
        if "pv" in element.abilities:
            e_array_of_taunts.append(element)

def board():
    bib_f = []
    bib_e = []
    for element in array_personaggi_amici:
        bib_f.append(element.nome + ' ' + str(element.attacco) + ' ' + str(
            element.salute) + ' ' + str(element.max_salute) + ' ' + str(element.abilities))
    for element in array_personaggi_nemici:
        bib_e.append(element.nome + ' ' + str(element.attacco) + ' ' + str(
            element.salute) + ' ' + str(element.max_salute) + ' ' + str(element.abilities))
    return bib_f, bib_e



# funzione di attacco del mio servitore al servitore nemico
def P_vs_E():
    global i, r, taunt, value, numero_r, personaggio_momentaneo_f, personaggio_momentaneo_e
    start = 3
    repeat = True
    add_1 = False
    if "fv" in array_personaggi_amici[i].abilities:
        start = 2
    if "sfv" in array_personaggi_amici[i].abilities:
        start = 0
    for n in range(start, 4):
        if not repeat or len(array_personaggi_nemici) == 0:
            break
        # se non ci sono servitori nemici con provocazione, scegline uno randomicamente (numero r ne indica la posizione)
        if len(e_array_of_taunts) == 0:
            numero_r = random.randrange(0, len(array_personaggi_nemici))
        # se ci sono scegli tra essi randomicamente, taunt è il personaggio, numero_r la posizione
        else:
            taunt = random.choice(e_array_of_taunts)
            numero_r = array_personaggi_nemici.index(taunt)
        elemento_casuale = array_personaggi_nemici[numero_r]
        print('\n' + array_personaggi_amici[i].nome + ' ' + str(array_personaggi_amici[i].attacco) + ' ' + str(
            array_personaggi_amici[i].salute) + ' ' + str(array_personaggi_amici[i].max_salute) + ' ' + str(array_personaggi_amici[i].abilities) + " (" + str(
            i) +  ")" + " ha lottato con " + elemento_casuale.nome + ' ' + str(elemento_casuale.attacco) + ' ' + str(
            elemento_casuale.salute) + ' ' + str(elemento_casuale.max_salute) + ' ' + str(elemento_casuale.abilities) + " (" + str(numero_r) + ")" + '\n')
        for elemento in array_personaggi_amici:
            print(elemento.nome + ' , posizione ' + str(array_personaggi_amici.index(elemento)) + ' ' + str(elemento.rantoli_di_morte))
        print("Vediamo ora i nemici")
        for elemento in array_personaggi_nemici:
            print(elemento.nome + ' , posizione ' + str(array_personaggi_nemici.index(elemento)) + ' ' + str(elemento.rantoli_di_morte))
        array_personaggi_amici[i].attacca(elemento_casuale)
        if array_personaggi_amici[i].nome == "Macao":
            array_personaggi_amici[i].Triggera_rantolo_di_morte(array_personaggi_amici, "f")
        # se il mio servitore attaccando muore, l'ordine di attacco rimane invariato (+1 ma muore, quindi -1 ergo +0), vai comunque nella funzione morte
        if array_personaggi_amici[i].salute <= 0:
            repeat = False
            array_personaggi_amici[i].morte("f")
            if i >= len(array_personaggi_amici):
                i = 0
        # se non muore dovresti aggiungere 1 all'ordine di attacco, ma aspetta che attacchi l'avversario per cui intanto rendi la variabile add_1 vera
        else:
            if not "fv" in array_personaggi_amici[i].abilities:
                personaggio_momentaneo_f = array_personaggi_amici[i]
                i += 1
                if i >= len(array_personaggi_amici):
                    i = 0
        # se muore il servitore nemico quando il mio servitore attacca, funzione morte in cui cambierà l'ordine di attacco
        if array_personaggi_nemici[numero_r].salute <= 0:
            # solo se il personaggio amico morto non è quello che aveva appena attaccato aggiungi 1 (che si sarebbe dovuto aggiungere prima, ma si è aspettato attaccasse il nemico)
            if personaggio_momentaneo_e == array_personaggi_nemici[numero_r]:
                r -= 1
            array_personaggi_nemici[numero_r].morte("e", "f")
            if r >= len(array_personaggi_nemici):
                r = 0
            if i >= len(array_personaggi_amici):
                i = 0
        print(board())
        personaggio_momentaneo_e = None


# funzione di attacco del servitore nemico al mio servitore, speculare a quanto visto sopra
def E_vs_P():
    global i, r, taunt, value, numero_r, personaggio_momentaneo_f, personaggio_momentaneo_e
    start = 3
    repeat = True
    if "fv" in array_personaggi_nemici[r].abilities:
        start = 2
    if "sfv" in array_personaggi_nemici[r].abilities:
        start = 0
    for n in range(start, 4):
        if not repeat or len(array_personaggi_amici) == 0:
            break
        if len(f_array_of_taunts) == 0:
            numero_r = random.randrange(0, len(array_personaggi_amici))
        else:
            taunt = random.choice(f_array_of_taunts)
            numero_r = array_personaggi_amici.index(taunt)
        elemento_casuale = array_personaggi_amici[numero_r]
        print('\n' + array_personaggi_nemici[r].nome + ' ' + str(array_personaggi_nemici[r].attacco) + ' ' + str(
            array_personaggi_nemici[r].salute) + ' ' + str(array_personaggi_nemici[r].max_salute) + ' ' + str(array_personaggi_nemici[r].abilities) + " (" + str(
            r) + ')' + " ha lottato con " + elemento_casuale.nome + ' ' + str(elemento_casuale.attacco) + ' ' + str(
            elemento_casuale.salute) + ' ' + str(elemento_casuale.max_salute) + ' ' + str(elemento_casuale.abilities) +  ' (' + str(numero_r) + ')' + '\n')
        for elemento in array_personaggi_amici:
            print(elemento.nome + ' , posizione ' + str(array_personaggi_amici.index(elemento)) + ' ' + str(elemento.rantoli_di_morte))
        print("Vediamo ora i nemici")
        for elemento in array_personaggi_nemici:
            print(elemento.nome + ' , posizione ' + str(array_personaggi_nemici.index(elemento)) + ' ' + str(elemento.rantoli_di_morte))
        array_personaggi_nemici[r].attacca(elemento_casuale)
        if array_personaggi_nemici[r].nome == "Macao":
            array_personaggi_nemici[r].Triggera_rantolo_di_morte(array_personaggi_nemici, "e")
        if array_personaggi_nemici[r].salute <= 0:
            repeat = False
            array_personaggi_nemici[r].morte("e")
            if r >= len(array_personaggi_nemici):
                r = 0
        else:
            if not "fv" in array_personaggi_nemici[r].abilities:
                personaggio_momentaneo_e = array_personaggi_nemici[r]
                r += 1
                if r >= len(array_personaggi_nemici):
                    r = 0
        if array_personaggi_amici[numero_r].salute <= 0:
            # solo se il personaggio amico morto è quello che aveva appena attaccato togli 1, perché è come se non avesse ancora attaccato se muore prima di switchare attaccante
            if personaggio_momentaneo_f == array_personaggi_amici[numero_r]:
                i -= 1
            array_personaggi_amici[numero_r].morte("f", "e")
            if i >= len(array_personaggi_amici):
                i = 0
        print(board())
        personaggio_momentaneo_f = None


domanda = input("Vuoi partire dagli array già scritti? ")
if "s" not in domanda:
    Variables.ask_array(array_nomi)
numero = Variables.number
nomi_array = Variables.array_nomi_p
stats_array = Variables.array_stats_p
abilities_array = Variables.array_of_abilities_p
deathrattles_array = Variables.array_of_deathrattles_p
for j in range(numero):
    i, r = 0, 0
    nomi_array = Variables.array_nomi_p
    stats_array = Variables.array_stats_p
    abilities_array = Variables.array_of_abilities_p
    deathrattles_array = Variables.array_of_deathrattles_p
    Fulfill_Array_Start()
    Fulfill_Arrays()
    inizio_combattimento()
    if len(array_personaggi_nemici) > len(array_personaggi_amici):
        first_player = 1
    elif len(array_personaggi_nemici) < len(array_personaggi_amici):
        first_player = 0
    else:
        first_player = random.randrange(0, 2)
    count = 0
    print("Inizio Partita")
    # print(first_player, "lol")
    while len(array_personaggi_nemici) > 0 and len(array_personaggi_amici) > 0:
        '''for element in array_personaggi_amici:
            print(element.nome, element.attacco, element.salute, element.abilities)
        for element in array_personaggi_nemici:
            print(element.nome, element.attacco, element.salute, element.abilities)'''
        if first_player == 0:
            P_vs_E()
            if not (len(array_personaggi_nemici) > 0 and len(array_personaggi_amici) > 0):
                break
            E_vs_P()
        else:
            E_vs_P()
            if not (len(array_personaggi_nemici) > 0 and len(array_personaggi_amici) > 0):
                break
            P_vs_E()
        '''for element in array_personaggi_amici:
            print(element.nome, element.attacco, element.salute, element.abilities)
        for element in array_personaggi_nemici:
            print(element.nome, element.attacco, element.salute, element.abilities)'''
    if len(array_personaggi_amici) == 0 and len(array_personaggi_nemici) > 0:
        count_lose += 1
        print("Lost")
    elif len(array_personaggi_amici) > 0 and len(array_personaggi_nemici) == 0:
        count_win += 1
        print("Won")
    elif len(array_personaggi_amici) == 0 and len(array_personaggi_nemici) == 0:
        count_tie += 1
        print("Tied")

print(count_win, count_tie, count_lose)
win_prob = float((count_win / numero) * 100)
tie_prob = float((count_tie / numero) * 100)
lose_prob = float((count_lose / numero) * 100)

print(win_prob, tie_prob, lose_prob)
print('array_nomi_p = ' + str(nomi_array))
print('array_stats_p = ' + str(stats_array))
print('array_of_abilities_p = ' + str(abilities_array))
print('array_of_deathrattles_p = ' + str(deathrattles_array))
# print(count_eccezioni)
