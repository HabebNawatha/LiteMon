# LiteMon 📊
A lightweight Python function monitoring client decorator & standalone metrics server.

# Overview 🚀
LiteMon is a zero‑config, lightweight monitoring tool that tracks your Python function calls, execution times, and performance metrics in real time.
It comes with a metrics server live dashboard where you can visualize and analyze metrics instantly.
## Features ✨

- 📈 Live Dashboard – view real-time metrics at /metrics
- ⚡ Lightweight – no heavy dependencies, minimal config
- 🧩 Zero Intrusion – just decorate your functions and monitor them
- 🧹 Reset Support — clear metrics instantly via /reset
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
1. Start the LiteMon server
```bash
litemon --port 8000
```
2. Use LiteMon in your App
```python
from flask import Flask
from litemon import configure_client, monitor

app = Flask(__name__)

# Configure LiteMon client to push metrics to the server
configure_client(server_url="http://127.0.0.1:8000", push_interval=2)

@monitor
def greet():
    return "Hello! Welcome to the server."

@monitor
def bye():
    return "Goodbye! See you soon."

@app.route('/greet', methods=['GET'])
def greet_route():
    return greet()

@app.route('/bye', methods=['GET'])
def bye_route():
    return bye()

if __name__ == '__main__':
    app.run(port=5050, debug=True)
```

3. Monitor Metrics
Fetch current metrics:
```bash
curl http://127.0.0.1:8000/metrics
```
* Your Flask app → http://127.0.0.1:5050
* LiteMon metrics dashboard → http://127.0.0.1:8000/metrics

4. Reset Metrics
Clear all collected metrics:
```bash
curl -X POST http://127.0.0.1:8000/reset
```
## Metrics Dashboard 📊
LiteMon’s metrics displays:
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
- ⚡ **Lightweight** – minimal dependencies.
- 🧩 **Easy to Use** – add a simple decorator and run the litemon server.
- 📊 **Live Metrics** – instantly see function calls and timings.
- 🔌 **Decoupled** — reuse the same server for multiple apps.
- 🛠 **Developer Friendly** – flexible, perfect for debugging and profiling.



## Contributing 🤝
We welcome contributions!
- Fork the repo
- Commit your changes
- Open a Pull Request 🎉



## Author ✍️
**Habeb Nawatha**  
🌐 [GitHub](https://github.com/HabebNawatha) • 💼 [LinkedIn](https://www.linkedin.com/in/habeb-nawatha/)