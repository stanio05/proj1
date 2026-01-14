# Gra Catch and Avoid

To repozytorium zawiera kod źródłowy do gry typu "Catch and Avoid", w której gracz steruje piłkarzem za pomocą rozpoznawania ruchów dłoni z kamery.

## Opis gry

Gra "Catch and Avoid" to prosta, ale wciągająca gra w której:
- Steruje się piłkarzem za pomocą ruchów dłoni przed kamerą
- Zbiera się piłki spadające z góry ekranu (każda piłka = 1 punkt)
- Unika się czerwonych kartek (każda kolizja = utrata 1 punktu zdrowia)
- Gra kończy się gdy zdrowie spadnie do zera

### Technologie
- **Python** - język programowania
- **MediaPipe** - rozpoznawanie ruchów dłoni
- **OpenCV** - przechwytywanie obrazu z kamery
- **Pygame** - grafika i logika gry

## Wymagania

- Python 3.8 lub nowszy
- Kamera internetowa
- System operacyjny: Windows, macOS lub Linux

## Instalacja

1. Sklonuj repozytorium:
```bash
git clone https://github.com/stanio05/proj1.git
cd proj1
```

2. Zainstaluj wymagane biblioteki:
```bash
pip install -r requirements.txt
```

## Uruchomienie

1. Upewnij się, że kamera jest podłączona i działa

2. Uruchom grę:
```bash
python game.py
```

3. Pojawi się okno z obrazem z kamery i okno gry

## Sterowanie

- **Ruch dłonią** - przesuń dłoń w lewo lub prawo przed kamerą aby sterować piłkarzem
- **R** - restart gry (po zakończeniu)
- **Q** - wyjście z gry

## Zasady gry

1. **Cel**: Zbierz jak najwięcej piłek unikając czerwonych kartek
2. **Punktacja**: Każda zebrana piłka = +1 punkt
3. **Zdrowie**: Zaczynasz z 3 punktami zdrowia
4. **Kolizje**: Każda czerwona kartka = -1 zdrowie
5. **Koniec gry**: Gdy zdrowie spadnie do 0

## Funkcjonalności

- ✅ Rozpoznawanie ruchów dłoni za pomocą MediaPipe
- ✅ Sterowanie postacią w czasie rzeczywistym
- ✅ System punktacji
- ✅ System zdrowia
- ✅ Losowe pojawianie się obiektów
- ✅ Detekcja kolizji
- ✅ Ekran końca gry z możliwością restartu

## Struktura projektu

```
proj1/
├── game.py           # Główny plik gry
├── requirements.txt  # Zależności projektu
├── README.md        # Dokumentacja
└── .gitignore       # Pliki ignorowane przez git
```

## Troubleshooting

**Problem: Kamera nie działa**
- Sprawdź czy kamera jest podłączona
- Upewnij się, że żadna inna aplikacja nie używa kamery
- Sprawdź uprawnienia dostępu do kamery

**Problem: Wolne działanie gry**
- Zamknij inne aplikacje używające kamery
- Zmniejsz rozdzielczość kamery w kodzie

**Problem: Brak rozpoznawania dłoni**
- Upewnij się, że ręka jest dobrze oświetlona
- Trzymaj dłoń w odpowiedniej odległości od kamery (30-60 cm)
- Sprawdź okno "Hand Tracking" czy dłoń jest wykrywana

## Autorzy

Projekt stworzony jako implementacja gry wykorzystującej technologie MediaPipe i OpenCV.

## Licencja

MIT License