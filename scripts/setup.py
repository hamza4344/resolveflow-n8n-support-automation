from pathlib import Path
import secrets
root=Path(__file__).resolve().parents[1]
path=root/'.env'
if path.exists():
    raise SystemExit('.env already exists; refusing to overwrite your settings')
text=(root/'.env.example').read_text()
for name in ('API_TOKEN','REVIEWER_TOKEN','N8N_ENCRYPTION_KEY'):
    text='\n'.join(name+'='+secrets.token_hex(32) if line.startswith(name+'=') else line for line in text.split('\n'))
path.write_text(text)
path.chmod(0o600)
print('Configuration generated. Start with docker compose up --build -d')
