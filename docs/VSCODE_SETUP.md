# Open and run EquityLens in VS Code

Open **File -> Open Folder** and select `E:\gpt\equitylens`. Open the entire checkout so VS Code can find `.vscode/tasks.json` and the local environment. Press Ctrl+P, type `app.py`, then Enter to read the interface code.

## Run without choosing the wrong interpreter

1. Save your edits with Ctrl+S.
2. Select **Terminal -> Run Task**.
3. Choose **EquityLens: check environment** first. It must report that the environment check passed; it starts no web server.
4. Run **EquityLens: run dashboard**.
5. Open the Local URL printed in the task terminal. The launcher uses `127.0.0.1` and port 8501 by default.
6. Stop the server with Ctrl+C in that terminal. Stop an old server before starting a replacement on the same port.

These tasks call the checkout's `.venv` Python directly and set the project folder as the working directory. They need an already prepared environment; they do not download packages, install extensions, change PowerShell policy or deploy the app. The ordinary **Run Python File** triangle is not the Streamlit run task.

## If VS Code has already selected a different Python

The workspace default points to `.venv`, but an earlier selection may remain. Use Ctrl+Shift+P -> **Python: Select Interpreter** and select the Python inside this checkout's `.venv`. On Windows its path is `E:\gpt\equitylens\.venv\Scripts\python.exe`.

Selecting the interpreter helps editor support and ordinary Python commands; the named tasks still explicitly use the project environment. No global Python setting is changed by this configuration.

## Terminal alternative

```powershell
cd E:\gpt\equitylens
.\.venv\Scripts\python.exe run_equitylens.py --check
.\.venv\Scripts\python.exe run_equitylens.py
```

If port 8501 is occupied and you want a second instance, use `run_equitylens.py --port 8502` and open the URL it prints. Otherwise stop the existing instance first. The launcher does not terminate other programs.

For first-time installation and import errors, see [Run and learn](RUN_AND_LEARN.md). The task configuration uses the official [VS Code task format](https://code.visualstudio.com/docs/debugtest/tasks), [workspace variables](https://code.visualstudio.com/docs/reference/variables-reference) and [Python interpreter settings](https://code.visualstudio.com/docs/python/settings-reference). JSON/path checks were performed locally; clicking these new tasks in a live VS Code window remains a manual check.
