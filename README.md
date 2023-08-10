This is a testing version, 

to run

```
uvicorn wsgi:app --reload
```

from the top level folder. 

This version attempts to use a system wide file based lock which is probably simpler and safer?!!!! that asyncio for a start! 

# sigraDB
A new lightweight Ontological Semantic Graph Data Base  

It is based on simple ttl files, and a simple folder data structure and meant to be both simple and lightweight. 


To install locally in development (edit mode) use (in teh folder where the setupfile is): 
```
pip install -e .
```


# todo: 

- use environment variables

```
import os

universe_root_path = os.getenv('UNIVERSE_ROOT_PATH', 'default/path/to/universe')
data_universe_instance = data_universe(universe_root_path)
```
