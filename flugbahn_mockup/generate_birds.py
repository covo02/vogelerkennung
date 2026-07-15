# from datetime import datetime,timedelta
# import random, math, json


# random.seed(datetime.now().timestamp())

# start=datetime(2026,7,8,10,0,0)
# recs=[]
# # birds=120; samples=125; interval=5
# birds=150; samples=35; interval=5
# for b in range(1,birds+1):

#     samples = random.randint(3, 29)

#     hour = random.randint(0, 23)
#     minute = random.randint(0, 30)
#     start = datetime(2026,7,8,hour,minute,0)

#     x,y=random.uniform(0,1000),random.uniform(0,1000); z=random.uniform(10,100)
#     ang=random.random()*2*math.pi; speed=random.uniform(6,14); vz=random.uniform(-0.05,0.05)
#     for i in range(samples):
#         # interval = random.randint(5, 20)
#         for _ in range(interval):
#             ang+=random.gauss(0,0.02); speed=max(4,min(16,speed+random.gauss(0,0.03)))
#             x+=math.cos(ang)*speed+0.04; y+=math.sin(ang)*speed-0.02
#             z=max(5,min(120,z+vz+random.gauss(0,0.05))); vz=max(-0.15,min(0.15,vz+random.gauss(0,0.005)))
#         # recs.append({"bird_id":f"bird_{b:04d}","determined_bird_id":f"bird_{b:04d}" if random.random()>0.015 else f"bird_{random.randint(1,birds):04d}","timestamp":(start+timedelta(seconds=i*interval)).isoformat()+"Z","x":round(x+random.gauss(0,0.08),2),"y":round(y+random.gauss(0,0.08),2),"z":round(z+random.gauss(0,0.03),2)})
#         recs.append({"bird_id":f"bird_{b:04d}","determined_bird_id":f"bird_0000" if random.random()>0.015 else f"bird_{random.randint(1,birds):04d}","timestamp":(start+timedelta(seconds=i*interval)).isoformat()+"Z","x":round(x+random.gauss(0,0.08),2),"y":round(y+random.gauss(0,0.08),2),"z":round(z+random.gauss(0,0.03),2)})

# out="birds_sparse_manybirds.json"
# json.dump(recs,open(out,"w"),indent=2)
# print(len(recs),out)


# #To Do:
# # evetuell die anzahl der intervalle pro vogel randomizen für mehr realismus (hat komische linien verursacht bitte prüfen)





















"""
Simulation künstlicher Vogel-Flugbahnen

Erzeugt eine JSON-Datei mit:
- Vogel-ID
- simulierter erkannter Vogel-ID (mit Fehlern)
- Zeitstempel
- 3D-Position (x,y,z)

Die Flugbewegung basiert auf einem zufälligen Bewegungsmodell:
- zufällige Änderung der Flugrichtung
- zufällige Änderung der Geschwindigkeit
- Messrauschen
"""

from datetime import datetime, timedelta
import random
import math
import json


# ============================================================
# Einstellungen der Simulation
# ============================================================

# Zufalls-Seed:
# Jeder Programmstart erzeugt neue Flugbahnen
random.seed(datetime.now().timestamp())


# Anzahl der simulierten Vögel
NUMBER_OF_BIRDS = 50


# Messabstand zwischen zwei gespeicherten Punkten [Sekunden]
TIME_INTERVAL = 5


# Simulationsdatum
SIMULATION_DATE = datetime(2026, 7, 8)


# Raumgrenzen
# entspricht z.B. einem Gelände von 1000m x 1000m
X_MIN = 0
X_MAX = 300

Y_MIN = 0
Y_MAX = 300


# Höhenbereich der Vögel
Z_MIN = 10
Z_MAX = 200


# Geschwindigkeitsbereich
MIN_SPEED = 4
MAX_SPEED = 16


# Wahrscheinlichkeit eines Tracking-Fehlers
TRACKING_ERROR_RATE = 0.015


# Messfehler der Positionsdaten
POSITION_NOISE = 0.08


# ============================================================
# Speicherung aller erzeugten Messpunkte
# ============================================================

records = []


# ============================================================
# Simulation der einzelnen Vögel
# ============================================================

for bird_number in range(1, NUMBER_OF_BIRDS + 1):

    # --------------------------------------------------------
    # Jeder Vogel bekommt eine zufällige Anzahl Messpunkte
    # --------------------------------------------------------

    number_of_samples = random.randint(3, 29)


    # --------------------------------------------------------
    # Zufälliger Startzeitpunkt des Vogels
    # --------------------------------------------------------

    start_time = SIMULATION_DATE.replace(
        hour=random.randint(0, 23),
        minute=random.randint(0, 30),
        second=0
    )


    # --------------------------------------------------------
    # Initiale Position im 3D-Raum
    #
    # x,y = horizontale Position
    # z   = Höhe
    # --------------------------------------------------------

    x = random.uniform(X_MIN, X_MAX)
    y = random.uniform(Y_MIN, Y_MAX)
    z = random.uniform(10, 100)



    # --------------------------------------------------------
    # Flugparameter
    #
    # angle:
    # Flugrichtung im Bogenmaß
    #
    # speed:
    # horizontale Geschwindigkeit
    #
    # vertical_speed:
    # Steigen/Sinken
    # --------------------------------------------------------

    angle = random.uniform(0, 2 * math.pi)
    # angle = random.uniform(0, 500 * math.pi)

    speed = random.uniform(6, 14)
    # speed = random.uniform(10, 24)

    vertical_speed = random.uniform(-0.05, 0.05)
    # vertical_speed = random.uniform(-0.01, 0.15)



    # ========================================================
    # Erzeugung der Trajektorie
    # ========================================================

    for sample_index in range(number_of_samples):


        # ----------------------------------------------------
        # Zwischen zwei Messungen werden mehrere kleine
        # Bewegungsschritte simuliert.
        #
        # Dadurch entstehen weichere Flugbahnen.
        # ----------------------------------------------------

        for _ in range(TIME_INTERVAL):


            # ------------------------------------------------
            # Änderung der Flugrichtung
            #
            # Normalverteilung:
            # Mittelwert = 0
            # Standardabweichung = 0.02
            #
            # Der Vogel macht also kleine zufällige Kurven.
            # ------------------------------------------------

            # angle += random.gauss(0, 0.02)
            angle += random.gauss(0, 0.04)



            # ------------------------------------------------
            # Geschwindigkeit verändert sich langsam
            # ------------------------------------------------

            speed += random.gauss(0, 0.03)


            # Begrenzung der Geschwindigkeit

            speed = max(
                MIN_SPEED,
                min(MAX_SPEED, speed)
            )



            # ------------------------------------------------
            # Bewegung im 2D-Raum
            #
            # Umrechnung:
            #
            # vx = v*cos(Winkel)
            # vy = v*sin(Winkel)
            #
            # ------------------------------------------------

            x += math.cos(angle) * speed
            y += math.sin(angle) * speed



            # ------------------------------------------------
            # Vertikale Bewegung
            # ------------------------------------------------

            z += vertical_speed


            # kleine zufällige Höhenänderung

            z += random.gauss(0, 0.05)



            # Höhe begrenzen

            z = max(
                Z_MIN,
                min(Z_MAX, z)
            )



            # ------------------------------------------------
            # Änderung der Steiggeschwindigkeit
            # ------------------------------------------------

            # vertical_speed += random.gauss(0, 0.005)
            vertical_speed += random.gauss(0, 0.01)   

            # vertical_speed = max(
            #     -0.15,
            #     min(0.15, vertical_speed)
            # )



        # ====================================================
        # Messpunkt erzeugen
        # ====================================================


        bird_id = f"bird_{bird_number:04d}"



        # ----------------------------------------------------
        # Simuliert erkannte Vogel-ID
        #
        # Normal:
        # bird_0000 bedeutet "kein sicherer Track"
        #
        # Selten:
        # falsche Zuordnung
        # ----------------------------------------------------

        if random.random() < TRACKING_ERROR_RATE:

            determined_id = (
                f"bird_{random.randint(1, NUMBER_OF_BIRDS):04d}"
            )

        else:

            determined_id = "bird_0000"



        # ----------------------------------------------------
        # Position mit Messrauschen speichern
        #
        # Simulation eines realen Sensors:
        # Kamera/Triangulation ist nie exakt
        # ----------------------------------------------------

        record = {

            "bird_id": bird_id,

            "determined_bird_id": determined_id,


            "timestamp":
                (
                    start_time
                    +
                    timedelta(
                        seconds=sample_index * TIME_INTERVAL
                    )
                )
                .isoformat()
                + "Z",



            "x":
                round(
                    x + random.gauss(0, POSITION_NOISE),
                    2
                ),


            "y":
                round(
                    y + random.gauss(0, POSITION_NOISE),
                    2
                ),


            "z":
                round(
                    z + random.gauss(0, 0.03),
                    2
                )
        }



        # Punkt zur Gesamtliste hinzufügen

        records.append(record)



# ============================================================
# JSON-Datei schreiben
# ============================================================

OUTPUT_FILE = "birds_sparse_manybirds.json"


with open(
    OUTPUT_FILE,
    "w"
) as file:

    json.dump(
        records,
        file,
        indent=2
    )


print(
    f"{len(records)} Punkte erzeugt"
)

print(
    f"Datei gespeichert: {OUTPUT_FILE}"
)