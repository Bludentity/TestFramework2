import csv
from pathlib import Path
from typing import List


def load_search_terms(csv_path: str = None) -> List[str]:
    root = Path(__file__).resolve().parent.parent
    data_dir = root / 'data'
    if csv_path:
        path = Path(csv_path)
    else:
        path = data_dir / 'search_terms.csv'

    if not path.exists():
        return []

    terms: List[str] = []
    with path.open(newline='', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            val = row.get('search_term') or row.get('term')
            if val:
                terms.append(val.strip())
    return terms
