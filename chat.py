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
        comment = str(match.group(4))
        category = categorise_message(comment)
        return date, minutes, category

    return None

def calculate_total_minutes(commit_messages):
    daily_minutes = {}
    for message in commit_messages:
        date, minutes, category = extract_date_and_minutes(message)
        if date:
            daily_minutes.setdefault(date, {}).setdefault(category, 0)
            daily_minutes[date][category] += minutes
    return daily_minutes

def categorise_message(comment):
    model = GPT4All("em_german_mistral_v01.Q4_0.gguf")
    prompt = f"Kategorisiere die Arbeit '{comment}' in die folgenden Kategorien: A für Recherche und Planung, B für Durchführung und Umsetzung, C für Dokumentation und D für Sonstiges."
    response = model.generate(prompt, max_tokens=3)
    return response

def initialize_pd_data():
    # Create date range from '2024-02-19' to '2024-06-14'
    date_range = pd.date_range(start='2024-02-19', end='2024-06-14', freq='D')

    # Initialize DataFrame with zeros in the columns for each category
    categories = ['A', 'B', 'C', 'D']
    data = {category: [0] * len(date_range) for category in categories}
    df = pd.DataFrame(data, index=date_range)

    return df

if __name__ == '__main__':
    commit_messages = get_commit_messages()
    daily_minutes = calculate_total_minutes(commit_messages)

    df = initialize_pd_data()

    # Update DataFrame with daily minutes for each category
    for date, categories in daily_minutes.items():
        for category, minutes in categories.items():
            df.loc[date, category] = minutes

    # Convert total minutes to hours
    total_hours = df.sum().sum() / 60
    print(f'Total hours spent on commits: {total_hours:.2f} hours')

    # Plotting
    plt.figure(figsize=(10, 6))
    df.plot(kind='bar', stacked=True, ax=plt.gca(), color=['skyblue', 'salmon', 'lightgreen', 'orange'])
    plt.title(f'Daily minutes spent on commits: Total = {total_hours:.2f} hours')
    plt.xlabel('Date')
    plt.ylabel('Minutes')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
if __name__ == '__main__':
    df = initialize_pd_data()
    commit_messages = get_commit_messages()
    daily_minutes = calculate_total_minutes(commit_messages, df)

    # Calculate total minutes by summing up all category columns, buachsiashc
    df['Total_Minutes'] = df[['Minutes_Recherche_Planung', 
                              'Minutes_Durchfuehrung_Umsetzung', 
                              'Minutes_Dokumentation', 
                              'Minutes_Sonstiges']].sum(axis=1)

    # Convert total minutes to hours
    total_hours = df['Total_Minutes'].sum() / 60
    print(f'Total hours spent on commits: {total_hours:.2f} hours')

    # Plotting
    plt.figure(figsize=(10, 6))
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
