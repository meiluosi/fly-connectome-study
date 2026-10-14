"""Map MaleCNS MB compartment label strings to canonical lobe compartments.
Primary = tokens before '>' or '<'; secondary after. Unparsed leftovers are reported, not guessed."""
import re
TOK=re.compile(r"(y\d|B'\d|B\d|a'\d|a\d)")
def canon(label):
    if label is None: return None
    s=label.replace("_bilateral","").replace("b'","B'")
    if s=="a2p3p": s="a2a3"  # alpha2 posterior + alpha3 posterior; subregion dropped
    s=s.replace("a/B","")  # lobe-level secondary target, not a compartment
    if s=="calyx": return {"primary":["calyx"],"secondary":[],"left":""}
    parts=re.split(r"[><]",s)
    prim=TOK.findall(parts[0]); sec=[t for p in parts[1:] for t in TOK.findall(p)]
    # strip tokens to find unexplained remainder
    rem=TOK.sub("",s); rem=re.sub(r"ped[c]?|[a-z]{1,2}|[<>/\d]","",rem)
    return {"primary":prim,"secondary":sec,"left":rem}
