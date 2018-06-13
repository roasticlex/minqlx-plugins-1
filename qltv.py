import minqlx

PLAYER_KEY = "minqlx:players:{}"

class qltv(minqlx.Plugin):

    def __init__(self):
        self.spec_index = 0
        self.last_spec_steam_id = 0
        self.spec_timer()

        self.add_command("qltv", self.cmd_qltv)

    @minqlx.delay(45)
    def spec_timer(self):
        if self.game.state == "in_progress":
            sorted_players = sorted(self.players(), key = lambda p: p.stats.score, reverse=True)
            sorted_player_count = len(sorted_players)

            if self.spec_index + 1 > sorted_player_count or self.spec_index == 5:
                self.spec_index = 0
            elif self.last_spec_steam_id == sorted_players[self.spec_index].steam_id:
                self.spec_index += 1

            for p in self.teams()['spectator']:
                if int(self.db.get(PLAYER_KEY.format(p.steam_id) + ":qltv")) == 1:
                    minqlx.client_command(p.id, 'follow ' + str(sorted_players[self.spec_index].id))

            self.last_spec_steam_id = sorted_players[self.spec_index].steam_id
            self.spec_index += 1
            self.spec_timer()

    def cmd_qltv(self, player, msg, channel):
        current_qltv_setting = int(self.db.get(PLAYER_KEY.format(player.steam_id) + ":qltv"))

        if not current_qltv_setting or current_qltv_setting == 0:
            current_qltv_setting = 0
            player.tell('^5***QTLV HAS BEEN ENABLED***')

        if current_qltv_setting == 1:
            new_qltv_setting = 0
            player.tell('^5***QTLV HAS BEEN DISABLED***')
        else:
            new_qltv_setting = 1

        self.db.set(PLAYER_KEY.format(player.steam_id) + ":qltv", new_qltv_setting)
