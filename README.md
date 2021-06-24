### One Time Setup

```
python3 -m venv env
```

To activate the env:

```
#fish
. env/bin/activate.fish
#bash
source env/bin/activate
```

Save and commit dependencies

```
pip freeze > requirements.txt
git add requirements.txt
git commit -m 'update dependencies'
```

### Environment Setup

Install [direnv](https://direnv.net/)

```
echo 'export BOT_TOKEN=xyz-your-token-xyz' >> .envrc
echo 'export WAIT_DIR=/some/directory' >> .envrc
```


### Telegram

Requires a bot token created via @BotFather.
