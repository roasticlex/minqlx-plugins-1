import minqlx

class timescalevote(minqlx.Plugin):

    def __init__(self):

        self.add_command("timescalevote", self.cmd_timescalevote, usage="<value>")
        self.add_command("settimescale", self.cmd_settimescale, 5)

    def cmd_timescalevote(self, caller, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE

        try:
            msg_as_float = float(msg[1])
        except:
            channel.reply("timescale must be a number in the range of 0.1 to 5")
            return
        
        if msg_as_float < 0.1 or msg_as_float > 5:
            channel.reply("timescale must be a number in the range of 0.1 to 5")
            return
        
        self.callvote("qlx !settimescale {}".format(msg[1]), "Change timescale to: {}?".format(msg_as_float))
        self.msg("{}^7 called a vote.".format(caller.name))

    def cmd_settimescale(self, caller, msg, channel):        
        minqlx.set_cvar("timescale", msg[1], -1)
        
        
