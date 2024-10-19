# **MANUALE PER L'USO DELL'INTEGRAZIONE TWITCH DEL GEC ASSIST TOOL** 

## 1. Setup
All'interno della cartella `data` c'è il file `TwitchConfig.json` che permette di controllare l'interazione dello strumento con la chat di twitch. Se il file manca, il software parte in modalità 'offline', ma può essere comunque usato.

Per configurere il software, aprire il suddetto file e cambiare i campi a seconda delle proprie preferenze:
1. `channel`: il nome del proprio canale twitch (non il link, solo lo username)
1. `mods`: la lista delle persone autorizzate ad usare i comandi, elencati tra virgolette e separati da una virgola. **NB**: inserire i nomi dei mod tutti in minuscolo, perché lo strumento legge i messaggi e converte in minuscolo, nomi compresi.
1. `message rate`:velocità di processing dei messaggi in secondi. Più è alta più velocemente processiamo messaggi con il rischio di finirli e dover aspettare. Più è bassa più tempo usiamo per processare i messaggi, con conseguente aumento del delay tra comando e azione, ma con meno "sprechi" se non ci sono messaggi
1. `queue_length`: numero massimo di messaggi da processare per loop.
1. `workers`: numero massimo di thread impiegate per processare i messaggi. Più il numero è alto più si possono processare messaggi in contemporanea, con conseguente aumento del carico sulla CPU
1. `BACKUP_COUNTER`: Quanti messaggi dalla chat leggere prima di forzare un salvataggio dei dati. Mettere a 0 per disabilitare l'opzione.

## 2. COMANDI

Lo strumento mette a disposizione diverse classi di comandi, che possono essere personalizzati a piacere. Per semplicità sono già forniti degli esempi di comandi. Si suggerisce comunque di evitare l'uso di accenti o caratteri speciali nel definire i comandi, e **sopratutto** di non mettere spazi.

Indipendentemente dal nome del comando usato, le varie classi di comandi hanno il seguente funzionamento:

* `CMD_ADD_POKEMON *pokémon*`: segna il pokémon come catturato (non servono gli *)
* `CMD_ADD_POKEMON_BLUE *pokémon*`: segna il pokémon come prossimo alla catturata
* `CMD_REMOVE_POKEMON *pokémon*`: segna il pokémon come non catturato
* `CMD_ADD_MOVE *mossa*`: segna la mossa come vista
* `CMD_REMOVE_MOVE *mossa*`: segna la mossa come non vista
* `CMD_ADD_TRAINER *piano*->*nome*`: segna l'allenatore con * nome * al piano specificato nel percorso attuale come battuto. In caso di allenatori con lo stesso nome, viene segnata la prima istanza non ancora spuntata
* `CMD_REMOVE_TRAINER *piano*->*nome*`: Come sopra, ma rimuove la spunta. In caso di allenatori con lo stesso nome, viene rimossa la prima istanza già spuntata
* `CMD_ADD_ITEM *piano*->*nome*`: Stesse regole di **marktrainer** ma per gli oggetti
* `CMD_REMOVE_ITEM *piano*->*nome*`: Come precedente, ma rimuove la spunta
* `CMD_ADD_MISC *piano*->*nome*`: Stesse regole di **marktrainer** ma per gli eventi
* `CMD_REMOVE_MISC *piano*->*nome*`: Come precedente, ma rimuove la spunta

**NB** : per l'overworld, seve specificare come piano "0". Inoltre lo strumento cerca una corrispondeza in base alle iniziali. Quindi per segnare l'oggetto "Acqua Fresca" è possibile scrivere semplicemente `!markitem *piano*-> Acqua`