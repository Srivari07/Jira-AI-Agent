# VS Code Debugging Guide for process_query

## Quick Start - 3 Methods to Debug

### Method 1: Debug Flask Backend (Recommended for API Testing)

1. **Set Breakpoints** in `src/backend/api.py`:

   - Click on line number 54 (the `process_query` function line)
   - Click left of line numbers to add red dot breakpoints
   - Add breakpoints at key locations:
     - Line ~95: After query analysis
     - Line ~102: After fetching tickets
     - Line ~110: After matching tickets
     - Line ~118: After generating resolution

2. **Start Debugging**:

   - Press `F5` or click "Run → Start Debugging"
   - Select: **"Debug Flask Backend (api.py)"**
   - Backend will start with debugger attached

3. **Make API Request**:

   - In another terminal: `.venv\Scripts\python.exe test_api_query.py`
   - Or use curl/Postman to send POST to `http://localhost:5000/api/query`

4. **When Breakpoint Hits**:
   - Execution pauses at your breakpoint
   - Inspect variables in "Variables" panel (left side)
   - Use Debug Console (bottom) to evaluate expressions
   - Step through code with:
     - `F10` - Step Over (next line)
     - `F11` - Step Into (enter function)
     - `Shift+F11` - Step Out (exit function)
     - `F5` - Continue

---

### Method 2: Debug Standalone Script (Easier, No Flask)

1. **Set Breakpoints** in `debug_process_query.py`:

   - Line 53: After analyzing query
   - Line 67: After fetching tickets
   - Line 82: After matching tickets
   - Line 95: After generating resolution

2. **Start Debugging**:

   - Press `F5`
   - Select: **"Debug Standalone process_query"**
   - Script runs directly without Flask

3. **Choose Test Case**:

   - Select from menu when prompted
   - Or enter custom query

4. **Step Through**:
   - Use F10/F11 to step through each line
   - Inspect all variables in real-time

---

### Method 3: Quick Inline Debugging

**Add this line anywhere in `process_query` function:**

```python
# In api.py, inside process_query()
breakpoint()  # Python 3.7+ built-in debugger
```

**Or for VS Code specific:**

```python
import debugpy
debugpy.breakpoint()
```

Then run normally - execution will pause at that line.

---

## VS Code Debugging Features

### Debug Console (Bottom Panel)

Type Python expressions while paused:

```python
# Check variable values
query
projects
len(historical_tickets)
matched_tickets[0] if matched_tickets else None

# Call functions
llm_agent.analyze_query("test")
type(jira_client)
```

### Watch Expressions (Left Panel)

Add expressions to monitor continuously:

- `len(historical_tickets)`
- `len(matched_tickets)`
- `query`
- `resolution[:100]`

### Call Stack (Left Panel)

Shows function call hierarchy - click to jump to any level

### Variables Panel (Left Panel)

Browse all variables in current scope:

- `data` - request data
- `query` - user query
- `historical_tickets` - list of tickets
- `matched_tickets` - filtered results

---

## Common Breakpoint Locations

In `src/backend/api.py` - `process_query()` function:

| Line | Location                   | Purpose                |
| ---- | -------------------------- | ---------------------- |
| ~54  | Function start             | Check request data     |
| ~75  | Before query validation    | Inspect incoming query |
| ~81  | Before analyze_query       | Before LLM call        |
| ~83  | After analyze_query        | See analysis result    |
| ~87  | Before search_tickets      | Before JIRA call       |
| ~93  | After search_tickets       | Check fetched tickets  |
| ~97  | Before match_tickets       | Before matching        |
| ~103 | After match_tickets        | See matched results    |
| ~108 | Before generate_resolution | Before final LLM call  |
| ~111 | After generate_resolution  | See final resolution   |
| ~122 | Before return              | Check final response   |

---

## Debugging Workflow

1. **Set breakpoint** at start of `process_query` (line ~54)
2. **Press F5** → Select "Debug Flask Backend"
3. **Wait** for "Running on http://0.0.0.0:5000" message
4. **In another terminal**: Run test script or curl
5. **Breakpoint hits** → Inspect variables
6. **Press F10** to step through line by line
7. **Check Variables panel** for all data
8. **Use Debug Console** to test expressions
9. **Press F5** to continue to next breakpoint

---

## Tips & Tricks

### Conditional Breakpoints

Right-click on breakpoint → "Edit Breakpoint" → Add condition:

```python
query == "specific text"
len(matched_tickets) == 0
```

### Logpoints (Print without stopping)

Right-click line number → "Add Logpoint":

```python
Query: {query}, Matched: {len(matched_tickets)}
```

### Quick Variable Inspection

Hover mouse over any variable to see its value

### Debug Console Tips

```python
# Pretty print
import json
print(json.dumps(matched_tickets, indent=2))

# Quick type check
type(llm_agent)

# Test function
llm_agent.analyze_query("test query")
```

---

## Troubleshooting

**Breakpoint not hitting?**

- Check you selected correct debug config
- Verify file is saved (Ctrl+S)
- Make sure request actually reaches endpoint

**Variables not showing?**

- Check "justMyCode": false in launch.json (already set)
- Make sure you're paused at breakpoint

**Can't connect to backend?**

- Check .env file has valid credentials
- Verify virtual environment is activated
- Check no other process on port 5000

---

## Keyboard Shortcuts

| Key             | Action                     |
| --------------- | -------------------------- |
| `F5`            | Start Debugging / Continue |
| `F9`            | Toggle Breakpoint          |
| `F10`           | Step Over (next line)      |
| `F11`           | Step Into (enter function) |
| `Shift+F11`     | Step Out (exit function)   |
| `Ctrl+Shift+F5` | Restart Debugging          |
| `Shift+F5`      | Stop Debugging             |

---

## Example Debug Session

1. Open `src/backend/api.py`
2. Click left of line 54 to add breakpoint (red dot appears)
3. Press `F5` → Select "Debug Flask Backend (api.py)"
4. Open new terminal → Run: `.venv\Scripts\python.exe test_api_query.py`
5. When breakpoint hits:
   - Look at Variables panel → See `request` object
   - Press `F10` → Step to line 75
   - Press `F10` → Step to line 79 (data extracted)
   - In Debug Console type: `data` → See the request payload
   - Press `F10` multiple times → Watch each step execute
   - Hover over `query_analysis` → See LLM result
   - Continue until you find the issue!

---

## Ready to Debug!

Press **F5** now and select a debug configuration to start!
