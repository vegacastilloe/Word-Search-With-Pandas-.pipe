# 🧠 Word Search con Pandas .pipe()
![License: MIT](https://img.shields.io/badge/License-MIT-cyan.svg)
![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![Last Updated](https://img.shields.io/github/last-commit/vegacastilloe/Customers-Table-With-Total-for-Each-Month)
![Language](https://img.shields.io/badge/language-español-darkred)

#
---
- 🎄 Christmas Excel Workout! 🎄
- 🌟 **Author**: Owen Price

    - ⭐Find the starting coordinate and direction of each of the words in the grid.
    - ⭐Use as many or as few formulas as you like. Or use a programming language of your choice!
    - ⭐To play on hard mode, dont't refer to the words in your solution - just find all the English words in the grid.

    - ⭐Words are only left-to-right or top-to-bottom.
      - E = East or horinzontal
      - S = South or vertical
      - SE = South-East or diagonally downwards from left to right
      - NE = North-East or diagonally upwards from left to right

🔗 You will find two array formulas in the following gist:

👉 https://lnkd.in/gRV95pje

#
#
**My code in Python** 🐍 **for this challenge**

  🔗 https://github.com/vegacastilloe/Word-Search-With-Pandas-.pipe/blob/main/word_search.py

  ---
  ---

Este README documenta paso a paso cómo resolví el - *word search* - publicado por **Owen Price**.

¿Existen mil maneras de resolverlo? Por supuesto. 

> Aquí mí manera, en la cual tome el archivo `*.txt` para formar el grid de 12×12 usando pandas 🐼 y el estilo funcional con .pipe(). 
Incluye: 
1. Explicación del código. 
2. Tabla comparativa de resultados y,
3.  tips de buenas prácticas.
 
---

# 🎯 Objetivo
- Parsear el archivo *.txt que contiene un grid 12×12 de letras.
- Buscar palabras en direcciones E (horizontal), S (vertical), SE (diagonal hacia abajo) y NE (diagonal hacia arriba).
- Devolver la coordenada inicial (fila, columna) y la dirección de cada palabra.
- Validar contra un diccionario esperado.

---

# 📜 Script paso a paso
```python
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
with open("/lnkd/data/matriz.txt", "r") as f:
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
```
---

# 📊 Tabla comparativa de resultados
|Word	| Coordinate |	Direction|
|:-----|:------------|:-----------|
|CHRISTMAS	| (1, 1) |	SE|
|HOLLY |	(2, 2) |	E|
|PEACE |	(3, 8) |	SE|
|NOEL |	(6, 3) |	NE|
|SANTA |	(8, 7) |	E|
|ANGEL |	(8, 8) |	S|
|BELLS |	(11, 7) |	E|
|JOLLY |	(7, 1) |	E|
|ELVES |	(8, 1) |	SE|
|GIFTS |	(8, 6) |	S|

---

# 💡 Buenas prácticas

- **Encapsula lógica en funciones:** `parse_grid` y `find_words_in_grid` son unidades testeables y reutilizables.
- **Usa** `.pipe()` **para claridad:** cada paso es explícito y encadenado, estilo funcional.
- **Valida resultados:** compara con un `dict expected` para asegurar exactitud.
- **Indices 1-based:** más intuitivo para puzzles, aunque pandas trabaje 0-based.
- **Rompe bucles temprano:** evita duplicados y mejora eficiencia.
- **Documenta direcciones como tuplas** `(dr, dc, nombre)`**:** fácil de extender si agregas NW, SW, etc.

---
### 📄 Licencia
---
Este proyecto está bajo ![License: MIT](https://img.shields.io/badge/License-MIT-cyan.svg). Puedes usarlo, modificarlo y distribuirlo libremente.

---
---
