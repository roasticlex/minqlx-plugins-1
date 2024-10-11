import minqlx
import requests
import json

class bigbrother(minqlx.Plugin):
    def __init__(self):
        super().__init__()
        self.add_hook("chat", self.handle_chat, priority=minqlx.PRI_LOWEST)
    
    def handle_chat(self, player, msg, channel):
        self.lookup_chat(player, msg, channel)
        return minqlx.RET_STOP_EVENT
    
    @minqlx.thread
    def lookup_chat(self, player, msg, channel):
        api_url = 'https://api.api-ninjas.com/v1/profanityfilter?text={}'.format(msg)          
        response = requests.get(api_url, headers={'X-Api-Key': self.get_cvar("qlx_big_brother_api_key")})

        if response.status_code == requests.codes.ok:
            response = json.loads(response.text)             
            self.msg("{}: {}".format(player, response["censored"])) 
        else:
            if response.status_code == 400:
                self.msg("Please set qlx_big_brother_api_key in server.cfg from: https://api-ninjas.com/api/profanityfilter")
            self.msg("Error: {} {}".format(response.status_code, response.text))
