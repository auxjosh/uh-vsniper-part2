import aiohttp
import json
import os
import asyncio
from tls_client import Session
import re, requests
import time

token = ''
guid = '1277646616706285609' # guild id of the guild to put your sniped vanity in heh!!!!
password = 'joshyposhy@8787998'
'''
set the targets like this!!


targets = {
   
    '1276644710806716480': 'fymjosh'
    ^^^^^^^^^^^^^^^^^^^^^  ^^^^^^^^^^
    Guild id of target     their vanity
}
 DO THIS BELOW 
 vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
'''

targets = {
    '1277646616706285609': 'fymjosh',
}

def fetch_buildnum() -> int: 
        build_number = None
        try:
            asset_files = re.findall(r'<script\s+src="([^"]+\.js)"\s+defer>\s*</script>', requests.get("https://discord.com/login").text)
            for js_endpoint in asset_files:
                resp = requests.get(f"https://discord.com/{js_endpoint}")
                if "buildNumber" not in resp.text:
                    continue
                else:
                    build_number = resp.text.split('build_number:"')[1].split('"')[0]
                    break
            return build_number
        except:
            return None

class Onliner:
    def __init__(self, token: str) -> None:
        self.token = token
        self.s = None
        self.session_id = None
        self.uri = None
        self.tasks = []
        self.xtick = None
        self.session = Session(client_identifier='chrome_117', random_tls_extension_order=True)

    def _mfa(self, password, tim, cooks):
        url = "https://discord.com/api/v9/mfa/finish"
        headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': self.token,
        'content-type': 'application/json',
        'origin': 'https://discord.com',
        'priority': 'u=1, i',
        'referer': 'https://discord.com/channels/@me',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'x-debug-options': 'bugReporterEnabled',
        'x-discord-locale': 'en-US',
        'x-discord-timezone': 'America/New_York',
        'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyOC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTI4LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjMyODY5NywiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0=',
    }
        payload = {
            'ticket': tim,
            'mfa_type': 'password',
            'data': password,
        
        }
        try:
            response = self.session.post(url, json=payload, headers=headers, cookies=cooks)
            return response.json()['token'], response.cookies.get('__Secure-recent_mfa')
        except:
            return None

    async def change_vanitys(self, vanity_code, password):
        url = f"https://discord.com/api/v9/guilds/{guid}/vanity-url"
        headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': self.token,
        'content-type': 'application/json',
        'origin': 'https://discord.com',
        'priority': 'u=1, i',
        'referer': 'https://discord.com/channels/@me',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'x-debug-options': 'bugReporterEnabled',
        'x-discord-locale': 'en-US',
        'x-discord-timezone': 'America/New_York',
        'x-discord-mfa-authorization': self.xtick,
        'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyOC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTI4LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjMyODY5NywiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0=',
        }
    
    
        try:
            response = self.session.patch(url, json={'code': vanity_code}, headers=headers)
            if response.status_code == 200:
                print(f"Sniped Vanity {vanity_code}")
            elif 'mfa' in response.text:
                
                    ticket = response.json()['mfa']['ticket']
                    cookies2 = response.cookies
                    tick, x = self._mfa(password, ticket, cookies2)
                    self.xtick = tick
                    if not tick:
                        print("Failed to get MFA token")
                        return
                    cookiesx = {
                    '__Secure-recent_mfa': x,
                    '__dcfduid': cookies2.get('__dcfduid'),
                    '__sdcfduid': cookies2.get('__sdcfduid'),
                    '__cfruid': cookies2.get('__cfruid'),
                    '_cfuvid': cookies2.get('_cfuvid'),
                    }
                    headers['x-discord-mfa-authorization'] = self.xtick
                    resp = self.session.patch(url, json={'code': vanity_code}, headers=headers, cookies=cookiesx)
                    if resp.status_code == 200:
                        print(f"Sniped Vanity {vanity_code}")
        except:
            print(response.json())

    async def start(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.ws_connect("wss://gateway.discord.gg/?encoding=json&v=9") as ws:
                    await self.send_presence(ws)
                    self.tasks = [self._handle_events(ws)]
                    await asyncio.gather(*self.tasks)
        except Exception as e:
            print(f"Error starting connection: {e}")

    async def send_presence(self, ws):
        try:
            await ws.send_json({

            "op": 2,
            "d": {
                "token": self.token,
                "capabilities": 30717,
                "properties": {
                        "os": "Windows",
                        "browser": "Chrome",
                        "device": "Desktop",
                        "system_locale": "en-US",
                        "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
                        "browser_version": f"117.0.0.0",
                        "os_version": "10",
                        "referrer": "",
                        "referring_domain": "",
                        "referrer_current": "",
                        "referring_domain_current": "",
                        "release_channel": "stable",
                        "client_build_number": int(fetch_buildnum()),
                        "client_event_source": None
                },
                "presence": {
                    "afk": False,
                    "since": time.time(),
                    "activities": [{
                        "name": 'running sniper by fymjosh',
                        "type": 0,
                    }],
                    "status": "unknown"
                },
                "compress": False,
                "client_state": {
                    "guild_versions": {}
                }
            }
        })
        except Exception as e:
            print(f"Error sending initial presence: {e}")


    async def _handle_s(self, ws):
        while True:
            try:
                async for msg in ws:
                    event = json.loads(msg.data)
                
                    if "s" in event:
                        self.s = event["s"]
                    if "resume_gateway_url" in event:
                        self.session_id = event["d"]["session_id"]
                        self.uri = event["d"]["resume_gateway_url"] + '/?encoding=json&v=9'
                        print("online with -> " + self.session_id)

            except Exception as e:
                print(f"Error during event handling: {e}")

    async def _handle_events(self, ws):
        try:
            async for msg in ws:
                    event = json.loads(msg.data)
                    
                    if event["op"] == 10:
                        heartbeat_interval = int(event["d"]["heartbeat_interval"]) / 1000
                        asyncio.create_task(self.send_heartbeat(ws, heartbeat_interval))

                    if event['t'] == 'GUILD_UPDATE':
                        if event['d']['id'] in targets and targets[event['d']['id']] != event['d']['vanity_url_code']:
                            await self.change_vanitys(targets[event['d']['id']], password)

        except Exception as e:
            print(f"Error during event handling: {e}")

    async def send_heartbeat(self, ws, interval):
        try:
            while True:
                heartbeat_json = {"op": 1, "d": self.s}
                await ws.send_json(heartbeat_json)
                await asyncio.sleep(interval)
        except Exception as e:
            print(f"Error sending heartbeat: {e}")

async def main():
    os.system('cls' if os.name=='nt' else 'clear')
    try:
        
        onliner = Onliner(token)
        await onliner.start()


            
    except Exception as e:
        print(f"Oh no!!!!! an error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
