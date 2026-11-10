from pathlib import Path
import pandas as pd

root = Path(__file__).resolve().parents[1]   # folderul Licenta
df = pd.read_csv(root / "data" / "dataset.csv").set_index("filestem")

for p in sorted((root / "data" / "sample" / "labels").glob("*.txt")):
    ids = sorted({l.split()[0] for l in p.read_text().splitlines() if l.strip()})
    print(p.stem, ids, "fracture_visible =", df.loc[p.stem, "fracture_visible"])