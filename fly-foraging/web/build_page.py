import json, os
t=open("page_template.html").read(); d=open("data.json").read(); sim=open("sim.js").read()
assert "/*__DATA__*/null" in t and "/*__SIM__*/" in t
html=t.replace("/*__DATA__*/null",d).replace("/*__SIM__*/",sim); open("index.html","w").write(html); print("index.html bytes",os.path.getsize("index.html"))
