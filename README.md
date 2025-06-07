# Matplotlib Graph Render API

This is a minimal Flask API to execute Python code with matplotlib and numpy and return a generated graph as a PNG image.

## Usage

- POST to `/render-matplotlib` with JSON body:
  `{ "code": "YOUR PYTHON CODE HERE" }`

- Returns: PNG image (mimetype `image/png`)

## Example Python code to send

```
import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(0, 10, 1000)
y = np.sin(x)
plt.plot(x, y)
plt.title('Sine Wave')
```

## Deploy on Render

1. Upload these files to GitHub
2. Connect GitHub repo to Render.com, create a new Web Service
3. Use `pip install -r requirements.txt` as the build command
4. Use `python app.py` as the start command
5. Set PORT environment variable to `$PORT` if required by Render

---
**Security Note:** This runs arbitrary code, so use with care.
