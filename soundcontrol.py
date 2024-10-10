import minqlx
import re
import datetime
import fileinput
import os

LENGTH_REGEX = re.compile(r"(?P<number>[0-9]+) (?P<scale>seconds?|minutes?|hours?|days?|weeks?|months?|years?)")
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

class soundcontrol(minqlx.Plugin):

    def __init__(self):
        super().__init__()
        self.add_command("soundban", self.cmd_soundban, 2, usage="<id> <length> seconds|minutes|hours|days|...")
        self.add_command("soundunban", self.cmd_soundunban, 2, usage="<id>")
        self.add_command("checksoundbans", self.cmd_checksoundbans, 2)
        self.add_command("adjustsounddelay", self.cmd_adjustsounddelay, 5, usage="<short/medium/long> <value>")
        self.add_command("addsound", self.cmd_addsound, 5, usage="<short/medium/long> <sound name>")
        self.add_command("customsounddelay", self.cmd_customsounddelay, 5, usage="<value> <sound name>")
        self.add_command("removesounddelay", self.cmd_removesounddelay, 5, usage="<sound name>")
        self.add_command("soundautobanthreshold", self.cmd_soundautobanthreshold, 5, usage="<value>")
        self.add_command("soundautobanduration", self.cmd_soundautobanduration, 5, usage="<length> seconds|minutes|hours|days|...")
        self.add_command("soundcontrolconfig", self.cmd_soundcontrolconfig, 5)

        self.sounds_per_minute = {}        

    def cmd_soundban(self, player, msg, channel):
        if len(msg) < 4:
            return minqlx.RET_USAGE

        try:
            ident = int(msg[1])
            target_player = None
            if 0 <= ident < 64:
                target_player = self.player(ident)
                ident = target_player.steam_id
        except ValueError:
            channel.reply("Invalid ID. Use either a client ID or a SteamID64.")
            return
        except minqlx.NonexistentPlayerError:
            channel.reply("Invalid client ID. Use either a client ID or a SteamID64.")
            return
        
        if target_player:
            name = target_player.name
        else:
            name = ident

        # Permission level 5 players not bannable.
        if self.db.has_permission(ident, 5):
            channel.reply("^6{}^7 has permission level 5 and cannot be banned.".format(name))
            return
        
        r = LENGTH_REGEX.match(" ".join(msg[2:4]).lower())
        if not r:
            r = LENGTH_REGEX.match(msg.lower())
        if r:            
            number = float(r.group("number"))
            if number <= 0: return
            scale = r.group("scale").rstrip("s")
            td = None
            
            if scale == "second":
                td = datetime.timedelta(seconds=number)
            elif scale == "minute":
                td = datetime.timedelta(minutes=number)
            elif scale == "hour":
                td = datetime.timedelta(hours=number)
            elif scale == "day":
                td = datetime.timedelta(days=number)
            elif scale == "week":
                td = datetime.timedelta(weeks=number)
            elif scale == "month":
                td = datetime.timedelta(days=number * 30)
            elif scale == "year":
                td = datetime.timedelta(weeks=number * 52)
            
            now = datetime.datetime.now().strftime(TIME_FORMAT)
            expires = (datetime.datetime.now() + td).strftime(TIME_FORMAT)

            with open("minqlx-plugins/soundcontrol/soundbans.txt", 'r') as file:
                content = file.read()
                if str(ident) in content:
                    ban_exists = True
                else:
                    ban_exists = False

            if ban_exists:
                with fileinput.input("minqlx-plugins/soundcontrol/soundbans.txt", inplace=True) as file:
                    for line in file:
                        if str(ident) in line:
                            #overwrite current ban line with new ban
                            print("{},{},{}\n".format(str(ident), expires, now), end='')
                        else:
                            print(line, end='')
                    if channel:
                        channel.reply("^6{} ^7 ban updated. Ban expires on ^6{}^7.".format(name, expires))
            else:
                self.msg("")
                f = open("minqlx-plugins/soundcontrol/soundbans.txt", "a")
                #add new ban line to end of file
                f.write("{},{},{}\n".format(str(ident), expires, now))
                f.close()
                if channel:
                    channel.reply("^6{} ^7has been banned from sounds. Ban expires on ^6{}^7.".format(name, expires))

    def cmd_soundunban(self, player, msg, channel):        
        """Unbans a player if soundbanned."""
        if len(msg) < 2:
            return minqlx.RET_USAGE

        try:
            ident = int(msg[1])
            target_player = None
            if 0 <= ident < 64:
                target_player = self.player(ident)
                ident = target_player.steam_id
        except ValueError:
            channel.reply("Invalid ID. Use either a client ID or a SteamID64.")
            return
        except minqlx.NonexistentPlayerError:
            channel.reply("Invalid client ID. Use either a client ID or a SteamID64.")
            return
        
        if target_player:
            name = target_player.name
        else:
            name = ident

        with fileinput.input("minqlx-plugins/soundcontrol/soundbans.txt", inplace=True) as file:
            for line in file:
                if str(ident) in line:
                    #remove ban line if steam id found
                    print("", end='')
                else:
                    print(line, end='')

        channel.reply("{} unbanned.".format(ident))

    def check_if_banned(self, player):
        with fileinput.input("minqlx-plugins/soundcontrol/soundbans.txt") as file:
            for line in file:
                if str(player.steam_id) in line:
                    #check if ban is expired by reading expiry date from file line
                    if line.split(",")[1] > (datetime.datetime.now()).strftime(TIME_FORMAT):
                        return True
                else:
                    return False

    def cmd_adjustsounddelay(self, player, msg, channel):
        if len(msg) < 3:
            return minqlx.RET_USAGE
        
        if msg[1] not in ["short", "medium", "long"]:
            channel.reply("Category must be short, medium or long.")
            return    
        
        try:
            int(msg[2])            
        except ValueError: 
            channel.reply("Value must be integer(number).")
            return  

        with fileinput.input("minqlx-plugins/soundcontrol/config.txt", inplace=True) as file:
            for line in file:
                if msg[1] in line:
                    #write category and duration at appropriate line
                    print("{},{}\n".format(msg[1], msg[2]), end='')
                else:
                    print(line, end='')

        channel.reply("Delay updated.")

    def cmd_addsound(self, player, msg, channel):
        if len(msg) < 3:
            return minqlx.RET_USAGE
        
        if msg[1] not in ["short", "medium", "long"]:
            channel.reply("Category must be short, medium or long.")
            return 
        
        with fileinput.input("minqlx-plugins/soundcontrol/custom_sound_delays.txt", inplace=True) as file:
            for line in file:
                if msg[2] in line:
                    #remove sound line if it exists
                    print("", end='')
                else:
                    print(line, end='')
                
        f = open("minqlx-plugins/soundcontrol/category_sound_delays.txt", "a")
        f.write("{},{}\n".format(msg[1], " ".join(msg[2:])))
        f.close()

        channel.reply("Sound delay added.")

    def cmd_customsounddelay(self, player, msg, channel):
        if len(msg) < 3:
            return minqlx.RET_USAGE
        
        try:
            int(msg[1])            
        except ValueError: 
            channel.reply("Value must be integer(number).")
            return 
        
        with fileinput.input("minqlx-plugins/soundcontrol/category_sound_delays.txt", inplace=True) as file:
            for line in file:
                if msg[2] in line:
                    #remove sound line if it exists
                    print("", end='')
                else:
                    print(line, end='')

        f = open("minqlx-plugins/soundcontrol/custom_sound_delays.txt", "a")
        f.write("{},{}\n".format(msg[1], " ".join(msg[2:])))
        f.close()

        channel.reply("Custom sound delay added.")
        
    def cmd_removesounddelay(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE
        
        with fileinput.input("minqlx-plugins/soundcontrol/category_sound_delays.txt", inplace=True) as file:
            for line in file:
                if " ".join(msg[1:]) in line:
                    #remove sound line if it exists
                    print("", end='')
                else:
                    print(line, end='')
    
        with fileinput.input("minqlx-plugins/soundcontrol/custom_sound_delays.txt", inplace=True) as file:
            for line in file:
                if  " ".join(msg[1:]) in line:
                    #remove sound line if it exists
                    print("", end='')
                else:
                    print(line, end='')
        
        channel.reply("Sound delay removed.")
    
    def cmd_soundautobanthreshold(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE
        
        try:
            int(msg[1])            
        except ValueError: 
            channel.reply("Value must be integer(number).")
            return 

        with fileinput.input("minqlx-plugins/soundcontrol/config.txt", inplace=True) as file:
            for line in file:
                if "soundautobanthreshold" in line:
                    print("soundautobanthreshold,{}\n".format(msg[1]), end='')
                else:
                    print(line, end='')
            
            channel.reply("soundautobanthreshold set.")

    def cmd_soundautobanduration(self, player, msg, channel):
        if len(msg) < 3:
            return minqlx.RET_USAGE        

        with fileinput.input("minqlx-plugins/soundcontrol/config.txt", inplace=True) as file:
            for line in file:
                if "soundautobanduration" in line:
                    self.msg("found soundbanautoduration")
                    print("soundautobanduration,{} {}\n".format(msg[1], msg[2]), end='')
                else:
                    print(line, end='')
                
            channel.reply("soundautobanduration set.")
    
    @minqlx.delay(60) 
    def handle_sound(self, player):
        soundautobanthreshold = 0
        soundautobanduration = 0

        with fileinput.input("minqlx-plugins/soundcontrol/config.txt") as file:
            for line in file:                
                if "soundautobanthreshold" in line:
                    if not line.split(",")[1].strip() == "none":
                        soundautobanthreshold = int(line.split(",")[1])
                if "soundautobanduration" in line:
                    if not line.split(",")[1].strip() == "none":
                        soundautobanduration = line.split(",")[1:2][0]

        if soundautobanthreshold and soundautobanduration:
            if self.sounds_per_minute[player.steam_id] > soundautobanthreshold:
                self.cmd_soundban(player.steam_id, soundautobanduration, "")

        self.sounds_per_minute[player.steam_id] = 0

    def cmd_checksoundbans(self, player, msg, channel):
        if os.stat("minqlx-plugins/soundcontrol/soundbans.txt").st_size != 0:
            with fileinput.input("minqlx-plugins/soundcontrol/soundbans.txt") as file:
                for line in file:
                    channel.reply(line)
        else:
            channel.reply("No sound bans are set.")

    def cmd_soundcontrolconfig(self, player, msg, channel):
        with fileinput.input("minqlx-plugins/soundcontrol/config.txt") as file:
            for line in file:
                channel.reply(line)
