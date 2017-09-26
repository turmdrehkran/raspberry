# Controller Software für die SEK Turmdrehkran Hardware
Diese Software wurde zur Steuerung eines Modell-Turmdrehkrans entworfen. Sie dient der Ansteuerung von 3 Schrittmotoren, der Verarbeitung von Eingaben einer Handsteuerung und der Annahme von Protokoll-Befehlen über eine Kommunikationsschnittstelle. Über diese Schnittstelle können Protokoll-Nachrichten empfangen werden, die als Ergebnis einer Verarbeitung einer DSL-Baubeschreinungsprache auswerten.

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

## Usage
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

This software was created as part of the course 'Software Development for Communication Networks' by Prof. Brocks  in the Master's program
'Computer Science and Communication Systems' at htw saar Saarland University
of Applied Sciences.
```

Autoren: 
* Dominik Erb
* Markus Jungbluth (@markusju)
