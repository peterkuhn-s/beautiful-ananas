import subprocess
import re
import pandas as pd
import matplotlib.pyplot as plt

def get_commit_messages():
    command = ['git', 'log', '--pretty=%s']
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    return result.stdout.splitlines()

def extract_date(commit_message):
    match = re.search(r'(\d{4}-\d{2}-\d{2})', commit_message)
    if match:
        return pd.to_datetime(match.group(1))
    return None

def extract_minutes(commit_message):
    match = re.search(r'(\d+)', commit_message)
    if match:
        return int(match.group(1))
    return 0

def calculate_total_minutes(commit_messages):
    daily_minutes = {}
    for message in commit_messages:
        date = extract_date(message)
        if date:
            minutes = extract_minutes(message)
            daily_minutes[date] = daily_minutes.get(date, 0) + minutes
    return daily_minutes

def calculate_total_minutes_old(commit_messages):
    total_minutes = 0
    for message in commit_messages:
        total_minutes += extract_minutes(message)
    return total_minutes

def initialize_pd_data():
    # Create date range from '2024-02-19' to '2024-06-14'
    date_range = pd.date_range(start='2024-02-19', end='2024-06-14', freq='D')

    # Initialize DataFrame with zeros in the second column
    df = pd.DataFrame(data={'Date': date_range, 'Minutes': 0})

    # Set 'Date' column as index
    df.set_index('Date', inplace=True)

    return df

if __name__ == '__main__':
    # Initialize DataFrame with zeros for each day
    df = initialize_pd_data()

    # Get commit messages and calculate daily minutes
    commit_messages = get_commit_messages()
    daily_minutes = calculate_total_minutes(commit_messages)

    # Update DataFrame with daily minutes
    for date, minutes in daily_minutes.items():
        df.loc[date, 'Minutes'] = minutes

    # Convert total minutes to hours
    total_hours = df['Minutes'].sum() / 60

    total_minutes = calculate_total_minutes_old(commit_messages)
    total_hours = total_minutes / 60
    print(f'Total minutes spent on commits: {total_hours} hours')

    
        # Display DataFrame and total minutes
    print("Daily minutes spent on commits:")
    print(df)
    print(f'Total minutes spent on commits: {df["Minutes"].sum()} minutes')


    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['Minutes'], marker='o', linestyle='-')
    plt.yscale('log')
    plt.title(f'Daily minutes spent on commits: Total = {total_hours:.2f} hours')
    plt.xlabel('Date')
    plt.ylabel('Minutes (log scale)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
