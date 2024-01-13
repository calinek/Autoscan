from Miner.AutoScan24 import AutoScan24
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import plotly.express as px
import os

def get_data_from_note(nazwa_pliku):
    try:
        with open(nazwa_pliku, 'r') as file:
            lines = file.readlines()

        data = {}
        for line in lines:
            key, *value = line.strip().split(' = ')
            data[key] = ' '.join(value) if value else ''

        marka_input = data.get('make', '')
        model_input = data.get('model', '')
        version_input = data.get('version', '')
        year_from_input = data.get('year_from', '')
        year_to_input = data.get('year_to', '')
        power_from_input = data.get('power_from', '')
        power_to_input = data.get('power_to', '')
        powertype_input = data.get('powertype', '')

        return marka_input, model_input, version_input, year_from_input, year_to_input, power_from_input, power_to_input, powertype_input

    except Exception as e:
        print(f"Error reading data from {nazwa_pliku}: {e}")
        return '', '', '', '', '', '', '', ''

if __name__ == "__main__":
    num_pages = 20
    downloaded_listings_file = f'listings/Results.csv'

    if not os.path.exists("listings"):
        os.makedirs("listings")

    
    nazwa_pliku_notatnika = 'INPUT.txt'
    marka_input, model_input, version_input, year_from_input, year_to_input, power_from_input, power_to_input, powertype_input = get_data_from_note(nazwa_pliku_notatnika)

    
    scraper = AutoScan24(marka_input, model_input, version_input, year_from_input, year_to_input, power_from_input, power_to_input, powertype_input)
    scraper.scrape(num_pages, True)
    scraper.save_to_csv(downloaded_listings_file)
    scraper.quit_browser()







# Wczytanie danych z pliku CSv
data = pd.read_csv('listings/Results.csv')

# Konwersja daty pierwszej rejestracji na format daty i konwersja przebiegu i ceny na numeryczne
data['first-registration'] = pd.to_datetime(data['first-registration'], format='%m-%Y')
data['mileage'] = pd.to_numeric(data['mileage'], errors='coerce')
data['price'] = pd.to_numeric(data['price'], errors='coerce')

# Podstawowe statystyki
basic_statistics = data.describe()

# Zapisanie podstawowych statystyk do pliku CSV
basic_statistics.to_csv('listings/Basic_Statistics.csv')

# Ustawienia wykresów
sns.set(style="whitegrid")

# Wykres pudełkowy przebiegu
plt.figure(figsize=(10, 6))
sns.boxplot(data['mileage'])
plt.title('Wykres pudełkowy przebiegu')
plt.xlabel('Przebieg (km)')
plt.ylabel('Rozkład wartości')
plt.savefig('listings/Mileage_Boxplot.jpg')

# Wykres pudełkowy cen
plt.figure(figsize=(10, 6))
sns.boxplot(data['price'])
plt.title('Wykres pudełkowy cen')
plt.xlabel('Cena (EUR)')
plt.ylabel('Rozkład wartości')
plt.savefig('listings/Price_Boxplot.jpg')

# Wykres liniowy roku pierwszej rejestracji vs cena
year_price_avg = data.groupby(data['first-registration'].dt.year)['price'].mean().reset_index()
plt.figure(figsize=(10, 6))
sns.lineplot(x='first-registration', y='price', data=year_price_avg)
plt.title('Średnia cena w zależności od roku pierwszej rejestracji')
plt.xlabel('Rok pierwszej rejestracji')
plt.ylabel('Średnia cena (EUR)')
plt.savefig('listings/Year_vs_Price_Line_Plot.jpg')

# Wykres rozrzutu przebieg vs cena z linią trendu
plt.figure(figsize=(10, 6))
sns.scatterplot(x='mileage', y='price', data=data)
sns.regplot(x='mileage', y='price', data=data, scatter=False, color='red')
plt.title('Wykres rozrzutu - Przebieg vs Cena z linią trendu')
plt.xlabel('Przebieg (km)')
plt.ylabel('Cena (EUR)')
plt.savefig('listings/Mileage_vs_Price_Scatter_with_Trendline.jpg')

# Wykres słupkowy ilości pojazdów w zależności od roku pierwszej rejestracji
count_year = data['first-registration'].dt.year.value_counts().sort_index().reset_index()
count_year.columns = ['year', 'count']
plt.figure(figsize=(12, 8))
sns.barplot(x='year', y='count', data=count_year)
plt.title('Liczba pojazdów w zależności od roku pierwszej rejestracji')
plt.xlabel('Rok pierwszej rejestracji')
plt.ylabel('Liczba pojazdów')
plt.savefig('listings/Count_by_Year_Bar_Plot.jpg')
