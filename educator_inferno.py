# educator_inferno.py

import minqlx

class educator_inferno(minqlx.Plugin):
    def __init__(self):
        super().__init__()
        self.add_command("educator_inferno", self.cmd_educator_inferno, 5)
        self.add_command("educator_extinguish", self.cmd_educator_extinguish, 5)

    def unload(self):
        minqlx.console_print("EducatOR inferno plugin unloaded")
  
    def cmd_educator_inferno(self, player, msg, channel):
        if player.steam_id == "76561197960782507":
            # Send a command to the client to set EduCatOR's model on fire
            player.send_client_command("r_flash 1 100 255 0 0")
            channel.reply("EduCatOR is now engulfed in flames!")

    def cmd_educator_extinguish(self, player, msg, channel):
        if player.steam_id == "76561197960782507":
            # Send a command to the client to remove the fire effect
            player.send_client_command("r_flash 0")
            channel.reply("The flames have been extinguished!")
