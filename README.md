Pythomat
========

Pythomat ist der ideale Helfer für (faule) Studenten. Wer die Flut an Skript-Versionen, Übungsblättern und Vorlesungsmitschnitten kennt, weiß, wie nervig es sein kann, seine digitale Kopie davon immer auf dem neusten Stand zu halten, sodass er auch in Bus, Bahn oder dem Saarland darauf zugreifen kann, ohne sich mit langsamen Mobilverbindungen herum zu schlagen.

Der Pythomat ist leicht erweiterbar, klein und (relativ) schnell installiert. Er ist in Python geschrieben, weil Cehmat, Javamat oder Essemelmat einfach dumm klingt. Und, weil Python plattformunabhängig ist. Und, weil der Autor es noch nicht konnte, als er das Skript begonnen hat.

# Voraussetzungen

Python 2.7 (nicht Python 3.x!) und mechanize werden benötigt.

# Installation

- Python 2.7 (irgendwas > 2.3 reicht zur Not auch) von http://python.org herunterladen und installieren.
- setuptools von https://pypi.python.org/pypi/setuptools herunterladen und installieren
- in der Konsole 'easy_install mechanize' eingeben
- einen Ordner pythomat anlegen
- youtube-dl von http://rg3.github.io/youtube-dl/ herunterladen und in den Ordner verschieben oder global installieren
- pythomat.py herunterladen und in den Ordner verschieben

# Konfiguration

Pythomat benutzt die Standard-Bibliothek ConfigParser zum Parsen von ini-Dateien. Standardmäßig wird pythomat.ini verwendet.

Hier eine Beispieldatei, die ein einzelnes Skript herunterlädt.

	[VorlesungsSkript]
	path = http://www.vorlesung.de/skript.pdf
	saveto = C:\Users\Beispiel\
	mode = single

Es stehen die folgenden Standard-Modi zur Verfügung:

	single		Lädt eine einzelne Datei herunter, falls sie auf dem Server geändert wurde. 
				Benötigt path und saveto.
	youtube		Lädt ein einzelnes YouTube-Video der gegebenen id herunter. 
				Benötigt path und saveto.
	batch		Durchsucht eine Seite nach Links und lädt alle diese Dateien herunter. 
				Benötigt path, saveto und pattern.
	module 		Lädt %name.py und führt %name.start(items) aus. items ist dabei ein Dictionary, das die
				Einstellungen enthält.
				
Hier steht ein zusätzliches Modul zur Verfügung:
	prog2		Lädt die aktuellen Youtube-Videos der Vorlesung herunter.
				Benötigt user, pass und saveto.

Weitere Modi lassen sich schnell selbst erstellen. Sollte man keinerlei Programmierkenntnisse haben, sind Anfragen unter Issues auch eine Möglichkeit.
