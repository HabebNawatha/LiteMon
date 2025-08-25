# LiteMon 📊
A lightweight Python function monitoring tool with a live metrics dashboard.

## Overview 🚀
LiteMon is a zero‑config, lightweight monitoring tool that tracks your Python function calls, execution times, and performance metrics in real time.
It comes with a built-in live dashboard where you can visualize and analyze metrics instantly.
## Features ✨

- 📈 Live Dashboard – view real-time metrics at /metrics

- ⚡ Lightweight – no heavy dependencies or config required

- 🧩 Zero Intrusion – just decorate your functions and monitor them

- 🛠 Built-in HTTP Server – launches automatically, no setup needed

- 🧑‍💻 Developer Friendly – perfect for debugging, profiling, and demos


## Installation 🔧

Install LiteMon directly from GitHub:

```bash
pip install git+https://github.com/HabebNawatha/LiteMon.git
```

Or, if you’re contributing locally:

```bash
git clone https://github.com/HabebNawatha/LiteMon.git
cd LiteMon
make install
```
## Quick Start 🏁
1. Basic Example
```python
from flask import Flask
from litemon import start_dashboard, monitor

app = Flask(__name__)

@monitor
def greet():
    print("Hello! Welcome to the server.")
    return "Hello! Welcome to the server."

@monitor
def bye():
    print("Goodbye! See you soon.")
    return "Goodbye! See you soon."

@app.route('/greet', methods=['GET'])
def greet_route():
    return greet()

@app.route('/bye', methods=['GET'])
def bye_route():
    return bye()

if __name__ == '__main__':
    start_dashboard(port=8000)  # Launches LiteMon dashboard
    app.run(port=5050, debug=True)
```

2. Run the app
```bash
python server.py
```
* Your Flask app → http://127.0.0.1:5050
* LiteMon metrics dashboard → http://127.0.0.1:8000/metrics




## Metrics Dashboard 📊
LiteMon’s dashboard displays:
- Function call counts
- Average execution times
- Error counts
- Real-time performance tracking
Example output:

```json
{
    "greet": {
        "calls": 12,
        "success":12,
        "failures":0,
        "avg_time": 3.21
    },
    "bye": {
        "calls": 12,
        "success":12,
        "failures":0,
        "avg_time": 1.84
    }
}
```
## Why LiteMon? 🤔
- ⚡ **Lightweight** – no heavy dependencies or setup.
- 🧩 **Easy to Use** – add a simple decorator, and you’re done.
- 📊 **Live Metrics** – instantly see function calls and timings.
- 🛠 **Developer Friendly** – perfect for debugging and profiling.



## Contributing 🤝
We welcome contributions!
- Fork the repo
- Create a new branch
- Commit your changes
- Submit a pull request 🎉



## Author ✍️
**Habeb Nawatha**  
🌐 [GitHub](https://github.com/HabebNawatha) • 💼 [LinkedIn](https://www.linkedin.com/in/habeb-nawatha/)