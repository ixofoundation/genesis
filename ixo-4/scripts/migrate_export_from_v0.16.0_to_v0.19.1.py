import json
import base58
import datetime
import dateutil.parser


in_file = 'exported.json'
out_file = 'genesis.json'

# Load genesis
with open(in_file, 'r', encoding='utf-8') as f:
    data = json.load(f)


# Update chain ID
data['chain_id'] = 'ixo-4'

# Update genesis time
data['genesis_time'] = '2022-12-08T10:00:00Z'

# data['app_state']['gov']['voting_params']['voting_period'] = "600s"

data['app_state']['ibc']['connection_genesis']['params'] =  {
  "max_expected_time_per_block": "30000000000"
}

data['app_state']['authz'] = {
  "authorization": []
}

data['app_state']['token'] = {
  "Params": {
    "cw20ContractCode": "0",
    "cw721ContractCode": "0",
    "ixo1155ContractCode": "0"
  },
  "tokenMinters": []
}

data['app_state']['wasm'] = {
  "codes": [],
  "contracts": [],
  "gen_msgs": [],
  "params": {
    "code_upload_access": {
      "address": "",
      # "addresses": [],
      "permission": "Nobody"
    },
    "instantiate_default_permission": "Nobody"
  },
  "sequences": []
}

data['app_state']['entity'] = {
  "entity_docs": [],
  "params": {
    "NftContractAddress": "ixo14hj2tavq8fpesdwxxcu44rty3hh90vhujrvcmstl4zr3txmfvw9sqa3vn7",
    "NftContractMinter": "ixo14hj2tavq8fpesdwxxcu44rty3hh90vhujrvcmstl4zr3txmfvw9sqa3vn7"
  }
}

data['app_state']['entity'] = {
  "entity_docs": [],
  "params": {
    "NftContractAddress": "ixo14hj2tavq8fpesdwxxcu44rty3hh90vhujrvcmstl4zr3txmfvw9sqa3vn7",
    "NftContractMinter": "ixo14hj2tavq8fpesdwxxcu44rty3hh90vhujrvcmstl4zr3txmfvw9sqa3vn7"
  }
}

data['app_state']['iid'] = {'iid_docs': [], 'iid_meta': []}

for did in data['app_state']['did'].get('did_docs', []):
  iid = {
    "accordedRight": [],
    "alsoKnownAs": "",
    "assertionMethod": [],
    "authentication": [did['did']],
    "capabilityDelegation": [],
    "capabilityInvocation": [],
    "context": [],
    "controller": [did['did']],
    "id": did['did'],
    "keyAgreement": [],
    "linkedEntity": [],
    "linkedResource": [],
    "service": [],
    "verificationMethod": [{
        "controller": did['did'],
        "id": did['did'],
        "publicKeyBase58": did['pub_key'],
        "type": "Ed25519VerificationKey2018"
    },
    {
        "controller": did['did'] + "#" + did['pub_key'],
        "id": did['did'],
        "publicKeyBase58": did['pub_key'],
        "type": "Ed25519VerificationKey2018"
    }]
  }
  data['app_state']['iid']['iid_docs'].append(iid)

del data['app_state']['did']

def determineProjectTypeCode( projectType ):
  match projectType:
    case "Project":
      return "1"
    case "Investment":
      return "2"
    case "Oracle":
      return "3"
    case "Cell":
      return "4"
    case "Template":
      return '5'
    case "Asset":
      return '6'
    case "Dao":
      return '7'
    case _:
      return "0"

for project in data['app_state']['project'].get('project_docs', []) or []:
  iid = {
    "accordedRight": [],
    "alsoKnownAs": "",
    "assertionMethod": [],
    "authentication": [project['project_did']],
    "capabilityDelegation": [],
    "capabilityInvocation": [],
    "context": [],
    "controller": [project['project_did']],
    "id": project['project_did'],
    "keyAgreement": [],
    "linkedEntity": [],
    "linkedResource": [],
    "service": [],
    "verificationMethod": [{
        "controller": project['project_did'],
        "id": project['project_did'],
        "publicKeyBase58": did['pub_key'],
        "type": "Ed25519VerificationKey2018"
    },
    {
        "controller": project['project_did'] + "#" + did['pub_key'],
        "id": project['project_did'],
        "publicKeyBase58": did['pub_key'],
        "type": "Ed25519VerificationKey2018"
    }]
  }

  startDate = None
  try:
    startDate = dateutil.parser.isoparse(project['data'].get('startDate', None)).isoformat()
  except:
    print(project)

  endDate = None
  try:
    endDate = dateutil.parser.isoparse(project['data'].get('endDate', None)).isoformat()
  except:
    print(project)
  # datetime.datetime.fromisoformat('2022-09-26T00:00:00')

  if 'createdBy' in project['data']:
    iid['controller'].append(project['data']['createdBy'])
  elif 'creator' in project['data']:
     iid['controller'].append(project['data']['creator']['id'])
  else:
    print(project)

  for linkedEntity in project['data'].get("linkedEntities", []):
    iid['linkedEntity'].append({
      "id": linkedEntity['id'],
      "relationship": linkedEntity['@type']
    })

  meta = {
    "id": iid['id'],
    "created": project['data'].get('createdOn', None),
    "credentials": [],
    "deactivated": False,
    "endDate": endDate,
    "entityType": determineProjectTypeCode(project['data'].get('@type', 'project')),
    "relayerNode": project['data'].get('relayerNode', None),
    "stage": "1",
    "startDate": startDate,
    "status": 0,
    "updated": data['genesis_time'],
    "verifiableCredential": "",
    "versionId": "1"
  }

  data['app_state']['iid']['iid_docs'].append(iid)
  data['app_state']['iid']['iid_meta'].append(meta)


# for denomMeta in data['app_state']['bank']['denom_metadata']:
  # if denomMeta['name'] == '': denomMeta['name'] = denomMeta['display']
  # if denomMeta['symbol'] == '': denomMeta['symbol'] = denomMeta['display']

# Update initial height
data['initial_height'] = '1'

# Finishing touches (replace & with unicode)
data = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)
data = data.replace('&', '\\u0026')

# Output migrated genesis
with open(out_file, 'w', encoding='utf-8') as f:
    f.write(data)
