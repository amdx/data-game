# Data Game

Das Spiel ist webbasiert und besteht aus drei Hauptkomponenten: einem
Data-Dashboard, das die Spieler durch das Spiel führt, die Spielzustände
verwaltet und als Server fungiert, fünf Data Game Clients für das Gameplay und
drei gedruckten Kartensets, die für das Spiel verwendet werden und die
Datenwerte definieren. Idealerweise sollten die Data Game Clients auf mobilen
Geräten ausgeführt werden.

## Voraussetzungen

Um das Spiel auszuführen, benötigst du Folgendes:

- **Einen PC mit einem 4K-Touchscreen**: Dieser wird als Dashboard und Server
  dienen. Obwohl das Spiel auch mit einer Maus funktioniert, bietet ein
  Touchscreen das beste Spielerlebnis. Alternativ kannst du den Server auf einem
  separaten Gerät bereitstellen und die Dashboard-App auf einem anderen Gerät
  öffnen.
    - Installiere [Docker](https://docs.docker.com/)
      und [Docker Compose](https://docs.docker.com/compose/) auf dem Server.
- **Fünf Geräte mit Touchscreens und Kameras**: Diese werden die Client-App
  ausführen. Wie beim Dashboard sind Touchscreens als Eingabegräte am besten
  geeignet.
- **Ein lokales Netzwerk**: Alle Geräte müssen mit demselben Netzwerk verbunden
  sein.
- **Gedruckte Spielkarten**: Du findest die erforderlichen Dateien zum
  Ausdrucken der drei Kartensets im Verzeichnis `print_data/`.
- **Make**: Installiere `make` auf deinem Server.
- **Chrome**: Installiere Chrome auf dem Dashboard und den Client-Geräten.

## Einrichtung

1. Klone dieses Repository auf deinem Server.
2. Stelle sicher, dass Docker und Docker Compose konfiguriert sid und ausgeführt
   werden.
3. Wenn dein Server eine Firewall hat, erlaube den Datenverkehr auf den Ports 80
   und 443.
4. Generiere ein selbstsigniertes Zertifikat mit `make certs`.
5. Führe `make build` aus.
6. Lade den dotLottie-Player herunter, wenn du das Spiel in einer
   Offline-Umgebung ausführen möchtest: `make get-dotlottie-player`.
7. Führe `make run` aus.

An diesem Punkt sollte der Server betriebsbereit sein.
`make stop` beendet alle Spiel-Services.

## Spiel starten

### Dashboard

- Um die Dashboard-App zu starten, öffne in Chrome:
  `https://<server-host>/dashboard`.

### Client

- Um die Client-App zu starten und das Spiel zu spielen öffne auf den
  fünf Mobilgeräten in Chrome: `https://<server-host>/tablet`.

## Datenquellen

Wenn du möchtest, kannst du die Datenwerte der Karten anpassen. Diese findest du
in `configs/dashboard_service/cards_data.csv`.
