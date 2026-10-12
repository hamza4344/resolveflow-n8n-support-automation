import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
for p in (root/'workflows').glob('*.json'):
    w=json.loads(p.read_text());names={n['name'] for n in w['nodes']}
    assert len(names)==len(w['nodes']), 'duplicate node names'
    assert not w['active']
    for name,connections in w['connections'].items():
        assert name in names
        for outputs in connections.values():
            for branch in outputs:
                for edge in branch:
                    assert edge['node'] in names
    for n in w['nodes']:
        if n['type'].endswith('webhook'):
            assert n['parameters']['authentication']=='headerAuth'
        assert not n.get('credentials'), 'do not ship user credential IDs'
    print(p.name+': structural checks passed (live n8n execution still required)')
