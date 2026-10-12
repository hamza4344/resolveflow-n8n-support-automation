import json
import urllib.request
from pathlib import Path
root=Path(__file__).resolve().parents[1]
config=dict(line.split('=',1) for line in (root/'.env').read_text().splitlines() if line and not line.startswith('#') and '=' in line)
def call(path,file,token):
    req=urllib.request.Request('http://127.0.0.1:5678/webhook/resolveflow/'+path,data=(root/'examples'/file).read_bytes(),headers={'Content-Type':'application/json','X-API-Key':config[token]})
    with urllib.request.urlopen(req,timeout=65) as res:body=json.load(res)
    print(json.dumps(body,indent=2))
call('intake','ticket.json','API_TOKEN')
call('intake','ticket.json','API_TOKEN')
call('intake','billing.json','API_TOKEN')
call('review','review.json','REVIEWER_TOKEN')
