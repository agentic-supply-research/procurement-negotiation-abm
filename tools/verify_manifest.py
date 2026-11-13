"""Verify byte-level integrity of the archived derived input and output artifacts."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    obj=json.loads((ROOT/'metadata_manifest.json').read_text())
    for rec in obj['files']:
        p=ROOT/rec['file']
        if not p.is_file(): raise FileNotFoundError(rec['file'])
        if p.stat().st_size != rec['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=rec['sha256']:
            raise AssertionError(f'File corrupted or changed: {rec["file"]}')
    print(f'PASS: {len(obj["files"])} archived input/result files match SHA-256 manifest')
if __name__=='__main__': main()
