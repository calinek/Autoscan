# Autoscan
AutoScout24 Scraper to narzędzie napisane w Pythonie, które automatycznie skrapuje dane o pojazdach z platformy AutoScout24. Używa Selenium WebDriver do nawigacji po stronach, ekstrakcji danych i zapisywania ich w postaci struktur danych Pandas, które następnie mogą być zapisane do pliku CSV.


markdown
Copy code
# AutoScout24 Scraper

## Opis projektu
AutoScout24 Scraper to narzędzie napisane w Pythonie, które automatycznie skrapuje dane o pojazdach z platformy AutoScout24. Używa Selenium WebDriver do nawigacji po stronach, ekstrakcji danych i zapisywania ich w postaci struktur danych Pandas, które następnie mogą być zapisane do pliku CSV.

## Funkcje
- Skrapowanie danych dotyczących pojazdów (marka, model, przebieg, typ paliwa, rok pierwszej rejestracji, cena).
- Możliwość określenia parametrów wyszukiwania, takich jak marka, model, rok produkcji, moc i rodzaj paliwa.
- Zapisywanie wyników do pliku CSV dla dalszej analizy.
- Obsługa paginacji wyników wyszukiwania.

## Wymagania
- Python 3.6+
- Selenium
- Pandas
- ChromeDriver (lub odpowiedni sterownik przeglądarki)

## Instalacja
git clone https://github.com/yourusername/autoscout24-scraper.git
cd autoscout24-scraper
pip install -r requirements.txt

python
Copy code

## Szybki start
```python
from AutoScan24 import AutoScan24

# Utwórz instancję skrapera z wybranymi parametrami
scraper = AutoScan24(make='honda', model='civic', version='', year_from=2015, year_to=2020,
                     power_from=50, power_to=200, powertype='hp')

# Skrapuj dane z pierwszych 5 stron
scraper.scrape(num_pages=5)

# Zapisz wyniki do pliku CSV
scraper.save_to_csv('wyniki.csv')

# Zamknij przeglądarkę
scraper.quit_browser()
Licencja
Ten projekt jest dostępny pod licencją MIT. Zobacz plik LICENSE dla pełnych informacji.

Wkład w projekt
Jeśli chcesz przyczynić się do tego projektu, są mile widziane pull requesty. Prosimy o utworzenie issue przed wysłaniem pull requestu.

Autorzy
Michał, Mateusz, Michał - Inicjatywa i rozwój projektu


Kontakt
Jeśli masz jakiekolwiek pytania lub sugestie, prosimy o kontakt przez GitHub Issues.

© 2024 . Wszystkie prawa zastrzeżone.
