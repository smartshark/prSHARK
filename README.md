# prSHARK

Collect pull request information for smartSHARK.

Currently only Github is supported.

## Create venv and install dependencies
```bash
python -m venv .
source bin/activate
pip install -r requirements.txt
```

## Run tests
```bash
python -m unittest
```

## Execution for smartSHARK

prSHARK tries to link commits, so it would be best if the repository is already collected via vcsSHARK. Otherwise only the project has to exist.
```bash
python smartshark_plugin.py -U $DBUSER -P $DBPASS -p $DBPORT -DB $DBNAME -a $AUTHENTICATION_DB -pn $PROJECT_NAME -i $PULL_REQUEST_SYSTEM_URL -b $BACKEND -t $TOKEN
```

$BACKEND is currently only github, $TOKEN is also a github developer token that is needed for accessing the Github API.
The URL is in this form: https://api.github.com/repos/$OWNER/$PROJECT/pulls
