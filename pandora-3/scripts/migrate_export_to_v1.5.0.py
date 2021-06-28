import json

in_file = 'exported.json'
out_file = 'genesis.json'

# Load genesis
with open(in_file, 'r') as f:
    data = json.load(f)


# Migrating auth
# Removing treasury module account, adding transfer module account
found_treasury = False

for acc in data['app_state']['auth']['accounts']:
    if acc['@type'] == "/cosmos.auth.v1beta1.ModuleAccount" and acc['name'] == "treasury":
        found_treasury = True
        acc['name'] = "transfer"
        acc['base_account']['address'] = "ixo1yl6hdjhmkf37639730gffanpzndzdpmh32gmns"

if not found_treasury:
    raise Exception("Did not find treasury account in exported.json.")


# Migrating bonds
for batch in data['app_state']['bonds']['batches']:
    if batch['buy_prices'] == None:
        batch['buy_prices'] = []
    if batch['buys'] == None:
        batch['buys'] = []
    if batch['sell_prices'] == None:
        batch['sell_prices'] = []
    if batch['sells'] == None:
        batch['sells'] = []
    if batch['swaps'] == None:
        batch['swaps'] = []

for bond in data['app_state']['bonds']['bonds']:
    if bond['function_parameters'] == None:
        bond['function_parameters'] = []

if data['app_state']['bonds']['params']['reserved_bond_tokens'] == None:
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

    if el['value']['credentials'] != None:
        for cred in el['value']['credentials']:
            cred['claim']['KYC_validated'] = cred['claim']['KYCValidated']
            del cred['claim']['KYCValidated']

            cred['cred_type'] = cred['type']
            del cred['type']

    if el['value']['credentials'] == None:
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
                            "connection_genesis" : {"client_connection_paths": [], "connections": [], "next_connection_sequence": "0"}}                            
data['app_state']['ibc']['client_genesis']['params']['allowed_clients'].append("06-solomachine")
data['app_state']['ibc']['client_genesis']['params']['allowed_clients'].append("07-tendermint")


# Removing oracles
del data['app_state']['oracles']


# Adding params
data['app_state']['params'] = None


# Migrating payments
for temp in data['app_state']['payments']['payment_templates']:
    if temp['discounts'] == None:
        temp['discounts'] = []

if data['app_state']['payments']['subscriptions'] == None:
    data['app_state']['payments']['subscriptions'] = [] 


# Migrating project
if len(data['app_state']['project']['account_maps']) > 0:
    maps = []

    for map in data['app_state']['project']['account_maps']:
        maps.append(map)
        del map
        
    for i, map in enumerate(maps):
        data['app_state']['project']['account_maps'][i] = {"map": map}  

if len(data['app_state']['project']['claims']) > 0:
    claims = []

    for claims_list in data['app_state']['project']['claims']:
        claims.append(claims_list)
        del claims_list

    for i, claims_list in enumerate(claims):
        if claims_list == None:
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
        if wd_list == None:
            data['app_state']['project']['withdrawal_infos'][i] = {"docs_list": []}
        else:    
            data['app_state']['project']['withdrawal_infos'][i] = {"docs_list": wd_list}   

data['app_state']['project']['withdrawals_infos'] = data['app_state']['project']['withdrawal_infos']
del data['app_state']['project']['withdrawal_infos']            


# Removing treasury
del data['app_state']['treasury']


# Adding transfer
data['app_state']['transfer'] = {"denom_traces" : [], "params": {"receive_enabled": True, "send_enabled": True}, "port_id": "transfer"}


# Adding vesting
data['app_state']['vesting'] = {}


# Evidence
data['consensus_params']['evidence']['max_bytes'] = "1048576"


# Update chain ID
data['chain_id'] = 'pandora-3'


# Update genesis time
data['genesis_time'] = '2021-06-30T12:00:00Z'


# Finishing touches (replace & with unicode)
data = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)
data = data.replace('&', '\\u0026')

# Output migrated genesis
with open(out_file, 'w') as f:
    f.write(data)