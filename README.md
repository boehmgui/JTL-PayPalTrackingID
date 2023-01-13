# Sendungsverfolgungsnummer zu PayPal übertragen

Dieses Skript setzt den Sendungsstatus und die Sendungsverfolgungsnummer für eine Paypal Transaktion ID.

Es implementiert die Tackers batch resource group von PayPal, welche hier beschrieben ist:
https://developer.paypal.com/api/tracking/v1/#trackers-batch_post

## Limitationen
- Das Skirpt unterstützt das Setzen der Sendungsdaten von genau einer Transkation. Sollen Sendungsdaten für 
  meherere Transaktionen gesetzt werden, muss das Skript entsprechend oft aufgerufen werden. 
- Es wird nur der Shipping Status ```SHIPPED``` unterstützt
- wenn keine Sendungsnummer angegeben wird, setzt Paypal den Carrier automatisch auf ```MANUAL```

# Installation als .exe (kein Python erforderlich)
## Vorbereitungen
Im Releasebereich https://github.com/boehmgui/JTL-PayPalTrackingID/releases das Paket ```pp_tracking_id.zip ```
herunterladen und lokal im Wunschverzeichnis entpacken. Folgende Dateien sollten dann vorhanden sein:
- pp_tracking_id.exe
- config.yaml
- .env.sandbox.example
- .env.production.example

## Konfigurationsdateien
### config.yaml
Die Datei config.yaml muss im gleichen Verzeichnis wie das Skript (.exe) liegen.
Über den Parameter ```LiveModus``` kann man steuern, ob man Tracking IDs für echte Kundentransaktionen (Live API -> 
```LiveModus: True```) oder 
 Testtransaktionen (Sandbox -> ```LiveModus: False```) setzen möchte.
Weitere Änderungen sollten in dieser Datei nicht gemacht werden

```
# Soll die Live API oder Sandbox AP benutzt werden?
# True -> Live API
# False -> Sandbox
LiveModus: True

# nur auf Anforderung ändern
Debug: False

# PayPal API Dokumentation:
# https://developer.paypal.com/api/tracking/v1/
SandBoxAPI:
  BaseUrl: 'https://api-m.sandbox.paypal.com'
  EndPoint_Token: '/v1/oauth2/token'
  EndPoint_TrackersBatch: '/v1/shipping/trackers-batch'

LiveAPI:
  BaseUrl: 'https://api-m.paypal.com'
  EndPoint_Token: '/v1/oauth2/token'
  EndPoint_TrackersBatch: '/v1/shipping/trackers-batch'


```

### Zugangsdaten
- Generieren der Zugansgdaten für PayPals REST API gemäß Beschreibung: https://developer.paypal.com/api/rest/#link-getcredentials

Bennen Sie folgende Dateien um:
- .env.production.example  -> .env.production
- .env.sandbox.example -> .env.sandbox
- 
Die erstellten Zugangsdaten dann in entsprechende .env.xxx eingetragen:
- PayPals Live System: ```.env.production```
- PayPals Sandbox: ```.env.sanbox```

Beispiel:
```
# API Zugangsdaten wie hier beschrieben generieren
# https://developer.paypal.com/api/rest/#link-getcredentials
Client_ID=AaNSfvjN3aV3rTaEd2d0n51foIzhbmnlkrmuw3zk0oqFEFjWQ72jp0Jy3EzSuev5LCoyzYyxbl9ikmPOo
Secret=EGnt5uUA1TB0Mw43yWPtrgsGcUghgn76fd9DId5i_kgdSYJ8Ef1qQ0Zxti00U4v7mTvqFIwKuuhkmPK9m-
```
Die .env.* Dateien müssen im gleichen Verzeichnis wie das Skript (.exe) liegen.



## Skriptstart

```
pp_tracking_id.exe -p transaction_id=<pp Transaktionscode> tracking_number=<carrier tracking id> carrier_other_name="< anderer carrier name>"
```




## Kommandozeilen Parameter:
- ```transaction_id```: Transaktionscode der Transaktion für welche der Sendungsstatus gesetzt werden soll. E.g. 2AB57058X62543450
- ```tracking_number```: Sendungsverfolgungsnummer des Carriers
- ```shipment_date```: in der Form JJJJ-MM-DD (2022-02-28) - wenn nicht angegeben wird aktuelles Datum genommen
- ```carrier```:
  - Carrier code gemäß https://developer.paypal.com/docs/tracking/reference/carriers/#link-addtrackingapicarriers
  - alternativ: ```OTHER``` - dann Carrier Namen in ```carrier_other_name``` setzen
- ```carrier_other_name```: alternativer Carrier Name → nur wenn Carrier auf ```OTHER``` gesetzt war 

**Achtung:** sofern übergebene Werte Leerzeichen enthalten, zB ```DHL Express``` als ```carrier_other_name```, muss 
dieser in Hochkommas eingeschlossen werden

## Fehler
Sollte beim Setzen des Sendungsstatus ein Fehler auftreten, wird für den entsprechenden PayPal TransaktionsCode ein 
Fehlerbereicht in das Verzeichnis ```./failed-trasactions``` geschrieben


# Python source code
## Getting Started
1. Clone this repository to a folder and change directory into the folder 
```git clone https://github.com/boehmgui/JTL-PayPalTrackingID.git```
2. Set up a virtual environment in it and install the required packages
  ```
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ``` 

## Access Token
1. create the access tokens for PayPals REST API as described  here: https://developer.paypal.
com/api/rest/#link-getcredentials

2. Renanme the following files:
   - .env.production.example  -> .env.production
   - .env.sandbox.example -> .env.sandbox

Insert the created tokens iinto the corresponding .env.xxx files:
- PayPals Live System: ```.env.production```
- PayPals Sandbox: ```.env.sanbox```
Example
```
# API Zugangsdaten wie hier beschrieben generieren
# https://developer.paypal.com/api/rest/#link-getcredentials
Client_ID=AaNSfvjN3aV3rTaEd2d0n51foIzhbmnlkrmuw3zk0oqFEFjWQ72jp0Jy3EzSuev5LCoyzYyxbl9ikmPOo
Secret=EGnt5uUA1TB0Mw43yWPtrgsGcUghgn76fd9DId5i_kgdSYJ8Ef1qQ0Zxti00U4v7mTvqFIwKuuhkmPK9m-
```
The .env.* must be in the same directory thne the script (.py).

## running the script
Example
```
python3 pp_tracking_id.py -p transaction_id=<pp Transaktionscode> tracking_number=<carrier tracking id> 
carrier_other_name="< other carrier name>"
```
