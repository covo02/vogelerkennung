### Bei jedem Event

- Thread-Start & Schleife

  - Startet einen eigenen Verarbeitungs-Thread.

  - Läuft, bis ein Shutdown-Signal empfangen wird.

- Event holen

  - Holt das nächste vollständige Event aus dem Event-Store (blockierend, mit Timeout).

  - Beendet sich, wenn kein Event mehr kommt und der Store im Shutdown ist.

- Event-Daten extrahieren

  - Extrahiert alle Kameradaten für das Event.

  - Loggt die Anzahl der beteiligten Kameras.

- Trigger-Metadaten

  - Holt Zeitstempel und Metadaten zum Auslöser des Events.

- Referenzkamera bestimmen

  - Wählt eine Kamera als Referenz (aus Kandidatenliste oder alphabetisch).

  - Holt deren Daten.

- GPS-Referenzpunkt setzen

  - Mit Lock (Thread-Sicherheit): Falls noch kein GPS-Referenzpunkt gesetzt ist, wird er aus der Referenzkamera übernommen und geloggt.

- Kamerapositionen (ENU) berechnen

  - Berechnet für jede Kamera die ENU-Koordinaten (Ost-Nord-Hoch, relativ zum Referenzpunkt).

- Kamerasicht-Richtungen berechnen

  - Berechnet für jede Kamera die Blickrichtung im ENU-System (sofern Kalibrierung vorhanden).

- Kamerapositionen für LIVE-Ansicht cachen

  - Speichert aktuelle ENU-Positionen für spätere Live-Visualisierung.

- Plot-Vorbereitung

  - Erstellt eine Plotly-Figur für die spätere Visualisierung.

- Bildverarbeitung & Bewegungsdetektion

  - Für jede Kamera:

    - Bilder decodieren.

    - Bewegungen (Motion) zwischen zwei Bildern erkennen.

    - Bewegungsdaten und Zeiten speichern.

    - Für jede Bewegung: Richtungsvektor berechnen und debuggen.

    - Kameraobjekte für Triangulation vorbereiten.

- Triangulation

  - Wenn mindestens zwei Kameras Bewegungen erkannt haben, werden die 3D-Punkte trianguliert (Position im Raum berechnet).

- Zeitstempel bestimmen

  - Zeitstempel des Events (aus Kameraheader oder aktuelle Zeit).

- Ergebnisse aufbereiten

  - Ergebnisse (3D-Punkte, Mittelwerte, etc.) für Speicherung und Visualisierung aufbereiten.

- CSV und Plot speichern

  - Ergebnisse als CSV speichern.

  - Plot als HTML speichern (optional).

- Event-Zusammenfassung und Details speichern

  - Zusammenfassung und Detaildaten für UI und spätere Abfragen speichern.

  - Ablaufdatum für automatische Löschung setzen.

- LIVE-Visualisierung aktualisieren

  - Neue Punkte zur Live-Visualisierung hinzufügen.

- Zähler erhöhen

  - Verarbeitungszähler erhöhen.

- Trigger-Metadaten aufräumen

  - Metadaten zum Event-Trigger löschen, um Speicher zu sparen.

- Logging

  - Fortschritt und Timing werden geloggt.

- Fehlerbehandlung

  - Fehler werden geloggt, der Thread läuft weiter.