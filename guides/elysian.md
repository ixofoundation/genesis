
# Elysian

The project to setup Elysian.  It runs Node.js app using [Express 4](http://expressjs.com/) in a dockerized container.

## Running Elysian

Make sure you have [Docker](https://docker.com/) installed.

```sh
git clone https://github.com/ixofoundation/ixo_pds.git # or clone your own fork
cd ixo-pds/bin
install npm packages
./start.sh

***********************************
* ELYSIAN START                   *
***********************************

WARNING: The create command is deprecated. Use the up command with the --no-start flag instead.
Creating db ... done
Creating cache ... done
Creating mq    ... done
Creating pol   ... done
Creating cli   ... done
Creating app   ... done
Starting db ... done
Starting mq ... done
Starting cache ... done
Starting pol ... done
Starting app ... done
Starting Elysian ...done
Attaching to app
app      | register handler.createProject
app      | register handler.createAgent
app      | register handler.updateAgentStatus
app      | register handler.submitClaim
app      | register handler.evaluateClaim
app      | register handler.listClaims
app      | register handler.listAgents
app      | (node:17) [DEP0010] DeprecationWarning: crypto.createCredentials is deprecated. Use tls.createSecureContext instead.
app      | (node:17) [DEP0011] DeprecationWarning: crypto.Credentials is deprecated. Use tls.SecureContext instead.
app      | Memcache connected
app      | MongDB connected
app      | App listening on port 5000
app      | RabbitMQ connected

***********************************
* ELYSIAN START COMPLETE          *
***********************************

```

Handlers are registered according to the capability loaded from the configuration file from the /bin folder. Template defines where the schema template directory can be found and the allow determines who has access to specified capability.

```
{
	"configuration": [
		{
			"capability": "CreateProject",
			"template": "projects",
			"allow":["did:sov:*"]
		},
		{
			"capability": "CreateAgent",
			"template": "agents"
		},
		{
			"capability": "UpdateAgentStatus",
			"template": "agents"
		},
		{
			"capability": "SubmitClaim",
			"template": "claims"
		},
		{
			"capability": "EvaluateClaim",
			"template": "evaluations"
		},
		{
			"capability": "ListClaims",
			"template": "claims" 
		},
		{
			"capability": "ListAgents",
			"template": "agents" 
		}
	]
}
```

```
./stop.sh

***********************************
* ELYSIAN SHUTDOWN                *
***********************************

Stopping app   ... done
Stopping pol   ... done
Stopping mq    ... done
Stopping cache ... done
Stopping db    ... done
Going to remove app, cli, pol, mq, cache, db
Are you sure? [yN] y
Removing app   ... done
Removing cli   ... done
Removing pol   ... done
Removing mq    ... done
Removing cache ... done
Removing db    ... done

***********************************
* ELYSIAN SHUTDOWN COMPLETE       *
***********************************


```
## Securing Mongo DB:

```
docker exec -ti db /bin/bash
mongod
use admin
db.createUser({user: "<admin username>", pwd: "<admin password>", roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]})
use admin
db.auth("<admin username>", "<admin password>" )
mongo --port 27017 -u "<admin username>" -p "<admin password>" --authenticationDatabase "admin"
use elysian
db.createUser({user: "<username>", pwd: "<password>", roles: [{role: "readWrite", db: "elysian"}]})

```

API documents can be found at https://github.com/ixofoundation/mkdocs/blob/master/docs/api.md

## License

 - **MIT** : http://opensource.org/licenses/MIT

