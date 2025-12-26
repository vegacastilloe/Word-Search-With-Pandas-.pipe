import pandas as pd

# 1. Función para parsear el texto a DataFrame
def parse_grid(raw: str) -> pd.DataFrame:
    raw = raw.strip().lstrip("={").rstrip("}").replace('"', '')
    rows = raw.split(";")
    matrix = [row.split(",") for row in rows]
    return pd.DataFrame(matrix)

# 2. Función para buscar palabras en el grid
def find_words_in_grid(grid: pd.DataFrame, words: list) -> pd.DataFrame:
    directions = [(0,1,'E'), (1,0,'S'), (1,1,'SE'), (-1,1,'NE')]

    def match_word(word, r0, c0, dr, dc):
        for i, ch in enumerate(word):
            r, c = r0 + i*dr, c0 + i*dc
            if r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1]:
                return False
            if grid.iat[r,c] != ch:
                return False
        return True

    results = []
    for w in words:
        found = False
        for r in range(grid.shape[0]):
            for c in range(grid.shape[1]):
                for dr, dc, dname in directions:
                    if match_word(w, r, c, dr, dc):
                        results.append({
                            'word': w,
                            'coordinate': (r+1, c+1),  # 1-based
                            'direction': dname
                        })
                        found = True
                        break
                if found: break
            if found: break
    return pd.DataFrame(results)

# 3. Uso correcto con pipeline
with open("/content/drive/MyDrive/sandbox/lnkd/Owen's python exercises/data/matriz.txt", "r") as f:
    raw = f.read()

words = ["CHRISTMAS","HOLLY","PEACE","NOEL","SANTA","ANGEL","BELLS","JOLLY","ELVES","GIFTS"]

df_result = (
    parse_grid(raw)                   # convierte string en DataFrame
    .pipe(find_words_in_grid, words)  # busca palabras con pipe
)

# 4. Selección final de columnas
df_final = (
  df_result
    .pipe(lambda d: d[['coordinate', 'direction']])
)

# 5. Validación contra dict esperado
expected = {
    'coordinate': {0: (1, 1), 1: (2, 2), 2: (3, 8), 3: (6, 3), 4: (8, 7), 5: (8, 8), 6: (11, 7), 7: (7, 1), 8: (8, 1), 9: (8, 6)}, 
    'direction': {0: 'SE', 1: 'E', 2: 'SE', 3: 'NE', 4: 'E', 5: 'S', 6: 'E', 7: 'E', 8: 'SE', 9: 'S'}
}
ok = (df_final.to_dict() == expected)

print(f'Match expected: 🐍✅ #{ok}\n')  # True si todo coincide
print(df_result[['coordinate', 'direction']].to_dict())
print(expected)
print(df_result)