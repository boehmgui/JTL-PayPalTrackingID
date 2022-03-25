# Sendungsverfolgungsnummer zu PayPal übertragen

Dieses Skript setzt den Sendungsstatus und Sendungsverfolgungsnummer für eine Paypal Transaktion ID.

Es implementiert die Tackers batch resource group von PayPal, welche hier beschrieben ist:
https://developer.paypal.com/api/tracking/v1/#trackers-batch_post

## Limitationen
- Das Skirpt unterstützt das Setzen der Sendungsdaten von genau einer Transkation. Sollen Sendungsdaten für 
  meherere Transaktionen gesetzt werden, muss das Skript entsprechend oft aufgerufen werden. 
- Es wird nur der Shipping Status ```SHIPPED``` unterstützt
- wenn keine Sendungsnummer angegeben wird, setzt Paypal den Carrier automatisch auf ```MANUAL```

# Vorbereitungen
## heruntrerladen des Skripts
Folgende Dateien wmüssen heruntergeladen und auf der lokalen HD in einem gemeinsamen Verzeichnis abgelegt werden
- pp_tracking_id.py
- pp_tracking_id.exe
- config.yaml.example
- requirements.txt

## Konfigurationsdatei
###config.yaml
Die Datei config.yaml muss im gleichen Verueichnis wie das Skript (.py oder .exe) liegen.

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

###Zugangsdaten
- Generieren der Zugansgdaten für PayPals REST API gemäß Beschreibung: https://developer.paypal.com/api/rest/#link-getcredentials

Die so erstellten Zugangsdaten dann in folgende zu erstellende Dateien eingetragen:
- PayPals Live System: ```.env.production```
- PayPals Sandbox: ```.env.sanbox```
Beispiel
```
# API Zugangsdaten wie hier beschrieben generieren
# https://developer.paypal.com/api/rest/#link-getcredentials
Client_ID=AaNSfvjN3aV3rTaEd2d0n51foIzhbmnlkrmuw3zk0oqFEFjWQ72jp0Jy3EzSuev5LCoyzYyxbl9ikmPOo
Secret=EGnt5uUA1TB0Mw43yWPtrgsGcUghgn76fd9DId5i_kgdSYJ8Ef1qQ0Zxti00U4v7mTvqFIwKuuhkmPK9m-
```
Diese .env.* Dateien müssen im gleichen Verueichnis wie das Skript (.py oder .exe) liegen.

## benötigte Python Module (nicht notwendig, wenn Windows .exe verwendet wird)
Installieren der Python Module
```
pip install -r requirements.txt
``` 

## Skriptstart
### Aufruf als Windows .exe

```
pp_tracking_id.exe -p transaction_id=<pp Transaktionscode> tracking_number=<carrier tracking id> carrier_other_name=< anderer carrier name>
```

### Aufruf als Python Skript

```
python3 pp_tracking_id.py -p transaction_id=<pp Transaktionscode> tracking_number=<carrier tracking id> carrier_other_name=< anderer carrier name>
```


## Kommandozeilen Parameter:
- ```transaction_id```: Transaktionscode der Transaktion für welche der Sendungsstatus gesetzt werden soll. E.g. 2AB57058X62543450
- ```tracking_number```: Sendungsverfolgungsnummer des Carriers
- ```shipment_date```: in der Form JJJJ-MM-DD (2022-02-28) - wenn nicht angegeben wird aktuelles Datum genommen
- ```carrier```:
  - Carrier code gemäß https://developer.paypal.com/docs/tracking/reference/carriers/#link-addtrackingapicarriers
  - alternativ: ```OTHER``` - dann Carrier Namen in ```carrier_other_name``` setzen
- ```carrier_other_name```: alternativer Carrier Name → nur wenn Carrier auf ```OTHER``` gesetzt war 

## Fehler
Sollte bem Setzen des Sendungsstatus ein fehler auftreten, wird für den entsprechenden PayPal TransaktionsCode ein 
Fehlerbereicht in das Verzeichnis ```./failed-trasactions``` geschrieben
