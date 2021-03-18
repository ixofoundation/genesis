import json

in_file = 'exported.json'
out_file = 'genesis.json'

# Load genesis
with open(in_file, 'r') as f:
    data = json.load(f)

# Migrate auth/accounts
data['app_state']['auth']['accounts'] = []
accs = data['app_state']['accounts']
for i, _ in enumerate(accs):
    acc = accs[i]
    is_module_account = acc['module_name'] != ""
    is_continuous_vesting_account = acc['start_time'] != "0" and acc['end_time'] != "0"
    is_delayed_vesting_account = acc['end_time'] != "0"
    if is_module_account:
        new_acc = {
            "type": "cosmos-sdk/ModuleAccount",
            "value": {
                "account_number": acc['account_number'],
                "address": acc['address'],
                "coins": acc['coins'],
                "name": acc['module_name'],
                "permissions": acc['module_permissions'],
                "public_key": "",
                "sequence": acc['sequence_number']
            }
        }
    elif is_continuous_vesting_account:
        new_acc = {
            "type": "cosmos-sdk/ContinuousVestingAccount",
            "value": {
                "account_number": acc['account_number'],
                "address": acc['address'],
                "coins": acc['coins'],
                "delegated_free": acc['delegated_free'],
                "delegated_vesting": acc['delegated_vesting'],
                "end_time": acc['end_time'],
                "original_vesting": acc['original_vesting'],
                "public_key": None,
                "sequence": acc['sequence_number'],
                "start_time": acc['start_time']
            }
        }
    elif is_delayed_vesting_account:
        new_acc = {
            "type": "cosmos-sdk/DelayedVestingAccount",
            "value": {
                "account_number": acc['account_number'],
                "address": acc['address'],
                "coins": acc['coins'],
                "delegated_free": acc['delegated_free'],
                "delegated_vesting": acc['delegated_vesting'],
                "end_time": acc['end_time'],
                "original_vesting": acc['original_vesting'],
                "public_key": None,
                "sequence": acc['sequence_number']
            }
        }
    else:
        new_acc = {
            "type": "cosmos-sdk/Account",
            "value": {
                "account_number": acc['account_number'],
                "address": acc['address'],
                "coins": acc['coins'],
                "public_key": None,
                "sequence": acc['sequence_number']
            }
        }
    data['app_state']['auth']['accounts'].append(new_acc)
del data['app_state']['accounts']

# Migrate distribution
data['app_state']['distribution']['params'] = {
    "base_proposer_reward": data['app_state']['distribution']['base_proposer_reward'],
    "bonus_proposer_reward": data['app_state']['distribution']['bonus_proposer_reward'],
    "community_tax": data['app_state']['distribution']['community_tax'],
    "withdraw_addr_enabled": data['app_state']['distribution']['withdraw_addr_enabled'],
}
del data['app_state']['distribution']['base_proposer_reward']
del data['app_state']['distribution']['bonus_proposer_reward']
del data['app_state']['distribution']['community_tax']
del data['app_state']['distribution']['withdraw_addr_enabled']

# Migrate evidence
data['app_state']['evidence'] = {
    "evidence": None,
    "params": {
        "max_evidence_age": data['app_state']['slashing']['params'][
            'max_evidence_age']
    }
}

# Migrate genutil
data['app_state']['genutil'] = {
    "gentxs": []
}

# Migrate gov
if len(data['app_state']['gov']['proposals']) == 0:
    data['app_state']['gov']['proposals'] = None

# Migrate project
data['app_state']['project']['claims'] = []

# Migrate slashing
del data['app_state']['slashing']['params']['max_evidence_age']

# Migrate staking
data['app_state']['staking']['params']['historical_entries'] = 0
validators = data['app_state']['staking']['validators']
for i, _ in enumerate(validators):
    validators[i]['description']['security_contact'] = ""

# Migrate upgrade
data['app_state']['upgrade'] = {}

# Update chain ID
data['chain_id'] = 'impacthub-2'

# Update genesis time
data['genesis_time'] = '2021-03-23T12:00:00Z'

# Migrate evidence consensus params
data['consensus_params']['evidence']['max_age_num_blocks'] = \
data['consensus_params']['evidence']['max_age']
del data['consensus_params']['evidence']['max_age']
data['consensus_params']['evidence']['max_age_duration'] = "172800000000000"

# Finishing touches (replace & with unicode)
data = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)
data = data.replace('&', '\\u0026')

# Output migrated genesis
with open(out_file, 'w') as f:
    f.write(data)
