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

- Kameransicht-Richtungen berechnen

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




### GPS Ermittlung

1. GPS Werte über die Sensoren bestimmen (PI)
    
    - pi*/gps_reader.py

2. Wert einlesen

    - get_gps_raw()

2. GPS Wert festlegen (PI)

    - Durchschnittswerte bestimmen

        - get_gps_data()
        - GPS_MODE = "avg"

    - Manuell Werte eintragen

        - GPS_MODE = "manual"

3. GPS Wert eintragen (PI)
    ```
    def get_selected_gps() -> tuple[dict, str]:
    gps = get_gps_data()
    if GPS_MODE == "manual":
        gps["lat"] = MANUAL_GPS["lat"]
        gps["lon"] = MANUAL_GPS["lon"]
        gps["alt"] = MANUAL_GPS["alt"]
    return gps, GPS_MODE
    ```

4. Per Trigger an den Server über JSON senden (PI)
    ```
    gps_selected, gps_mode = get_selected_gps()
    ori_selected, imu_mode = get_selected_orientation()

    base_header = build_base_header(
        trigger_time=trigger_time,
        event_id=event_id,
        gps=gps_selected,          # ← GPS data here
        orientation=ori_selected,  # ← Orientation data here
        lux=lux, temp=temp, press=press, hum=hum,
        alt_mode=gps_mode,
    )
    ```

5. GPS Daten empfangen
    ```
    with gps_reference_lock:
    gps_reference_point = (  # ← ENU origin
        reference_camera_data.header["gps"]["lat"],
        reference_camera_data.header["gps"]["lon"],
        reference_camera_data.header["gps"]["alt"],
    )
    ```

6. An den Referenzpunkt anpassen
    ```
    e, n, u = tri.geodetic_to_enu(lat, lon, alt, gps_ref[0], gps_ref[1], gps_ref[2])
                    camera_positions_enu_event[cam_id] = (float(e), float(n), float(u))
    ```

7. GPS Wert für den Livegraphen aufbereiten
    ```
    enu = kamera.enu_koordinate
    if isinstance(enu, (list, tuple)) and len(enu) >= 3:
        with camera_positions_lock:
            camera_positions_enu[camera_id] = (float(enu[0]), float(enu[1]), float(enu[2]))
    ```