import json

in_file = 'exported.json'
out_file = 'genesis.json'

# Load genesis
with open(in_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Migrating bonds
for bond in data['app_state']['bonds']['bonds']:
    bond['reserve_withdrawal_address'] = bond['fee_address']
    bond['allow_reserve_withdrawals'] = False
    bond['available_reserve'] = bond['current_reserve']

# Update chain ID
data['chain_id'] = 'pandora-4'

# Update genesis time
data['genesis_time'] = '2021-08-01T12:00:00Z'

# Finishing touches (replace & with unicode)
data = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)
data = data.replace('&', '\\u0026')

# Output migrated genesis
with open(out_file, 'w', encoding='utf-8') as f:
    f.write(data)
