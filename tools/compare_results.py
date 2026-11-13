"""Compare archived numeric results with a separately regenerated CSV output set."""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]

def compare_csv(reference:Path,generated:Path,rtol=1e-9,atol=1e-9):
    a,b=pd.read_csv(reference),pd.read_csv(generated)
    if list(a.columns)!=list(b.columns):raise AssertionError(f'Column mismatch: {reference.name}')
    if len(a)!=len(b):raise AssertionError(f'Row count mismatch: {reference.name}: {len(a)} vs {len(b)}')
    cols=list(a.columns)
    # Outputs were created in deterministic order; compare within identical row ordering.
    for col in cols:
        x,y=a[col],b[col]
        if pd.api.types.is_numeric_dtype(x) and pd.api.types.is_numeric_dtype(y):
            np.testing.assert_allclose(x.to_numpy(),y.to_numpy(),rtol=rtol,atol=atol,equal_nan=True,err_msg=f'{reference.name}:{col}')
        elif not x.fillna('MISSING').equals(y.fillna('MISSING')):
            raise AssertionError(f'String/key column mismatch: {reference.name}:{col}')
    print(f'PASS {reference.name}: {len(a)} records')

def main():
    p=argparse.ArgumentParser();p.add_argument('--generated',type=Path,required=True)
    a=p.parse_args();src=ROOT/'results';g=a.generated
    files=sorted(g.glob('*.csv'))
    if not files:raise SystemExit('No CSV files found in the generated directory')
    for f in files:
        ref=src/f.name
        if not ref.exists():raise FileNotFoundError(ref)
        compare_csv(ref,f)

if __name__=='__main__':main()
