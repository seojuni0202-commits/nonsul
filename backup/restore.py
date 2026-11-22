# 백업 풀기: python3 backup/restore.py <사이트 비밀번호> <풀 폴더>
# 저장소 루트(key.json 이 있는 곳)에서 실행한다. 필요: pip install cryptography
import sys,json,base64,hashlib,io,tarfile,os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
pw,dest=sys.argv[1],sys.argv[2]
here=os.path.dirname(os.path.abspath(__file__));root=os.path.dirname(here)
k=json.load(open(root+'/key.json'))
kek=PBKDF2HMAC(hashes.SHA256(),32,base64.b64decode(k['salt']),k['iter']).derive(pw.encode())
DK=AESGCM(kek).decrypt(base64.b64decode(k['iv']),base64.b64decode(k['wrapped']),None)
info=json.load(open(here+'/info.json'));A=AESGCM(DK);raw=b''
for n in range(info['parts']):
    b=open(f'{here}/part-{n:02d}.bin','rb').read();raw+=A.decrypt(b[:12],b[12:],None)
assert hashlib.sha256(raw).hexdigest()==info['sha256'],'백업이 손상됨'
os.makedirs(dest,exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(raw),mode='r:gz') as t: t.extractall(dest,filter='data')
print('풀었음:',dest,'파일',info['files'])
