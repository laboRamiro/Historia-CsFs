import sys, re
base = sys.argv[1]
qfile = sys.argv[2]
books = {}
for n in range(1,7):
    lines = open(f"{base}/b{n}.txt", encoding="utf-8").read().split("\n")
    books[n] = lines
def locate(n, q):
    lines = books[n]
    chap = None
    for i,l in enumerate(lines):
        m = re.match(r"<<<ARCHIVO Text/(\w+)\.xhtml>>>", l)
        if m: chap = m.group(1)
        if q in l:
            return chap, i
    return None, None
ok=bad=0
for raw in open(qfile, encoding="utf-8"):
    raw=raw.rstrip("\n")
    if not raw.strip() or raw.startswith("#"): continue
    n, q = raw.split("|",1)
    n=int(n)
    chap, i = locate(n, q)
    if chap: ok+=1; print(f"OK  L{n} cap {chap}: {q[:70]}")
    else: bad+=1; print(f"FAIL L{n}: {q}")
print("ok",ok,"bad",bad)
