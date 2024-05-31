from fastapi import FastAPI, Response, HTTPException
import sys
import uvicorn
import threading
import time
import requests
import json

app = FastAPI()

def get_global_state():
    f = open('global_state.json')
    d = json.load(f)
    return d


@app.get("/ping")
async def ping():
        state = get_global_state()
        if state['command'] in ['start', 'resume']:
            thread = threading.Thread(target=send_ping)
            thread.start()
            return Response(content="pong", media_type="text/html")
        return Response(content=f"Error: Game state is {state['command']}", media_type="text/html")

def send_ping():
    print("sending ping")
    time.sleep(int(pong_time_ms)/1000)
    resp = requests.get(f"http://0.0.0.0:{port2}/ping", timeout=10)
    print("ping sent", resp)


if __name__ == "__main__":
    args = sys.argv
    print(args)
    if len(args) != 5:
        print("Usage: ./pong_cli.py <command> <pong_time_ms>")
        exit()
    _, command, pong_time_ms, port1, port2 = args
    uvicorn.run(app, host="0.0.0.0", port=int(port1))