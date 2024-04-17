from gpt4all import GPT4All

model = GPT4All("em_german_mistral_v01.Q4_0.gguf")


# Definiere den Eingabetext
prompt = "Kategorisiere die Arbeit 'Messkonzept ausarbeiten' in die folgenden Kategorien: A für Recherche und Planung, B für Durchführung und Umsetzung, C für Dokumentation und D für Sonstiges."

# Rufe die API auf, um die Kategorisierung zu erhalten
response = model.generate(prompt, max_tokens=3)

# Gib die Antwort aus
print(response)
