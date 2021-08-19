import json

in_file = 'exported_step_1.json'
out_file = 'genesis.json'

# Load genesis
with open(in_file, 'r') as f:
    data = json.load(f)

# ------------------------------------------------------------ 1.4.3 to 1.5.0

# Migrating auth
# Removing treasury module account, adding transfer module account
found_treasury = False

for acc in data['app_state']['auth']['accounts']:
    if acc['@type'] == "/cosmos.auth.v1beta1.ModuleAccount" and acc['name'] == "treasury":
        found_treasury = True
        acc['name'] = "transfer"
        acc['base_account']['address'] = "ixo1yl6hdjhmkf37639730gffanpzndzdpmh32gmns"

if not found_treasury:
    first_unused_acc_number = str(len(data['app_state']['auth']['accounts']))
    data['app_state']['auth']['accounts'].append(
        {
            '@type': '/cosmos.auth.v1beta1.ModuleAccount',
            'base_account': {
                'account_number': first_unused_acc_number,
                'address': 'ixo1yl6hdjhmkf37639730gffanpzndzdpmh32gmns',
                'pub_key': None,
                'sequence': '0'
            },
            'name': 'transfer',
            'permissions': ['minter', 'burner']
        }
    )

# Migrating bank
data['app_state']['bank']['denom_metadata'] = [
    {
        "base": "uatom",
        "denom_units": [
            {"aliases": ["microatom"], "denom": "uatom", "exponent": 0},
            {"aliases": ["milliatom"], "denom": "matom", "exponent": 3},
            {"aliases": [], "denom": "atom", "exponent": 6}
        ],
        "description": "The native staking token of the Cosmos Hub.",
        "display": "atom"
    },
    {
        "base": "uixo",
        "denom_units": [
            {"aliases": ["microixo"], "denom": "uixo", "exponent": 0},
            {"aliases": ["milliixo"], "denom": "mixo", "exponent": 3},
            {"aliases": [], "denom": "ixo", "exponent": 6}
        ],
        "description": "The native staking token of ixo.",
        "display": "ixo"
    },
]

# Migrating bonds
for batch in data['app_state']['bonds']['batches']:
    if batch['buy_prices'] is None:
        batch['buy_prices'] = []
    if batch['buys'] is None:
        batch['buys'] = []
    if batch['sell_prices'] is None:
        batch['sell_prices'] = []
    if batch['sells'] is None:
        batch['sells'] = []
    if batch['swaps'] is None:
        batch['swaps'] = []

for bond in data['app_state']['bonds']['bonds']:
    if bond['function_parameters'] is None:
        bond['function_parameters'] = []

if data['app_state']['bonds']['params']['reserved_bond_tokens'] is None:
    data['app_state']['bonds']['params']['reserved_bond_tokens'] = []

# Adding capability
data['app_state']['capability'] = {"index": "2", "owners": []}
data['app_state']['capability']['owners'].append({"index": "1", "index_owners": {"owners": []}})
data['app_state']['capability']['owners'][0]['index_owners']['owners'].append({"module": "ibc", "name": "ports/transfer"})
data['app_state']['capability']['owners'][0]['index_owners']['owners'].append({"module": "transfer", "name": "ports/transfer"})

# Migrating did
for el in data['app_state']['did']['did_docs']:
    el['@type'] = "/did.BaseDidDoc"
    del el['type']

    if el['value']['credentials'] is not None:
        for cred in el['value']['credentials']:
            cred['claim']['KYC_validated'] = cred['claim']['KYCValidated']
            del cred['claim']['KYCValidated']

            cred['cred_type'] = cred['type']
            del cred['type']

    if el['value']['credentials'] is None:
        el['value']['credentials'] = []

    el['credentials'] = el['value']['credentials']

    el['did'] = el['value']['did']

    el['pub_key'] = el['value']['pubKey']

    del el['value']

# Adding ibc
data['app_state']['ibc'] = {"channel_genesis": {"ack_sequences": [], "acknowledgements": [], "channels": [],
                                                "commitments": [], "next_channel_sequence": "0", "receipts": [], "recv_sequences": [],
                                                "send_sequences": []},
                            "client_genesis": {"clients": [], "clients_consensus": [], "clients_metadata": [],
                                               "create_localhost": False, "next_client_sequence": "0", "params": {"allowed_clients": []}},
                            "connection_genesis": {"client_connection_paths": [], "connections": [], "next_connection_sequence": "0"}}
data['app_state']['ibc']['client_genesis']['params']['allowed_clients'].append("07-tendermint")

# Removing oracles
del data['app_state']['oracles']

# Migrating payments
if data['app_state']['payments']['payment_templates'] is not None:
    for temp in data['app_state']['payments']['payment_templates']:
        if temp['discounts'] is None:
            temp['discounts'] = []

if data['app_state']['payments']['subscriptions'] is None:
    data['app_state']['payments']['subscriptions'] = []

# Migrating project
if len(data['app_state']['project']['account_maps']) > 0:
    maps = []

    for acc_map in data['app_state']['project']['account_maps']:
        maps.append(acc_map)
        del acc_map

    for i, acc_map in enumerate(maps):
        data['app_state']['project']['account_maps'][i] = {"map": acc_map}

if len(data['app_state']['project']['claims']) > 0:
    claims = []

    for claims_list in data['app_state']['project']['claims']:
        claims.append(claims_list)
        del claims_list

    for i, claims_list in enumerate(claims):
        if claims_list is None:
            data['app_state']['project']['claims'][i] = {"claims_list": []}
        else:
            data['app_state']['project']['claims'][i] = {"claims_list": claims_list}

for project_doc in data['app_state']['project']['project_docs']:
    project_doc['project_did'] = project_doc['projectDid']
    del project_doc['projectDid']

    project_doc['pub_key'] = project_doc['pubKey']
    del project_doc['pubKey']

    project_doc['sender_did'] = project_doc['senderDid']
    del project_doc['senderDid']

    project_doc['tx_hash'] = project_doc['txHash']
    del project_doc['txHash']

if len(data['app_state']['project']['withdrawal_infos']) > 0:
    wds = []

    for wd_list in data['app_state']['project']['withdrawal_infos']:
        wds.append(wd_list)
        del wd_list

    for i, wd_list in enumerate(wds):
        if wd_list is None:
            data['app_state']['project']['withdrawal_infos'][i] = {"docs_list": []}
        else:
            data['app_state']['project']['withdrawal_infos'][i] = {"docs_list": wd_list}

data['app_state']['project']['withdrawals_infos'] = data['app_state']['project']['withdrawal_infos']
del data['app_state']['project']['withdrawal_infos']

# Migrate staking
data['app_state']['staking']['exported'] = True

# Removing treasury
del data['app_state']['treasury']

# Adding transfer
data['app_state']['transfer'] = {"denom_traces": [], "params": {"receive_enabled": False, "send_enabled": False}, "port_id": "transfer"}


# Adding vesting
data['app_state']['vesting'] = {}

# Migrate evidence
data['consensus_params']['evidence']['max_bytes'] = "50000"

# ------------------------------------------------------------ 1.5.0 to 1.6.0

# Migrating bonds
for bond in data['app_state']['bonds']['bonds']:
    bond['reserve_withdrawal_address'] = bond['fee_address']
    bond['allow_reserve_withdrawals'] = False
    bond['available_reserve'] = bond['current_reserve']

# ------------------------------------------------------------ GENERAL


# Update chain ID
data['chain_id'] = 'impacthub-3'

# Update genesis time
data['genesis_time'] = '2021-08-19T12:00:00Z'

# Update initial height
data['initial_height'] = '1'

# Change max validators to 50 as indicated in:
# https://github.com/ixofoundation/governance/blob/main/proposals/001-stargate-upgrade/readme.md
data['app_state']['staking']['params']['max_validators'] = 50

# Finishing touches (replace & with unicode)
data = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)
data = data.replace('&', '\\u0026')

# Output migrated genesis
with open(out_file, 'w') as f:
    f.write(data)
