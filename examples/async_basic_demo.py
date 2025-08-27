from fastapi import FastAPI
from litemon import configure_client, monitor
import asyncio

app = FastAPI()

# Configure LiteMon client
configure_client(server_url="http://127.0.0.1:8000", push_interval=2)

@monitor
async def greet_async():
    await asyncio.sleep(1)
    return "Hello! Welcome to the async server."

@monitor
async def bye_async():
    await asyncio.sleep(2)
    return "Goodbye! See you soon."

@app.get("/greet")
async def greet_route():
    return {"message": await greet_async()}

@app.get("/bye")
async def bye_route():
    return {"message": await bye_async()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "examples.async_basic_demo:app",
        host="127.0.0.1",
        port=5050,
        reload=True,
        log_level="debug"
    )