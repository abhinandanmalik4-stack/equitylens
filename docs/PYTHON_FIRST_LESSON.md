# First lesson: understand the import error you saw

Start here if you know basic Python. Spend about 15 minutes on this lesson; learning the entire dashboard at once is not required. Code examples below refer to this checkout, and shorter teaching examples are labelled separately.

## One Python process uses one environment

Your browser reported `ModuleNotFoundError: No module named 'equitylens'` at an import in app.py. That means the Python process running the app could not locate our package. It does not, by itself, mean the package files were deleted.

On November 2, the checkout's own Python successfully imported `equitylens` from `src/equitylens`. A different launch environment was therefore a likely cause; the exact failed process was not inspected. Use [the VS Code tasks](VSCODE_SETUP.md) or the explicit `.venv` command to remove that ambiguity.

In the VS Code terminal, run:

```powershell
cd E:\gpt\equitylens
.\.venv\Scripts\python.exe -c "import sys, equitylens; print(sys.executable); print(equitylens.__file__)"
```

Read the two paths. The first should point to this checkout's `.venv` Python. The second should point to this checkout's `src/equitylens/__init__.py`. These tell you which interpreter and package copy are actually in use.

## Importing and calling are different

Actual import from app.py:

```python
from equitylens.catalog import search_instruments
```

- `equitylens` is our package under `src/`.
- `catalog` identifies `catalog.py` inside it.
- `search_instruments` is a function defined there.
- The import makes that function available by name. It does not yet search for your typed company name.

Actual call from app.py:

```python
matches = search_instruments(query)
```

`query` is the input passed into the function. The returned matching instruments are assigned to `matches`. In basic Python terms, it is input -> function -> return value.

Try a call without opening the webpage:

```powershell
.\.venv\Scripts\python.exe -c "from equitylens.catalog import search_instruments; print([item.name for item in search_instruments('banking')])"
```

Expected catalogue matches: `HDFC Bank` and `ICICI Bank`. These are names in our demo catalogue, not fetched market data or a current listing verification.

## Why the code is inside src

The package files live in `src/equitylens`, while `app.py` lives at the project root. During setup, `python -m pip install -e .` registers the project with that particular Python environment. The dot means the current project; editable mode lets source edits be used without reinstalling after every code change.

Installing it into one Python environment does not install it into every Python on the computer. Installing a similarly named package from the internet is not the solution to finding our local project.

The new `run_equitylens.py` launcher finds this checkout's `.venv`, checks imports, then starts Streamlit with that interpreter and the correct working directory. `--check` checks imports only. It does not install packages or start a server.

## A tiny practice example

This is a separate teaching example, not a replacement for project code:

```python
def find_names(query):
    names = ['HDFC Bank', 'ICICI Bank', 'Infosys']
    result = []
    for name in names:
        if query.lower() in name.lower():
            result.append(name)
    return result

matches = find_names('bank')
print(matches)
```

Predict the result, run it in a separate scratch file if desired, then explain the loop, condition and return. Both bank names should be returned. Our real search additionally checks symbols and sectors, and uses Instrument objects rather than plain strings. That is the next concept to learn; do not try to memorise it before this example makes sense.

## Interview checkpoint

Explain these without reading a script:

1. How is importing a function different from calling it?
2. What are an input argument and a return value in the search example?
3. Why can the same source work with one Python but fail with another?
4. Why do we check the interpreter and package paths before reinstalling anything?

An accurate project explanation is: "EquityLens uses a local Python package for its search and data logic. Streamlit's app.py imports those functions. The environment must have that package installed, so we launch through the project's own Python."

Say which parts you have personally read, modified and tested, and acknowledge AI assistance when discussing implementation. This worksheet is preparation, not a claim that you have completed the lesson or mastered the project.
