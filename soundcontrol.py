import minqlx
import re
import datetime
import fileinput

LENGTH_REGEX = re.compile(r"(?P<number>[0-9]+) (?P<scale>seconds?|minutes?|hours?|days?|weeks?|months?|years?)")
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

class soundcontrol(minqlx.Plugin):

    def __init__(self):
        super().__init__()
        self.add_command("soundban", self.cmd_soundban, usage="<id> <length> seconds|minutes|hours|days|... [reason]")

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
        #if self.db.has_permission(ident, 5):
        #    channel.reply("^6{}^7 has permission level 5 and cannot be banned.".format(name))
        #    return
        

        if len(msg) > 4:
            reason = " ".join(msg[4:])
        else:
            reason = ""
        
        r = LENGTH_REGEX.match(" ".join(msg[2:4]).lower())
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

            with open("soundbans.txt", 'r') as file:
                content = file.read()
                if str(target_player.steam_id) in content:
                    ban_exists = True
                else:
                    ban_exists = False

            if ban_exists:
                with fileinput.input("soundbans.txt", inplace=True) as file:
                    for line in file:
                        if str(player.steam_id) in line:
                            #overwrite current ban line with new ban
                            print("{},{},{},{}\n".format(str(target_player.steam_id), expires, reason, now), end='')
                        else:
                            print(line, end='')
            else:
                f = open("soundbans.txt", "a")
                #add new ban line to end of file
                f.write("{},{},{},{}\n".format(str(target_player.steam_id), expires, reason, now))
                f.close()
                channel.reply("^6{} ^7has been banned from sounds. Ban expires on ^6{}^7.".format(name, expires))

    def check_if_banned(self, player):
        with open("soundbans.txt", 'r') as file:
            for num, line in enumerate(file, 1):
                if str(player.steam_id) in line:
                    #check if ban is expired by reading expiry date from file line
                    if line.split(",")[1] > (datetime.datetime.now()).strftime(TIME_FORMAT):
                        return True
                else:
                    return False
