import pandas as pd
import os

# Caminho para a pasta onde estão os ficheiros CSV
pasta_csvs = "C:/Users/joaoc/Desktop/ATP_JAPAO_FINAL/SCRIPT_ADICIONAL_MATCHES"

# Lista todos os ficheiros CSV na pasta
ficheiros = [f for f in os.listdir(pasta_csvs) if f.endswith('.csv')]

# Lê e junta todos os ficheiros num único DataFrame
df_total = pd.concat([pd.read_csv(os.path.join(pasta_csvs, f)) for f in ficheiros], ignore_index=True)

# Guarda o resultado num novo ficheiro
df_total.to_csv("EXTERNAL_matches.csv", index=False)