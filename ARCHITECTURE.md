# Architektura Gry - Catch and Avoid

## Przegląd

Gra "Catch and Avoid" została zaimplementowana w Pythonie z wykorzystaniem następujących komponentów:

## Struktura Kodu

### Klasy Główne

#### 1. `HandTracker`
Odpowiada za wykrywanie i śledzenie dłoni przy użyciu MediaPipe i OpenCV.

**Główne metody:**
- `__init__()` - Inicjalizacja MediaPipe Hands i kamery
- `update()` - Aktualizacja pozycji dłoni z każdej klatki kamery
- `get_player_x()` - Konwersja pozycji dłoni na współrzędne ekranu
- `close()` - Zamknięcie kamery i okien

**Funkcjonalność:**
- Wykrywa jedną dłoń w czasie rzeczywistym
- Używa punktu odniesienia 8 (czubek palca wskazującego) do określenia pozycji
- Wyświetla obraz z kamery z nałożonymi punktami odniesienia dłoni

#### 2. `Player`
Reprezentuje gracza (piłkarza) sterowanego przez dłoń.

**Atrybuty:**
- `x, y` - Pozycja na ekranie
- `width, height` - Wymiary
- `rect` - Prostokąt kolizji

**Metody:**
- `update(x)` - Aktualizacja pozycji na podstawie ruchu dłoni
- `draw(screen)` - Rysowanie postaci gracza

#### 3. `Ball`
Klasa reprezentująca piłkę do zbierania.

**Atrybuty:**
- `x, y` - Pozycja
- `radius` - Promień
- `speed` - Prędkość opadania

**Metody:**
- `update()` - Przesunięcie piłki w dół
- `draw(screen)` - Rysowanie piłki z wzorem
- `is_off_screen()` - Sprawdzenie czy piłka wyszła poza ekran

#### 4. `RedCard`
Klasa reprezentująca czerwoną kartkę (przeszkodę).

**Atrybuty:**
- `x, y` - Pozycja
- `width, height` - Wymiary
- `speed` - Prędkość opadania

**Metody:**
- `update()` - Przesunięcie kartki w dół
- `draw(screen)` - Rysowanie czerwonej kartki
- `is_off_screen()` - Sprawdzenie czy kartka wyszła poza ekran

#### 5. `Game`
Główna klasa zarządzająca grą.

**Atrybuty stanu:**
- `score` - Wynik gracza
- `health` - Punkty zdrowia
- `game_over` - Flaga końca gry
- `balls` - Lista aktywnych piłek
- `red_cards` - Lista aktywnych czerwonych kartek

**Główne metody:**
- `run()` - Główna pętla gry
- `update()` - Aktualizacja stanu gry
- `draw()` - Renderowanie grafiki
- `spawn_objects()` - Tworzenie nowych obiektów
- `check_collisions()` - Detekcja kolizji
- `reset_game()` - Reset gry do stanu początkowego

## Przepływ Gry

```
Start
  ↓
Inicjalizacja (Pygame, MediaPipe, OpenCV)
  ↓
Główna Pętla ←─────────┐
  ↓                     │
Obsługa Zdarzeń         │
  ↓                     │
Aktualizacja Dłoni      │
  ↓                     │
Aktualizacja Gracza     │
  ↓                     │
Tworzenie Obiektów      │
  ↓                     │
Aktualizacja Obiektów   │
  ↓                     │
Detekcja Kolizji        │
  ↓                     │
Renderowanie            │
  ↓                     │
Sprawdzenie Końca ──────┘
  ↓
Czyszczenie i Zamknięcie
  ↓
Koniec
```

## Parametry Gry

### Stałe Konfiguracyjne
```python
WINDOW_WIDTH = 800      # Szerokość okna
WINDOW_HEIGHT = 600     # Wysokość okna
FPS = 60                # Klatki na sekundę

PLAYER_WIDTH = 50       # Szerokość gracza
PLAYER_HEIGHT = 60      # Wysokość gracza

BALL_RADIUS = 20        # Promień piłki
RED_CARD_WIDTH = 30     # Szerokość czerwonej kartki
RED_CARD_HEIGHT = 45    # Wysokość czerwonej kartki

INITIAL_HEALTH = 3      # Początkowe zdrowie
SPAWN_INTERVAL = 60     # Interwał pojawiania się obiektów (klatki)
FALL_SPEED = 3          # Prędkość opadania obiektów
```

## System Kolizji

Gra używa prostokątów kolizji Pygame (`pygame.Rect`) do wykrywania kolizji:

1. **Piłki**: Kolizja z graczem → +1 punkt, usuń piłkę
2. **Czerwone kartki**: Kolizja z graczem → -1 zdrowie, usuń kartkę
3. **Koniec gry**: Gdy zdrowie = 0

## System Spawnu

- Obiekty pojawiają się co 60 klatek (1 sekunda przy 60 FPS)
- 70% szansy na piłkę, 30% na czerwoną kartkę
- Losowa pozycja X w granicach ekranu
- Początkowa pozycja Y powyżej ekranu

## Optymalizacje

1. **Wydajność kamery**: 
   - Używa `cv2.waitKey(1) & 0xFF` dla efektywnej aktualizacji okna
   - Jednoczesne przetwarzanie i wyświetlanie

2. **Zarządzanie pamięcią**:
   - Usuwanie obiektów poza ekranem
   - Czyszczenie list przy restarcie

3. **Detekcja dłoni**:
   - Ograniczenie do jednej dłoni
   - Optymalne ustawienia pewności detekcji

## Obsługa Błędów

- Sprawdzanie dostępności kamery przy inicjalizacji
- Obsługa błędów odczytu klatki
- Informacje o błędach w języku polskim
- Bezpieczne zamykanie zasobów

## Możliwe Rozszerzenia

1. **Różne poziomy trudności** - regulowane prędkości i częstotliwości
2. **Power-upy** - specjalne obiekty z bonusami
3. **Efekty dźwiękowe** - dźwięki przy zbieraniu i kolizjach
4. **Tablica wyników** - zapisywanie najlepszych wyników
5. **Więcej postaci** - wybór różnych piłkarzy
6. **Animacje** - płynniejsze ruchy i przejścia
7. **Multiplayer** - rywalizacja dwóch graczy
