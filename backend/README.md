
# activate venv
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# run igora protocol 
[IGORA protocol](https://github.com/scenaristeur/igora)  / [Igora Doc(https://scenaristeur.github.io/igora/)]
or other LLM configured in OAI_CONFIG_LIST (see autogen doc)

in igoraa run 

```
docker compose up
```


# test your installation with a simple_chat
```bash
python simple_chat.py
```
# run Equipe autobuild
- based on https://github.com/microsoft/autogen/blob/main/notebook/autobuild_basic.ipynb
```bash
python -m main.py
```


# autre projet nommé autobuild
qui n'a rien a voir https://phenix-online.org/documentation/reference/autobuild.html