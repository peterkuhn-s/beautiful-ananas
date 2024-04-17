import subprocess
import re
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from gpt4all import GPT4All

def get_commit_messages():
    command = ['git', 'log', '--pretty=%s %ct']
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    return result.stdout.splitlines()

def extract_date_and_minutes(commit_message):
    match = re.search(r'(\d+) (.+?) (\d+) (\s)$', commit_message)
    if match:
        minutes = int(match.group(1))
        unix_timestamp = int(match.group(3))
        date = pd.to_datetime(unix_timestamp, unit='s').strftime('%Y-%m-%d')
        comment = str(match.group(2))
        categorie = categorise_mesage(comment)
        print(date, minutes, categorie)
        return date, minutes, categorie

    return None, 0



def calculate_total_minutes(commit_messages, df):
    for message in commit_messages:
        date, minutes, category = extract_date_and_minutes(message)
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


def categorise_mesage(comment):
    model = GPT4All("em_german_mistral_v01.Q4_0.gguf")
    # Definiere den Eingabetext
    prompt = f"Kategorisiere die Arbeit '{comment}' in die folgenden Kategorien: A für Recherche und Planung, B für Durchführung und Umsetzung, C für Dokumentation und D für Sonstiges."

    # Rufe die API auf, um die Kategorisierung zu erhalten
    response = model.generate(prompt, max_tokens=3)
    # Gib die Antwort aus
    print(response)
    return response


def initialize_pd_data():
    # Create date range from '2024-02-19' to '2024-06-14'
    date_range = pd.date_range(start='2024-02-19', end='2024-06-14', freq='D')

    # Initialize DataFrame with zeros in the minutes columns and 'Category' column with default value 'str'
    df = pd.DataFrame(data={'Date': date_range, 
                            'Minutes_Recherche_Planung': 0, 
                            'Minutes_Durchfuehrung_Umsetzung': 0, 
                            'Minutes_Dokumentation': 0, 
                            'Minutes_Sonstiges': 0, 
                            'Total_Minutes': 0,  # New column for total minutes
                            'Category': str}, 
                      index=date_range)

    return df



if __name__ == '__main__':
                              
    df = initialize_pd_data()
    commit_messages = get_commit_messages()
    daily_minutes = calculate_total_minutes(commit_messages, df)


    # Calculate total minutes by summing up all category columns
    df['Total_Minutes'] = df[['Minutes_Recherche_Planung', 
                              'Minutes_Durchfuehrung_Umsetzung', 
                              'Minutes_Dokumentation', 
                              'Minutes_Sonstiges']].sum(axis=1)

    # Convert total minutes to hours
    total_hours = df['Total_Minutes'].sum() / 60

    print(f'Total hours spent on commits: {total_hours:.2f} hours')

    # Plotting
    plt.figure(figsize=(10, 6))
 
    plt.yscale('log')
    
    # Set y-axis to use base 10 instead of exponential notation
    plt.gca().yaxis.set_major_formatter(ScalarFormatter())
    
    plt.stackplot(df.index, 
                  df['Minutes_Recherche_Planung'], 
                  df['Minutes_Durchfuehrung_Umsetzung'], 
                  df['Minutes_Dokumentation'], 
                  df['Minutes_Sonstiges'], 
                  labels=['Recherche und Planung', 
                          'Durchführung und Umsetzung', 
                          'Dokumentation', 
                          'Sonstiges'],
                  colors=['blue', 'green', 'orange', 'red'])  # Assign colors to each category
    plt.legend(loc='upper left')
    plt.title(f'Daily minutes spent on commits: Total = {total_hours:.2f} hours')
    plt.xlabel('Date')
    plt.ylabel('Minutes')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
