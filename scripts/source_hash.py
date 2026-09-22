from pathlib import Path
import hashlib
p=Path('contracts/verid.py')
print('contracts/verid.py sha256:',hashlib.sha256(p.read_bytes()).hexdigest())
