import subprocess
import re

def get_commit_messages():
    command = ['git', 'log', '--pretty=%s']
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    return result.stdout.splitlines()

def extract_minutes(commit_message):
    match = re.search(r'(\d+)', commit_message)
    if match:
        return int(match.group(1))
    return 0

def calculate_total_minutes(commit_messages):
    total_minutes = 0
    for message in commit_messages:
        total_minutes += extract_minutes(message)
    return total_minutes

if __name__ == '__main__':
    commit_messages = get_commit_messages()
    total_minutes = calculate_total_minutes(commit_messages)
    total_hours = total_minutes / 60
    print(f'Total minutes spent on commits: {total_hours} hours')
