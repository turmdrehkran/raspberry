# Controller Software für die SEK Turmdrehkran Hardware
Diese Software wurde zur Steuerung eines Modell-Turmdrehkrans entworfen. Sie dient der Ansteuerung von 3 Schrittmotoren, der Verarbeitung von Eingaben einer Handsteuerung und der Annahme von Protokoll-Befehlen über eine Kommunikationsschnittstelle. Über diese Schnittstelle können Protokoll-Nachrichten empfangen werden, die als Ergebnis einer Verarbeitung einer DSL-Baubeschreibungsprache auswerten.

## Setup
Um diese Software zu installieren wird ein Raspberry der zweiten oder dritten Generation benötigt.
Die Software würde auch auf einem Raspberry erster Generation laufen, jedoch ist auf diesen Geräten die Anzahl der verfügbaren GPIO-Pins zu niedrig.

Zunächst müssen auf dem Raspberry Pi die Abhängigkeiten dieses Projekts befriedigt werden:
```
$ sudo apt-get install libbluetooth-dev python-pip
```
Anschließend kann über den PIP-Paketmanager die `turmdrehkran-app` installiert werden:
```
$ pip install https://github.com/turmdrehkran/raspberry/archive/master.tar.gz
```
## Benutzung
`turmdrehkran-app` bietet zwei Einstiegspunkte, die als Befehl auf der Shell ausgeführt werden können
* `turmdrehkran-controller`
    * Steuerungssoftware für die Kran-Hardware 
* `turmdrehkran-bt-proxy`
    * Proxy-Applikation, die einen Bluetooth RFCOMM-Socket auf ein TCP-Socket mappt. Kann im Zusammenspiel mit einer externen Applikation zum Einsatz kommen, die den Hardware-Controller ansteuert. 

Die Controller Software kann über den Aufruf in der Shell mit Angabe von Parametern gestartet werden:
```
$ turmdrehkran-controller -h
usage: turmdrehkran-controller [-h] {gpio,mock} {bluetooth,tcp}

Turmdrehkran Hardware Controller

positional arguments:
  {gpio,mock}      Mode of operation: 'gpio' will use the Raspberry's GPIO.
                   'mock' will simulate the Pi's GPIO and print actions to the
                   screen.
  {bluetooth,tcp}  Socket Type: 'bluetooth' will start a Bluetooth RFCOMM
                   service. 'tcp' will start a single-threaded TCP Server on
                   Port 5010.

optional arguments:
  -h, --help       show this help message and exit

This software was created as part of the course 'Software Development for Communication Networks' by Prof. Brocks 
as part of the Master's program 'Computer Science and Communication Systems' at htw saar Saarland University
of Applied Sciences.
```
Die Proxy Software kann ebenfalls über den Aufruf in der Shell gestartet werden:
```
$ turmdrehkran-bt-proxy
Suche Controller...
Suche Raspberry

```
Die Proxy-Software versucht zunächst den Raspberry und dann den Arduino zu finden. Findet er eines der beiden Geräte in diese Reihenfolge wartet er auf eine eingehende TCP-Verbindung auf Port `5010`. Sobald eine Verbindung zu diesem Port hergestellt ist, wird auch eine Verbindung über Bluetooth hergestellt.

## Bluetooth-Konfiguration
Damit sich der HigherLevelController mit dem Controller verbinden kann, müssen beide Geräte zuvor ein Bluetooth-Pairing durchführen.
Um dies durchzuführen muss folgender Befehl auf dem Hardware-Controller ausgeführt werden:

```
$ bluetoothctl 
[NEW] Controller 00:1A:7D:DE:AD:00 pi [default]
[bluetooth]# agent on
[bluetooth]# pairable on
[bluetooth]# discoverable on
...
Pin-Eingabe
```
Sobald sich der Client mit dem Controller verbindet muss eine PIN eingebene werden. Die Bluetooth-Konsole fordert dann dazu auf.
Sobald das Pairing abgeschlossen ist, verbinden sich Controller und HigherLevelController jedes mal automatisch.

## Pin-Belegung
Alle Belegungsangaben beziehen sich auf die `BOARD` Nummerierung des Raspberry Pi 2 und 3.
### Inputs
| Pin | Beschreibung |
| --- | --- |
| `35` | Lichtschranke 1 |
| `36` | Lichtschranke 2 |
| `32` | Lichtschranke 3  |
| `33` | Lichtschranke 4  |
| `22` | Handsteuerung Oben  |
| `23` | Handsteuerung Unten  |
| `19` | Handsteuerung Links |
| `21` | Handsteuerung Rechts  |
| `24` | Handsteuerung Optional Oben  |
| `26` | Handsteuerung Optional Unten  |
| `29` | Handsteuerung Optional Links  |
| `31` | Handsteuerung Optional Rechts  |

### Outputs
| Pin | Beschreibung |
| --- | --- |
| `7` | Motor 1 Direction |
| `8` | Motor 1 Steps (PWM) |
| `11` | Motor 2 Direction |
| `12` | Motor 2 Steps (PWM) |
| `15` | Motor 3 Direction |
| `16` | Motor 3 Steps (PWM) |
| `40` | Connection LED |

Autoren: 
* Dominik Erb
* Markus Jungbluth (@markusju)
