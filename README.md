# demo-orders-api

A small sample order service, used to demonstrate [Hatterdash](https://hatterdash.io). It has never been deployed and isn't meant to be.

Its pull requests are staged. They contain deliberate security flaws and vulnerable dependencies, so Hatterdash has something to find. Don't copy code from them.

## Run the tests

```bash
pip install -r requirements-dev.txt
python -m pytest --cov=.
```
