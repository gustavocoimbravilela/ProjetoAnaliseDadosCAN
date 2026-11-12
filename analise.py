# Código que analise o log e extrai dados interessantes dele.

# Carregar os dados do log
import pandas as pd

arquivo = '2014_KW_T270_Starting_CSU090B6.txt'

df = pd.read_csv(
    arquivo,
    sep = r'[ #]', # separa por espaço e '#'
    engine = 'python',
    header=None,
    names=['timestamp', 'channel', 'can_id', 'data']
)

# Limpa o timestamp "(1594703731)" -> float
df['timestamp'] = df['timestamp'].str.strip('()').astype(float)

# tempo relativo ao início (segundos)
df['t'] = df['timestamp'] - df['timestamp'].iloc[0]

df['id_int'] = df['can_id'].apply(int, base=16) # converte as strings para números
df['priority'] = (df['id_int'] >>  26) &  0x7  # Descarta os primeiros 26 bits e seleciona apenas os 3 primeiros dos que sobraram