import minqlx

class mapvoterules(minqlx.Plugin):

    def __init__(self):
        self.set_cvar_once("qlx_allowSameMapVote", "0")

        self.add_hook("vote_called", self.handle_vote_called)
        self.add_hook("vote_ended", self.handle_vote_ended)
    
    def handle_vote_called(self, caller, vote, args):
        if not self.get_cvar("g_allowSpecVote", bool) and caller.team == "spectator":
            if caller.privileges == None:
                caller.tell("^1You are not allowed to call a vote as spectator.")
                return minqlx.RET_STOP_ALL
                        
        if not self.get_cvar("qlx_allowSameMapVote", bool):            
            if vote.lower() == "map" and args.lower() == self.get_cvar("mapname"):
                caller.tell("You can't callvote the same/current map!")
                return minqlx.RET_STOP_ALL
        
    def handle_vote_ended(self, votes, vote, args, passed):
        self.msg(votes)
        return minqlx.RET_STOP_ALL
