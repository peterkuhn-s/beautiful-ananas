import subprocess
import re
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

def get_commit_messages():
    command = ['git', 'log', '--pretty=%s %ct']
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    return result.stdout.splitlines()

def extract_date_and_minutes(commit_message):
    match = re.search(r'(\d+) (.+?) (\d+)$', commit_message)
    if match:
        minutes = int(match.group(1))
        unix_timestamp = int(match.group(3))
        date = pd.to_datetime(unix_timestamp, unit='s').strftime('%Y-%m-%d')
        return date, minutes
    return None, 0

def calculate_total_minutes(commit_messages):
    daily_minutes = {}
    for message in commit_messages:
        date, minutes = extract_date_and_minutes(message)
        if date:
            daily_minutes[date] = daily_minutes.get(date, 0) + minutes
    return daily_minutes

def initialize_pd_data():
    # Create date range from '2024-02-19' to '2024-06-14'
    date_range = pd.date_range(start='2024-02-19', end='2024-06-14', freq='D')

    # Initialize DataFrame with zeros in the second column
    df = pd.DataFrame(data={'Date': date_range, 'Minutes': 0})

    # Set 'Date' column as index
    df.set_index('Date', inplace=True)

    return df

if __name__ == '__main__':
    commit_messages = get_commit_messages()
    daily_minutes = calculate_total_minutes(commit_messages)

    df = initialize_pd_data()

    # Update DataFrame with daily minutes
    for date, minutes in daily_minutes.items():
        df.loc[date, 'Minutes'] = minutes

    # Convert total minutes to hours
    total_hours = df['Minutes'].sum() / 60
    print(f'Total hours spent on commits: {total_hours:.2f} hours')

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.bar(df.index, df['Minutes'], color='skyblue')
    plt.yscale('log')
    
    # Set y-axis to use base 10 instead of exponential notation
    plt.gca().yaxis.set_major_formatter(ScalarFormatter())
    
    plt.title(f'Daily minutes spent on commits: Total = {total_hours:.2f} hours')
    plt.xlabel('Date')
    plt.ylabel('Minutes')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
