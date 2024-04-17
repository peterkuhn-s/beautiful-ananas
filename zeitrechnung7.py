import subprocess
import re
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from gpt4all import GPT4All
import pickle

# Define the filename for the categorization cache file
CACHE_FILE = 'categorization_cache.pkl'

def load_categorization_cache():
    """Load the categorization cache from the persistent file."""
    try:
        with open(CACHE_FILE, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return {}

def save_categorization_cache(cache):
    """Save the categorization cache to the persistent file."""
    with open(CACHE_FILE, 'wb') as file:
        pickle.dump(cache, file)


def get_commit_messages():
    """Fetches commit messages and their timestamps using git log."""
    command = ['git', 'log', '--pretty=%s %ct']
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    return result.stdout.splitlines()




def extract_date_and_minutes(commit_message, cache):
    """Extracts date, minutes, and category from a commit message."""
    #print(commit_message)
    match = re.search(r'(\d*) (.+?) (\d+)$', commit_message)
    if match:
        minutes = int(match.group(1)) if match.group(1) else 0
        unix_timestamp = int(match.group(3))
        date = pd.to_datetime(unix_timestamp, unit='s').strftime('%Y-%m-%d')
        comment = str(match.group(2))
        category = categorise_message(comment, cache)
        return date, minutes, category
    return pd.Timestamp.now().strftime('%Y-%m-%d'), 0, None



def calculate_total_minutes(commit_messages, df, cache):
    """Calculates total minutes spent on each category."""
    for message in commit_messages:
        date, minutes, category = extract_date_and_minutes(message, cache)
        #print(date)
        if date:
            if category == 'A':
                df.loc[date, 'Minutes_Recherche_Planung'] += minutes
            elif category == 'B':
                df.loc[date, 'Minutes_Durchfuehrung_Umsetzung'] += minutes
            elif category == 'C':
                df.loc[date, 'Minutes_Dokumentation'] += minutes
            else:
                df.loc[date, 'Minutes_Sonstiges'] += minutes
    return df


def categorise_message(comment, cache):
    """Categorize the message using the cache if available, otherwise use GPT."""
    print(comment)
    if comment in cache:
        return cache[comment]
    else:
        try:
            # Call GPT function to categorize the message
            model = GPT4All("gpt4all-falcon-newbpe-q4_0.gguf")
            prompt = f"Kategorisiere die Arbeit '{comment}' in die folgenden Kategorien: A für Recherche und Planung, B für Durchführung und Umsetzung der Versuche, C für Dokumentation und D für Sonstiges."
            response = model.generate(prompt, max_tokens=3)
            category = parse_category_from_response(response)
            # Update cache
            cache[comment] = category
            save_categorization_cache(cache)
            print(category)
            return category
        except Exception as e:
            print(f"Error occurred while categorizing message: {e}")
            return None

def parse_category_from_response(response):
    """Parses the category from the API response."""
    if 'A' in response:
        return 'A'
    elif 'B' in response:
        return 'B'
    elif 'C' in response:
        return 'C'
    else:
        return 'D'



def initialize_pd_data():
    """Initializes the Pandas DataFrame with zeros and default values."""
    date_range = pd.date_range(start='2024-02-17', end='2024-06-14', freq='D')
    df = pd.DataFrame(data={'Minutes_Recherche_Planung': 0, 
                            'Minutes_Durchfuehrung_Umsetzung': 0, 
                            'Minutes_Dokumentation': 0, 
                            'Minutes_Sonstiges': 0, 
                            'Total_Minutes': 0,  # New column for total minutes
                            'Category': None}, 
                      index=date_range)
    return df

def plot_daily_minutes(df):
    """Plots the daily minutes spent on commits."""
    plt.figure(figsize=(10, 6))
    dates = df.index
    
    # Define the height of each category for each date
    Recherche_Planung = df['Minutes_Recherche_Planung']
    Durchfuehrung_Umsetzung = df['Minutes_Durchfuehrung_Umsetzung']
    Dokumentation = df['Minutes_Dokumentation']
    Sonstiges = df['Minutes_Sonstiges']
    
    # Plot stacked bars for each category
    plt.bar(dates, Recherche_Planung, color='blue', label='Recherche und Planung')
    plt.bar(dates, Durchfuehrung_Umsetzung, bottom=Recherche_Planung, color='green', label='Durchführung und Umsetzung')
    plt.bar(dates, Dokumentation, bottom=Recherche_Planung+Durchfuehrung_Umsetzung, color='orange', label='Dokumentation')
    plt.bar(dates, Sonstiges, bottom=Recherche_Planung+Durchfuehrung_Umsetzung+Dokumentation, color='red', label='Sonstiges')

    plt.yscale('log')
    # Set y-axis to use base 10 instead of exponential notation
    plt.gca().yaxis.set_major_formatter(ScalarFormatter())
    
    plt.legend(loc='upper left')
    plt.title(f'Daily minutes spent on commits: Total = {df["Total_Minutes"].sum() / 60:.2f} hours')
    plt.xlabel('Date')
    plt.ylabel('Minutes')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
if __name__ == '__main__':
    df = initialize_pd_data()
    commit_messages = get_commit_messages()
    #print(commit_messages)
    # Load categorization cache
    cache = load_categorization_cache()
    daily_minutes = calculate_total_minutes(commit_messages, df, cache)

    # Calculate total minutes by summing up all category columns
    df['Total_Minutes'] = df[['Minutes_Recherche_Planung', 
                              'Minutes_Durchfuehrung_Umsetzung', 
                              'Minutes_Dokumentation', 
                              'Minutes_Sonstiges']].sum(axis=1)

    # Plotting
    plot_daily_minutes(df)
    
    # Save categorization cache to pickle file
    save_categorization_cache(cache)

    # Print the contents of the cache
    print("Categorization cache:")
    for key, value in cache.items():
        print(f"Commit message: {key}, Category: {value}")
