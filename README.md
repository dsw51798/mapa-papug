# MAPA PAPUG
Jakub Kuśmierek, 51798 <br>
Data wykonania: Styczeń 2025



## 💠Cel Strony
Głównym celem projektu było wykorzystanie środowiska Flask, JavaScript oraz HTML stylizowanego za pomocą CSS w celu przedstawienia fikcyjnej strony społecznościowej dla posiadaczy papug. Użytkownicy mogą dodawać własne zdjęcia a następnie przeglądać je na interaktywnym modelu planety. Projekt został też zainspirowany moją pasją do grafiki 3D, odcisków cyfrowych (dane EXIF), a także wiedzą w tym obszarze, co znacznie ułatwiło pisanie funkcji dynamicznie renderującej mapę.

## Instalacja
Projekt jest gotowy do pobrania i uruchomienia. Należy jednak upewnić się że pobrane są wszystkie moduły z pliku `requirements.txt` Aby to zrobić, najlepiej w środowisku wirtualny, należy wykonać komendę:
```
pip install -r requirements.txt
```
Po zainstalowaniu wszystkich modułów projekt jest gotowy do uruchomienia:
```
python main.py
```
Projekt domyślnie włącza się na porcie `5000`, zatem URL to `127.0.0.1:5000`

## 💠Architektura Projektu
Projekt jest podzielony na foldery zgodnie z wymaganiami środowiska Flask:
* instance: zawiera bazę danych users.db
* static: zawiera 'statyczne' pliki typu
  * fonts (czcionki)
  * img (obrazy — w tym tekstury)
  * js (skrypty JavaScript)
  * live (dynamicznie odświeżane posty i ich obrazy)
  * styl w CSS
* templates: template stron w postaci plików .html

Plik requirements.txt zawiera wszystkie biblioteki wymagane do uruchomienia projektu w środowisku Python.

W projekcie użyto biblioteki zewnętrzne zgodnie z zamierzonym celem ich używania.
* Moduły Flask są niezbędne do funkcjonalności strony, w tym...
  * Flask Admin umożliwia dostęp do panelu administracyjnego gdzie w sposób przyjazny dla człowieka można zarządzać bazą danych w interfejsie graficznym
  * Flack Bcrypt szyfruje hasła w celu zapewnienia jaknajwyższej jakości bezpieczeństwa dla użytkowników końcowych
* Pillow, PIExif umożliwiają odszyfrowywanie danych EXIF (położenia geograficznego) z przesłanych przez użytkowników zdjęć.
* Używany w JavaScript'cie ThreeJS to wydajny silnik renderowania sceny 3D za pomocą frameworku OpenGL. W nim proceduralnie generowana jest sfera na którą nakładana jest tekstura Ziemii. W celu zwiększenia wydajności używana jest technika renderowania materiałów "unlit", czyli obiekty są zawsze oświetlone — nie emitują cieni, ani ich nie przyjmują.

