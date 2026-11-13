"""Conservative scan for account identifiers and accidental local paths."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
SUFFIXES={'.md','.py','.txt','.yml','.yaml','.json','.toml','.csv','.gitignore'}
PATTERNS={
 'email-address': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'),
 'local-windows-user-path':re.compile(r'[A-Za-z]:\\Users\\[^\\/\s]+'),
 'local-unix-user-path':re.compile(r'/(?:home|Users)/[A-Za-z0-9_.-]+/'),
 'known-api-key-format':re.compile(r'\b(?:sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,})\b')
}
def main():
    failures=[]
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file() or path.suffix not in SUFFIXES:continue
        if any(x in ('.git','.venv','scratch','__pycache__') for x in path.parts):continue
        txt=path.read_text('utf-8',errors='replace')
        for label,pattern in PATTERNS.items():
            if pattern.search(txt):failures.append((str(path.relative_to(ROOT)),label))
    if failures:raise AssertionError('Potential personal/private identifiers: '+repr(failures))
    print('PASS: no emails, machine-user directories, or obvious secret token patterns in public text')
if __name__=='__main__':main()
