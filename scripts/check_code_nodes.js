const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
for (const file of fs.readdirSync(path.join(root, 'workflows'))) {
  const workflow = JSON.parse(fs.readFileSync(path.join(root, 'workflows', file)));
  for (const node of workflow.nodes.filter(n => n.type === 'n8n-nodes-base.code')) {
    const input = [{ json: { event_id: 'smoke', needs_review: true, status: 'pending_review' } }];
    const result = new Function('$input', node.parameters.jsCode)({ all: () => input });
    if (result.length !== 1 || result[0].json.event_id !== 'smoke' || !result[0].json.route) throw new Error(node.name);
    if (node.name === 'Prepared outbox') {
      const rejected = new Function('$input', node.parameters.jsCode)({ all: () => [{json:{status:'rejected'}}] });
      if (rejected[0].json.route !== 'rejected') throw new Error('Rejected ticket routing');
    }
    console.log(node.name + ': code execution passed');
  }
}
