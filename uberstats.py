import minqlx
import time

class uberstats(minqlx.Plugin):

    def __init__(self):
        self.add_hook("stats", self.handle_stats)
        self.add_hook("game_start", self.handle_game_start)
        self.add_hook("game_end", self.handle_game_end)

        self.weapon_accuracies = ["PLASMA", "ROCKET", "PROXMINE", "RAILGUN", "CHAINGUN", "NAILGUN", "GRENADE", "LIGHTNING", "SHOTGUN", "MACHINEGUN", "HMG", "BFG"]
        self.outputted_accuracy_players = []
        self.kamikaze_stats = {}
        self.plasma_stats = {}

        self.best_kpm_names = []
        self.best_kpm = 0

        self.best_kd_names = []
        self.best_kd = 0

        self.most_damage_names = []
        self.most_damage = 0

        self.longest_spree_names = []
        self.longest_spree = 0

        self.best_rail_accuracy_names = []
        self.best_rail_accuracy = 0
        self.best_rail_hits = 0
        self.best_rail_shots = 0

        self.most_nade_kills_names = []
        self.most_nade_kills = 0

        self.most_pummels_names = []
        self.most_pummels = 0

        self.most_dmg_taken_names = []
        self.most_dmg_taken = 0

        self.world_death_types = ["UNKNOWN", "WATER", "SLIME", "LAVA", "CRUSH", "FALLING", "TRIGGER_HURT", "HURT"]
        self.world_death_stats = {}
        self.most_world_deaths_names = []
        self.most_world_deaths = 0

    def handle_stats(self, stats):
        if self.game.state == "in_progress":
            if stats['TYPE'] == "PLAYER_DEATH":
                if int(stats['DATA']['STEAM_ID']) != 0: #only human players shall pass
                    #remove player from plasma kill counter when they die
                    if stats['DATA']['VICTIM']['NAME'] in self.plasma_stats:
                        self.plasma_stats[stats['DATA']['VICTIM']['NAME']] = 0

                    #count player world deaths
                    if stats['DATA']['MOD'] in self.world_death_types:
                        victim_name = stats['DATA']['VICTIM']['NAME']
                        if victim_name not in self.world_death_stats:
                            self.world_death_stats[victim_name] = 1
                        else:
                            self.world_death_stats[victim_name] += 1

            elif stats['TYPE'] == "PLAYER_KILL" and stats['DATA']['MOD'] == "PLASMA":
                killer_name = stats['DATA']['KILLER']['NAME']
                if killer_name != stats['DATA']['VICTIM']['NAME']:
                    if killer_name not in self.plasma_stats:
                        self.plasma_stats[killer_name] = 1
                    else:
                        self.plasma_stats[killer_name] += 1

                    if self.plasma_stats[killer_name] == 1:
                        self.handle_plasma_stats(killer_name)
            elif stats['TYPE'] == "PLAYER_KILL" and stats['DATA']['MOD'] == "KAMIKAZE":
                killer_name = stats['DATA']['KILLER']['NAME']
                if killer_name != stats['DATA']['VICTIM']['NAME']:
                    if killer_name not in self.kamikaze_stats:
                        self.kamikaze_stats[killer_name] = 1
                    else:
                        self.kamikaze_stats[killer_name] += 1

                    if self.kamikaze_stats[killer_name] == 1:
                        self.handle_kamikaze_stats(killer_name)

        if stats['TYPE'] == "PLAYER_STATS":
            #these stats come at end of game after MATCH_REPORT for each player
            if stats['DATA']['QUIT'] == 0 and stats['DATA']['WARMUP'] == 0:
                player_name = stats['DATA']['NAME']

                #player accuracies (sent to each player in tell)
                if int(stats['DATA']['STEAM_ID']) != 0:
                    player = self.player(int(stats['DATA']['STEAM_ID']))
                    #dont show if player is in spec, also handle multiple output bug as well
                    if player.team != "spectator" and player.steam_id not in self.outputted_accuracy_players:
                        accuracy_output = "^2YOUR ACCURACY:"
                        for weapon in self.weapon_accuracies:
                            weapon_shots = stats['DATA']['WEAPONS'][weapon]["S"]
                            weapon_hits = stats['DATA']['WEAPONS'][weapon]["H"]
                            if weapon_shots > 0:
                                if weapon_hits > 0:
                                    weapon_accuracy = 100 * (weapon_hits / weapon_shots)
                                else:
                                    weapon_accuracy = 0.00
                                accuracy_output += " - ^3{}: ^1{:0.2f}".format(weapon, weapon_accuracy)
                        player.tell(accuracy_output)
                        self.outputted_accuracy_players.append(player.steam_id)

                if stats['DATA']['PLAY_TIME'] > 0:
                    player_kpm = stats['DATA']['KILLS'] / (stats['DATA']['PLAY_TIME'] / 60)
                else:
                    player_kpm = 0

                if stats['DATA']['DEATHS'] != 0: #we don't want to divide by 0!
                    player_kd = stats['DATA']['KILLS'] / stats['DATA']['DEATHS']
                else:
                    player_kd = stats['DATA']['KILLS']

                player_dmg = stats['DATA']['DAMAGE']['DEALT']
                player_longest_spree = stats['DATA']['MAX_STREAK']

                player_rail_hits = 0
                player_rail_shots = 0

                if stats['DATA']['WEAPONS']['RAILGUN']['H'] >= 6:
                    player_rail_hits = stats['DATA']['WEAPONS']['RAILGUN']['H']
                    player_rail_shots = stats['DATA']['WEAPONS']['RAILGUN']['S']
                    player_rail_accuracy = 100 * (player_rail_hits / player_rail_shots)
                else:
                    player_rail_accuracy = 0

                player_nade_kills = stats['DATA']['WEAPONS']['GRENADE']['K']
                player_pummels = stats['DATA']['WEAPONS']['GAUNTLET']['K']                
                player_dmg_taken = stats['DATA']['DAMAGE']['TAKEN']

                if not self.best_kpm_names:
                    self.best_kpm_names = [player_name]
                    self.best_kpm = player_kpm
                elif player_kpm > self.best_kpm:
                    self.best_kpm_names = [player_name]
                    self.best_kpm = player_kpm
                elif player_kpm == self.best_kpm:
                    self.best_kpm_names.append(player_name)

                if not self.best_kd_names:
                    self.best_kd_names = [player_name]
                    self.best_kd = player_kd
                elif player_kd > self.best_kd:
                    self.best_kd_names = [player_name]
                    self.best_kd = player_kd
                elif player_kd == self.best_kd:
                    self.best_kd_names.append(player_name)

                if not self.most_damage_names:
                    self.most_damage_names = [player_name]
                    self.most_damage = player_dmg
                elif player_dmg > self.most_damage:
                    self.most_damage_names = [player_name]
                    self.most_damage = player_dmg
                elif player_dmg == self.most_damage:
                    self.most_damage_names.append(player_name)
                    
                if not self.longest_spree:
                    self.longest_spree_names = [player_name]
                    self.longest_spree = player_longest_spree
                elif player_longest_spree > self.longest_spree:
                    self.longest_spree_names = [player_name]
                    self.longest_spree = player_longest_spree
                elif player_longest_spree == self.longest_spree:
                    self.longest_spree_names.append(player_name)  
                    
                if not self.best_rail_accuracy_names:
                    self.best_rail_accuracy_names = [player_name]
                    self.best_rail_accuracy = player_rail_accuracy
                    self.best_rail_hits = player_rail_hits
                    self.best_rail_shots = player_rail_shots
                elif player_rail_accuracy > self.best_rail_accuracy:
                    self.best_rail_accuracy_names = [player_name]
                    self.best_rail_accuracy = player_rail_accuracy
                    self.best_rail_hits = player_rail_hits
                    self.best_rail_shots = player_rail_shots
                elif player_rail_accuracy == self.best_rail_accuracy:
                    self.best_rail_accuracy_names.append(player_name)

                if not self.most_nade_kills_names:
                    self.most_nade_kills_names = [player_name]
                    self.most_nade_kills = player_nade_kills
                elif player_nade_kills > self.most_nade_kills:
                    self.most_nade_kills_names = [player_name]
                    self.most_nade_kills = player_nade_kills
                elif player_nade_kills == self.most_nade_kills:
                    self.most_nade_kills_names.append(player_name)

                if not self.most_pummels_names:
                    self.most_pummels_names = [player_name]
                    self.most_pummels = player_pummels
                elif player_pummels > self.most_pummels:
                    self.most_pummels_names = [player_name]
                    self.most_pummels = player_pummels
                elif player_pummels == self.most_pummels:
                    self.most_pummels_names.append(player_name)
                    
                if not self.most_dmg_taken_names:
                    self.most_dmg_taken_names = [player_name]
                    self.most_dmg_taken = player_dmg_taken
                elif player_dmg_taken > self.most_dmg_taken:
                    self.most_dmg_taken_names = [player_name]
                    self.most_dmg_taken = player_dmg_taken
                elif player_dmg_taken == self.most_dmg_taken:
                    self.most_dmg_taken_names.append(player_name)    

    @minqlx.delay(2)
    @minqlx.thread
    def handle_game_end(self, data):
        if not data["ABORTED"]:
            stats_output = "^1KILL MACHINE: "
            for i, player_name in enumerate(self.best_kpm_names):
                stats_output += "^7" + player_name
                if len(self.best_kpm_names) > 1 and len(self.best_kpm_names) - 1 != i:
                    stats_output += ", "
            stats_output += "^2 - {:0.2f} kills/min".format(self.best_kpm)
            self.msg(stats_output)

            stats_output = "^1BEST COUNTERSTRIKE PLAYER: "
            for i, player_name in enumerate(self.best_kd_names):
                stats_output += "^7" + player_name
                if len(self.best_kd_names) > 1 and len(self.best_kd_names) - 1 != i:
                    stats_output += ", "
            stats_output += "^2 - {:0.2f} K/D ratio".format(self.best_kd)
            self.msg(stats_output)

            stats_output = "^1DESTRUCTICATOR: "
            for i, player_name in enumerate(self.most_damage_names):
                stats_output += "^7" + player_name
                if len(self.most_damage_names) > 1 and len(self.most_damage_names) - 1 != i:
                    stats_output += ", "
            stats_output += "^2 - {:,} dmg given".format(self.most_damage)

            self.msg(stats_output)
            time.sleep(3)

            if self.longest_spree > 1:
                stats_output = "^1RAMBO: "
                for i, player_name in enumerate(self.longest_spree_names):
                    stats_output += "^7" + player_name
                    if len(self.longest_spree_names) > 1 and len(self.longest_spree_names) - 1 != i:
                        stats_output += ", "
                stats_output += "^2 - {} kill streak".format(self.longest_spree)
                self.msg(stats_output)

            if self.best_rail_accuracy > 0:
                stats_output = "^1LASER EYES: "
                for i, player_name in enumerate(self.best_rail_accuracy_names):
                    stats_output += "^7" + player_name
                    if len(self.best_rail_accuracy_names) > 1 and len(self.best_rail_accuracy_names) - 1 != i:
                        stats_output += ", "
                stats_output += "^2 - {:0.2f} percent rail accuracy ({} hits / {} shots)".format(self.best_rail_accuracy, self.best_rail_hits, self.best_rail_shots)
                self.msg(stats_output)      
            
            if self.most_nade_kills > 0:
                stats_output = "^3PINEAPPLE POWER: "
                for i, player_name in enumerate(self.most_nade_kills_names):
                    stats_output += "^7" + player_name
                    if len(self.most_nade_kills_names) > 1 and len(self.most_nade_kills_names) - 1 != i:
                        stats_output += ", "
                stats_output += "^2 - {} grenade kills".format(self.most_nade_kills)
                self.msg(stats_output)    

            time.sleep(2)

            if self.most_pummels > 0:
                stats_output = "^1PUMMEL LORD: "
                for i, player_name in enumerate(self.most_pummels_names):
                    stats_output += "^7" + player_name
                    if len(self.most_pummels_names) > 1 and len(self.most_pummels_names) - 1 != i:
                        stats_output += ", "
                stats_output += "^2 - {} pummels".format(self.most_pummels)
                self.msg(stats_output)

            stats_output = "^6BIGGEST PINCUSHION: "
            for i, player_name in enumerate(self.most_dmg_taken_names):
                stats_output += "^7" + player_name
                if len(self.most_dmg_taken_names) > 1 and len(self.most_dmg_taken_names) - 1 != i:
                    stats_output += ", "
            stats_output += "^2 - {:,} ^6dmg taken".format(self.most_dmg_taken)
            self.msg(stats_output)

            stats_output = "^6CLUMSIEST FOOL: "
            for name, world_deaths in self.world_death_stats.items():
                if not self.most_world_deaths_names:
                    self.most_world_deaths_names = [name]
                    self.most_world_deaths = world_deaths
                elif world_deaths > self.most_world_deaths:
                    self.most_world_deaths_names = [name]
                    self.most_world_deaths = world_deaths
                elif world_deaths == self.most_world_deaths:
                    self.most_world_deaths_names.append(name)

            if self.most_world_deaths > 0:
                for i, player_name in enumerate(self.most_world_deaths_names):
                    stats_output += "^7" + player_name
                    if len(self.most_world_deaths_names) > 1 and len(self.most_world_deaths_names) - 1 != i:
                        stats_output += ", "
                stats_output += "^2 - {:,} deaths by world".format(self.most_world_deaths)
                self.msg(stats_output)

    @minqlx.delay(8)
    def handle_plasma_stats(self, player_name):
        if self.plasma_stats[player_name] >= 5:
            self.center_print("{}^6 PLASMORGASM".format(player_name))
            self.msg("{} ^6PLASMORGASM: ^7({} plasma kills in 8s)".format(player_name, self.plasma_stats[player_name]))
        self.plasma_stats[player_name] = 0

    @minqlx.delay(5)
    def handle_kamikaze_stats(self, player_name):
        kami_msg = "{}^7's ^3 KAMI: ^7{} ^1KILLS".format(player_name, self.kamikaze_stats[player_name])
        self.center_print(kami_msg)
        self.msg(kami_msg)
        self.kamikaze_stats[player_name] = 0

    def handle_game_start(self, data):
        self.best_kpm_names = []
        self.best_kpm = 0

        self.best_kd_names = []
        self.best_kd = 0

        self.most_damage_names = []
        self.most_damage = 0

        self.longest_spree_names = []
        self.longest_spree = 0

        self.best_rail_accuracy_names = []
        self.best_rail_accuracy = 0
        self.best_rail_hits = 0
        self.best_rail_shots = 0

        self.most_nade_kills_names = []
        self.most_nade_kills = 0

        self.most_pummels_names = []
        self.most_pummels = 0

        self.most_dmg_taken_names = []
        self.most_dmg_taken = 0

        self.world_death_stats = {}
        self.most_world_deaths_names = []
        self.most_world_deaths = 0

        self.kamikaze_stats = {}
        self.plasma_stats = {}
        self.outputted_accuracy_players = []
