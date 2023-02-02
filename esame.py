# classe per le eccezioni
class ExamException(Exception):
    pass


# creo la classe principale CSVTimeSeriesFile
class CSVTimeSeriesFile():
   
    # inizializzo sul nome del file inserito
    def __init__(self, name):
        self.name = name

    #-=-=-=-=-=-=-#
    #  GET_DATA   #
    #-=-=-=-=-=-=-#
    def get_data(self):

        # controllo la correttezza del nome del file
        if self.name == ''  or  self.name == None :
            raise ExamException('Errore: nessun file inserito.')
        if type(self.name) != str:
            raise ExamException('Errore: nome del file inserito non valido.')
            
        # provo a leggere il file
        try:
            controllo_file = open(self.name, 'r')
            controllo_file.readline()
        except Exception as e1:
            raise ExamException('Errore: non è stato possibile leggere il file {}'.format(e1))


        # creo una lista di liste con gli elementi del file inserito
        lista_di_liste = []
        with open(self.name) as file1:

            # questa variabile aiuta a capire se il file è vuoto o se contiene tutti elementi non validi
            # se contatore > 0 e lista_di_liste == [], allora il file non è vuoto ma non contiene alcun elemento valido
            contatore = 0
            for line in file1:
                
                # separo ogni riga per la virgola
                elementi = line.strip('\n').split(',')

                # faccio un cast di tutti gli elementi a int e float
                # come precisato nel testo dell'esame, ignoro valori non numerici
            
                # prima faccio cast di epoch
                try:
                    elementi[0] = float(elementi[0])
                    elementi[0] = int(elementi[0])
                except:   
                    contatore += 1
                    continue

                # infine faccio cast di temperature
                try:
                    elementi[1] = float(elementi[1])
                except:
                    contatore += 1
                    continue

                #creo una lista con solo le prime due colonne
                #primi_due_elementi = [elementi[0], elementi[1]]
                    
                lista_di_liste.append([elementi[0], elementi[1]])

                
        # se la lista_di_liste è vuota e contatore = 0, significa che il file è vuoto
        if lista_di_liste == [] and contatore == 0:
            raise ExamException('Errore: il file inserito è vuoto')
        else:
            pass

                       
        for i in range(len(lista_di_liste)):
            for j in range(len(lista_di_liste)):

                # controllo se ci sono duplicati
                if i != j:
                    if (lista_di_liste[i][0] == lista_di_liste[j][0]) and (lista_di_liste[i][0] != ''):
                        raise ExamException('Errore: il timestamp {} è presente più volte'.format(lista_di_liste[i][0]))
                
                # controllo se le timestamp sono ordinate cronologicamente
                if i < j:

                    if lista_di_liste[i][0] > lista_di_liste[j][0]:
                        raise ExamException('Errore: la serie temporale nel file non è ordinata:\nriga {}, {} > riga {}, {}'.format(i+1, lista_di_liste[i][0], j+1, lista_di_liste[j][0]))

          
                        
        return lista_di_liste


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
# COMPUTE_DAILY_MAX_DIFFERENCE  #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
def compute_daily_max_difference(time_series):

    lista_differenze = []
    # la lista tmp contiene tutti i valori di un giorno e viene azzerata dopo ogni giorno
    tmp = []
   
    for i in range(len(time_series)):  

        if (i+1) != len(time_series):
        
            epoch_corrente = time_series[i][0]
            epoch_successivo = time_series[i+1][0]  

            # converto epoch in giorni e ottengo il giorno corrente e quello successivo
            giorno_corrente = epoch_corrente - (epoch_corrente % 86400)
            giorno_successivo = epoch_successivo - (epoch_successivo % 86400)

            # aggiungo a tmp tutti i valori appartenenti allo stesso giorno
            if giorno_corrente == giorno_successivo:
                tmp.append(time_series[i][1])
                
            # se l'elemento successivo non appartiene allo stesso giorno
            # calcolo max e min e infine la differenza
            else:
                tmp.append(time_series[i][1])

                if len(tmp) == 1:
                    # se questo è l'unico elemento della giornata, aggiungo None
                    lista_differenze.append(None)
                    tmp = []
                else:
                    for j in range(len(tmp)):
                        # "inizializzo" max e min alla prima iterazione
                        if j == 0:
                            massimo = tmp[j]
                            minimo = tmp[j]
                            continue
    
                        # confronto con max e min
                        if tmp[j] > massimo:
                            massimo = tmp[j]
                        if tmp[j] < minimo:
                            minimo = tmp[j]
                            
                    # siccome python presenta un bug per il calcolo tra float, devo usare round()
                    # calcolo e aggiungo la differenza
                    lista_differenze.append(round(massimo-minimo, 3))
                    tmp = []

        # questa parte viene eseguita quando si arriva all'ultimo elemento di time_series
        else:  
            
            tmp.append(time_series[i][1])
            
            # se temperature di questa riga non appartiene ad altri giorni,
            # quindi è l'unico per un determinato giorno, aggiungo None alla lista finale
            if len(tmp) == 1:
                lista_differenze.append(None)
                tmp = []
            # altrimenti faccio il solito calcolo e finisco
            else:
                for j in range(len(tmp)):
                    if j == 0:
                        massimo = tmp[j]
                        minimo = tmp[j]
                        continue
    
                    if tmp[j] > massimo:
                        massimo = tmp[j]
                    if tmp[j] < minimo:
                        minimo = tmp[j]

                lista_differenze.append(round(massimo-minimo, 3))
                tmp = []
        
        
    return lista_differenze
               
        
#####################################################

#time_series_file = CSVTimeSeriesFile(name='data.csv')
#time_series = time_series_file.get_data()
#print(time_series)
#print(compute_daily_max_difference(time_series))
#risultato = compute_daily_max_difference(time_series)
#for i in risultato:
#    print(i)