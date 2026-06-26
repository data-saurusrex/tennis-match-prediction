import pandas as pd
import glob

# Caminho onde estão os ficheiros
caminho = "C:/Users/joaoc/Desktop/ATP_JAPAO_FINAL/SCRIPT_ADICIONAL_RANKINGS"  
ficheiros = glob.glob(f"{caminho}/atp_rankings_*.csv")

# Lê e junta os ficheiros, ignorando cabeçalhos repetidos
dfs = []
for f in ficheiros:
    df = pd.read_csv(f)
    df = df[df["ranking_date"] != "ranking_date"]  # remove possíveis cabeçalhos no meio
    dfs.append(df)

# Junta todos num só DataFrame
df_total = pd.concat(dfs, ignore_index=True)

# Guarda num novo ficheiro CSV com um único cabeçalho
df_total.to_csv("EXTERNAL_rankings.csv", index=False)
