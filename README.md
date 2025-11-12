# Box-Mon
Monitor state of different downstream IP networks

## Setup

Install dependencies (works on Windows or Linux):

```bash
python install_dependencies.py
```

Then start the Flask dashboard:

```bash
python app.py
```

## Debugging / Test Run Helper

To generate a quick snapshot of the mock service checks without launching the UI, run:

```bash
python diagnostics.py
```

The script prints a readable summary for each configured node and dumps a JSON payload example so you can verify the mocked data end-to-end.
