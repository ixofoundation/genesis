import json

in_file = 'exported.json'
out_file = 'genesis.json'

# Load genesis
with open(in_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update chain ID
data['chain_id'] = 'pandora-5'

# Update genesis time
data['genesis_time'] = '2022-07-014T10:00:00Z'

# Update initial height
data['initial_height'] = '1'

# Finishing touches (replace & with unicode)
data = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)
data = data.replace('&', '\\u0026')

# Output migrated genesis
with open(out_file, 'w', encoding='utf-8') as f:
    f.write(data)
