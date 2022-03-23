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
- Generienren der Zugansgdaten für PayPals REST API gemäß Beschreibung: https://developer.paypal.com/api/rest/#link-getcredentials
- Umbenennen von ```config.yaml.example``` in ```config.yaml```
- ```CLIENT_ID``` und ```SECRET``` von der PayPal Seite entsprechend SandBox oder live Zugang in der Yaml Datei unter 
  ```CredentialsSandBox``` respektive ```CredentialsLive``` eintragen

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
Sollte bem Setzen des Sendungsstatus ei fehler auftreten, wird für den entsprechende PayPal TransaktionsCode ein 
Fehlerbereicht in das Verzeichnis ```./failed-trasactions``` geschrieben