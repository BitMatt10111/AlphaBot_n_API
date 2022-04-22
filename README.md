# AlphaBot_n_API

L'obbiettivo di questo progetto era quello di creare una web api ed un client  
che interagendo facessero muovere un'AlphaBot in base a dei sensori. Lo scopo  
finale era quello di riuscire a completare un percorso a ferro di cavallo formato  
da alcune scatole di cartone.

**Librerie usate:**
- RPi.GPIO
- time
- flask
- random
- requests

## API Server

### sensor_api
Questa funzione associata alla pagina */api/v1/sensors/obstacles* legge i valori tramite  
`GPIO.input(DR)` e `GPIO.input(DL)` e la returna sotto forma di dizionario.  

### motors_api
Questa funzione preleva dall'url i valori dati dal client pwmR, pwmL, time e  
le usa per muovere l'Alphabot.

## Client

É essenzialmente un while true che ad ogni iterazione preleva i valori dai sensori  
tramite `requests.get("http://192.168.0.141:5000/api/v1/sensors/obstacles")` e in base  
ad essi decide se girare a dx, sx, andare dritto o tornare un po' indietro curvando da  
un lato scelto in modo casuale. Una volta ottenuti i valori, tramite la riga di codice  
`x=requests.get(f"http://192.168.0.141:5000/api/v1/motors/both?pwmL={pwmL}&pwmR={-pwmR}&time={500}")`  
esegue una GET "inviando" i valori tramite URL al server API.  
