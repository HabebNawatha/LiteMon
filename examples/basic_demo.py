import time
from litemon import monitor, start_dashboard
import litemon

# Start the dashboard in the background
start_dashboard(port=8000)

@monitor
def greet(name: str):
    """Simulate greeting with a small delay"""
    time.sleep(0.1)
    return f"Hello, {name}"

@monitor
def risky_div(a: int, b:int):
    """Simulate a division function with occasionl errors"""
    return a / b

if __name__ == "__main__":
    print(litemon.__file__)
    for i in range(0,5):
        greet("litemon")
        try:
            risky_div(10, i % 3)
        except ZeroDivisionError:
            pass
    print("📊 Visit http://127.0.0.1:8000/metrics to see live LiteMon stats")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 LiteMon dashboard stopped")
