import csv
import pickle

# Load data from the pickle file
with open('categorization_cache.pkl', 'rb') as file:
    data = pickle.load(file)

# Export the data to a CSV file
with open('categorization_cache.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for key, value in data.items():
        writer.writerow([key, value])

# Modify the data
data['epoxy graphit und alu mischen und messen'] = 'B'

# Import the modified data from the CSV file
modified_data = {}
with open('categorization_cache.csv', 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        modified_data[row[0]] = row[1]

# Save the modified data back to the pickle file
with open('categorization_cache.pkl', 'wb') as file:
    pickle.dump(modified_data, file)
