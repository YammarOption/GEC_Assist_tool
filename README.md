# G.E.T - GET EVERYTHING TRACKER
Il GET è uno strumento grafico per tenere traccia dei progressi fatti durante la "Get Everything Challenge" in Pokémon. Lo strumento permette di monitorare facilmente i progressi nel gioco senza doverli memorizzare ed è progettato per fungere da cornice per il gioco, avendo un foro centrale dove posizionare il gioco, e consentendo di ridimensionare i bordi per coprire ciò che rimane scoperto. Una volta posizionato, è possibile utilizzare il pulsante ``blocco`` per ancorare lo strumento in modo che rimanga in primo piano e non scompaia cliccando fuori dalla finestra.

Lo strumento consente di controllare tutti i seguenti requisiti, necessari per completare la sfida GEC:

### 1. Tutti i Pokémon
![image](/img/Main_bar_1.png)

Il primo requisito della sfida è **catturare tutti i Pokémon** nel dex regionale e ottenere un *living dex*. Lo strumento consente agli utenti di monitorare facilmente i progressi offrendo una tabella con tutti i Pokémon presenti nel dex e un contatore nell'angolo in alto a destra dell'interfaccia grafica. Cliccando sull'icona di un Pokémon si cambia il suo colore tra tre possibilità:
1. **Grigio**: Pokémon non ancora catturato
2. **Colorato**: Pokémon catturato e presente nel living dex
3. **Blu**: Pokémon che sarà presto ottenuto (es. tramite evoluzione, scambio, ecc.)

![image](/img/Dex.png)

### 2. Tutti gli Strumenti
![image](/img/Main_bar_2.png)

Il secondo traguardo per completare la sfida è ottenere **ogni singolo oggetto** nel gioco.

Questa funzionalità è accompagnata dal Route Tracker, che mostra i progressi per ogni percorso, inclusi gli oggetti presenti. Gli oggetti contrassegnati con *(H)* sono nascosti, mentre altri oggetti visibili in mappa.

Il numero totale di oggetti visualizzati è calcolato come *la somma di tutti gli oggetti raccoglibili più uno per ciascun oggetto acquistabile esclusivamente*.

### 3. Tutti gli Allenatori
![image](/img/Main_bar_3.png)

Il terzo obiettivo della sfida è **sfidare ogni allenatore** nel gioco. Questo include anche le lotte opzionali e quelle mancabili. Le lotte accessibili solo tramite glitch non contano.

Lo strumento consente, tramite il Route Tracker, di vedere tutti gli allenatori in ogni piano di un percorso insieme alle loro squadre, per contrassegnare facilmente quelli già sconfitti rispetto a quelli mancanti. Selezionando un allenatore, il contatore aumenterà automaticamente, mentre deselezionandolo il contatore diminuirà. Gli allenatori con squadre multiple (es. rivali) sono conteggiati come una singola istanza, sebbene tutte le loro squadre possibili siano mostrate.

### 4. Tutte le Mosse
![image](/img/Main_bar_4.png)

Il quarto requisito è **vedere almeno una volta tutte le mosse** nel gioco, Lotta compresa. Lo strumento offre un elenco pratico a sinistra del Route Tracker sulla destra con una lista di controllo per tutte le mosse, che aumenterà automaticamente il contatore.

<img src="img/Move_list.png" width="150"/>

Una volta contrassegnata una mossa, essa scompare dall'elenco e riappare in un secondo elenco in basso, contrassegnata in verde. Da questo secondo elenco è possibile deselezionare una mossa per farla riapparire nell'elenco delle mosse non contrassegnate.

### 5. Tutte le Altre Cose
![image](/img/Main_bar_5.png)

L'ultima categoria raggruppa tutti gli elementi rimanenti che devono essere completati. Questo gruppo include elementi come:
- Interagire con tutti i Pokémon fissi (come Snorlax o Voltorb trappola)
- Completare tutti gli scambi in-game
- Ottenere tutti i Pokémon regalati. I Pokémon di questa categoria includono anche quelli acquistati (come Magikarp), ma non quelli ottenuti al casinò, poiché questi sono ripetibili.
- Se sono presenti le slot machine nel gioco, ottenere almeno una volta un **777** o il suo equivalente.

## Finestra del Route Tracker
La finestra del Route Tracker è un elemento secondario che si apre insieme alla GUI principale. Questa finestra mostra un elenco statico con tutte le mosse e, per un percorso selezionato, tutti gli oggetti, allenatori ed eventi raggruppati per la loro posizione nella mappa. Tutti gli elementi sono mostrati insieme a una casella di controllo per segnarli come completati/ottenuti e aumentare il contatore corrispondente.

Nella parte superiore della finestra è presente una combobox, per cambiare facilmente il percorso attualmente visualizzato. I percorsi sono presentati in ordine alfanumerico.

![image](/img/route_explorer.png)

## Salvare e cancellare dati
Lo strumento salva automaticamente i dati una volta chiusa una delle due finestre principali. Per eliminare tutti i dati è possibile:
1. Deselezionare tutto
2. Eliminare il file ``Datapack/data.json`` che tiene traccia dei progressi.

## Differenze tra versioni:
Al momento sono disponibili due versioni diverse dello strumento GEC Assist. Le loro differenze risiedono in come è presentato il layout:
- La versione regolare offre un layout per Pokédex e oggetti che è espandibile e scorrevole, con le icone che si allineano per occupare lo spazio disponibile.
- La versione *Stream* invece utilizza un layout fisso, che non si adatta alle dimensioni della finestra ma non ha aree scorrevoli, lasciando tutte le icone visibili contemporaneamente.

Per alternare la versione da utilizzare, cambiala dal file Config.ini.

## Personalizzazione:
Il GET consente di tenere traccia dei progressi per giochi diversi. Per cambiare correttamente da un gioco all'altro è necessario un ``Datapack``. Per installare un datapack, basta scaricarlo e posizionare la cartella vicino al file eseguibile. Inoltre, per una migliore integrazione, è possibile modificare il file ``Config.ini`` e cambiare il valore ``Gen`` in uno degli disponibili.

## Crediti
- **LetalStrems** (https://www.twitch.tv/letalstreams) per lo sviluppo della sfida e delle sue regole
- **PMDCollab SpriteCollab** (https://sprites.pmdcollab.org/) per i ritratti dei Pokémon usati nel Pokédex
- **DougDoug e collaboratori** (https://www.dougdoug.com/twitchplays) per il codice "Twitch chat plays".
