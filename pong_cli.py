import os
import sys
import json
import re
import time
import requests

def get_global_state():
    f = open('global_state.json')
    d = json.load(f)
    return d

def set_global_state(state):
    f = open('global_state.json')
    json_object = json.dumps(state, indent=4) 
    with open("global_state.json", "w") as outfile:
        outfile.write(json_object)

def send_first_request():
    requests.get("http://localhost:8001/ping")

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        print("Usage: ./pong_cli.py <command> <pong_time_ms>")
        exit()
        
    _, command, pong_time_ms = args
    print(f"{command} pong game with {int(pong_time_ms) / 1000} second(s) between pongs.")
    if command == "start":
        os.system("rm -f *log.txt && touch server1_log.txt server2_log.txt")
        os.system(f"python3 /mnt/c/Users/ashit/Desktop/Dataloop/pong_server.py {command} {pong_time_ms} 8001 8002 >>server1_log.txt 2>&1 &")
        os.system(f"python3 /mnt/c/Users/ashit/Desktop/Dataloop/pong_server.py {command} {pong_time_ms} 8002 8001  >>server2_log.txt 2>&1 &")
        time.sleep(2)
        f = open("server1_log.txt", "r")
        logs = f.read()
        pid_1 = re.findall(".*Started server process \[(\d+)\]", logs)[0]
        f = open("server2_log.txt", "r")
        logs = f.read()
        pid_2 = re.findall(".*Started server process \[(\d+)\]", logs)[0]
        set_global_state({"command": command, "pid_1": pid_1, "pid_2": pid_2})
        send_first_request()

    elif command == "stop":
        state = get_global_state()
        os.system(f"kill -9 {state['pid_1']} && kill -9 {state['pid_2']}")
        state.update({"command": command, "pid_1": 0, "pid_2": 0})
        set_global_state(state)
    
    else:
        state = get_global_state()
        state.update({"command": command})
        set_global_state(state)
        if command == "resume":
            send_first_request()
