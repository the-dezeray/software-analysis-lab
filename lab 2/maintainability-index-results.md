# Maintainability Index Results

Command: `radon mi src/`

Note: No `src/` directory exists in this repo (source is in `app/`). `radon mi src/` returns empty. Below is the result for the actual source `app/` (`radon mi -s app/`).

## `radon mi app/`

```
app\cli.py - A
app\storage.py - A
app\tasks.py - A
app\__init__.py - A
```

## `radon mi -s app/` (with scores)

```
app\cli.py - A (71.45)
app\storage.py - A (83.65)
app\tasks.py - A (56.26)
app\__init__.py - A (100.00)
```

All files rank A (highly maintainable, MI 20-100 scale where higher is better).
