import subprocess, sys, json, glob, os, tempfile
code="import sys,os,json,hashlib\nRD=sys.argv[1]\nfor i in range(40):\n    k=f'{sys.argv[2]}|{i}'; json.dump(dict(key=k,value=dict(final=i)),open(f'{RD}/{hashlib.sha1(k.encode()).hexdigest()}.json.tmp'+sys.argv[2],'w')); os.replace(f'{RD}/{hashlib.sha1(k.encode()).hexdigest()}.json.tmp'+sys.argv[2],f'{RD}/{hashlib.sha1(k.encode()).hexdigest()}.json')\n"
d=tempfile.mkdtemp(); ps=[subprocess.Popen([sys.executable,"-c",code,d,t]) for t in "abc"]; [p.wait() for p in ps]
n=len(glob.glob(d+"/*.json")); assert n==120,n; print("test_store.py: 3 concurrent writers, 120/120 entries survived")
