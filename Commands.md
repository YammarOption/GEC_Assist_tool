# **MANUALE PER L'USO DELL'INTEGRAZIONE TWITCH DEL GEC ASSIST TOOL** 

## 1. Setup
All'interno della cartella `data` c'è il file `TwitchConfig.json` che permette di controllare l'interazione dello strumento con la chat di twitch.

Per configurere il software, aprire il suddetto file e cambiare i campi a seconda delle proprie preferenze:
1. `channel`: il nome del proprio canale twitch (non il link, solo lo username)
1. `mods`: la lista delle persone autorizzate ad usare i comandi, elencati tra virgolette e separati da una virgola. **NB**: inserire i nomi dei mod tutti in minuscolo, perché lo strumento legge i messaggi e converte in minuscolo, nomi compresi.
1. `message rate`:velocità di processing dei messaggi in secondi. Più è alta più velocemente processiamo messaggi con il rischio di finirli e dover aspettare. Più è bassa più tempo usiamo per processare i messaggi, con conseguente aumento del delay tra comando e azione, ma con meno "sprechi" se non ci sono messaggi
1. `queue_length`: numero massimo di messaggi da processare per loop.
1. `workers`: numero massimo di thread impiegate per processare i messaggi. Più il numero è alto più si possono processare messaggi in contemporanea, con conseguente aumento del carico sulla CPU

## 2. COMANDI
Lo strumento mette a disposizione i seguenti comandi:

* `!markmon *pokémon*`: segna il pokémon come catturato (non servono gli *)
* `!markblu *pokémon*`: segna il pokémon come prossimo alla catturata
* `!unmarkmon *pokémon*`: segna il pokémon come non catturato
* `!markmove *mossa*`: segna la mossa come vista
* `!unmarkmove *mossa*`: segna la mossa come non vista
* `!marktrainer *piano*->*nome*`: segna l'allenatore con * nome * al piano specificato nel percorso attuale come battuto. In caso di allenatori con lo stesso nome, viene segnata la prima istanza non ancora spuntata
* `!unmarktrainer *piano*->*nome*`: Come sopra, ma rimuove la spunta. In caso di allenatori con lo stesso nome, viene rimossa la prima istanza già spuntata
* `!markitem *piano*->*nome*`: Stesse regole di **marktrainer** ma per gli oggetti
* `!unmarkitem *piano*->*nome*`: Come precedente, ma rimuove la spunta
* `!markmisc *piano*->*nome*`: Stesse regole di **marktrainer** ma per gli eventi
* `!unmarkmisc *piano*->*nome*`: Come precedente, ma rimuove la spunta

**NB** : per l'overworld, seve specificare come piano "0". Inoltre lo strumento cerca una corrsipondeza in base alle iniziali. Quindi per segnare l'oggetto "Acqua Fresca" è possibile scrivere semplicemente `!markitem *piano*-> Acqua`