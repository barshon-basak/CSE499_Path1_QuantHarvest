"""Package portable code/results; exclude installed libraries and source renderings."""
from pathlib import Path
import hashlib,zipfile
ROOT=Path(__file__).resolve().parent

def included(p):
    rel=p.relative_to(ROOT)
    return (p.is_file() and not any(part in {'.deps','.venv','__pycache__','references'} for part in rel.parts)
            and p.name not in {'SHA256SUMS.txt','tests-before.txt'})

def main():
    files=sorted(p for p in ROOT.rglob('*') if included(p))
    hashes={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    sums=ROOT/'SHA256SUMS.txt'
    sums.write_text(''.join(f'{v}  {k}\n' for k,v in hashes.items()),encoding='utf-8')
    archive=ROOT.parent/'key-clustering-study.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in files+[sums]:
            z.write(p,arcname='key-clustering-study/'+p.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for name,digest in hashes.items():
            assert hashlib.sha256(z.read('key-clustering-study/'+name)).hexdigest()==digest
        assert len([n for n in z.namelist() if '/groups/' in n])==218
    print(f'{archive}\n{archive.stat().st_size:,} bytes\n{len(files)+1} files; all hashes verified')

if __name__=='__main__':main()
