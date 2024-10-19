<strong>bigbrother.py</strong> 
- automatically censors chat and returns censored verion of text
- requires an API key from: https://api-ninjas.com/api/profanityfilter
- set qlx_big_brother_api_key in server.cfg
- the free API will handle 10,000 requests a month

<strong>bot_antispec.py</strong> - fixes bug with bot_minplayers and teamsizes lower than player limit that causes bots to spec (kicks them)

<strong>chatbot.py</strong> - Cohere chatbot that responds to user chat
- run: "pip install chatterbot" and "pip install cohere"
- register and get an API key from https://dashboard.cohere.com/api-keys
- add to server.cfg: set qlx_chatbot_api_key <API KEY>
- !chatbot <message> - get a response from chatbot

<strong>crash.py</strong> - !crash for random crash noob intro sounds :D

<strong>discordbot.py</strong> - announce server stats to your Discord server!
- example output: https://i.gyazo.com/d52607e54225419f4ed61e3789b68181.png
- qlx_discord_channel_id and qlx_discord_bot_token MUST be set for this to work
- you also need to authenticate the bot with a gateway at least once for it to be able to send messages - for instance using https://github.com/roasticle/QLStats-Discord-Minimal - after it auths with the gateway once, you don't need to use the bot php script anymore
- see https://github.com/Just-Some-Bots/MusicBot/wiki/FAQ for creating the bot and also follow enabling developer mode
- once developer mode is enabled, right click on your Discord channel and copy id - use this for qlx_discord_channel_id
- optional cvar discord_chat_channel_id - this will output chat to the discord channel with the channel id specified

<strong>duke.py</strong> - Duke Nukem sound triggers
- requires http://steamcommunity.com/sharedfiles/filedetails/?id=572453229
- use !duke for random sound or !duke <soundname> (without .wav at the end).. list of sounds is on workshop page

<strong>gravityfixer.py</strong> - restores gravity to normal after maps with custom gravity
- in your server.cfg you will need to set qlx_alternateGravityMaps "mapname1,mapname2,etc" for each map that has an alternate gravity set 

<strong>fun.py</strong> - custom fun.py
- requires Dark Fiber Sound Pack - https://steamcommunity.com/sharedfiles/filedetails/?id=830745553 (add 830745553 to your servers workshop.txt and qlx_workshopReferences in server.cfg

<strong>funstuff.py</strong> - various fun vote functions
- !slaphappy <id or "everyone"> number_of_slaps frequency_in_seconds damage (damage is optional)
- !hulk <id or "everyone"> - gives player(s) massive amounts of hp, armor and powerups
- !rename <id or "everyone"> name_to_rename_to
- !gay - makes everyones name gay
- !straight - makes everyones name straight
- !purgatory <id or "everyone"> - sends player(s) off map
- !kill - kill everyone

<strong>gungames.py</strong> - custom voting triggers for gungames factories
- this REQUIRES workshop item: http://steamcommunity.com/sharedfiles/filedetails/?id=862639717
- if vote passes will reload current map with voted factory
- !gungames to show all available options
- available triggers: !glovelove !mgs !shotties !nades !rockets !lgs !rails !plasmas !bfgs !nails !mines !chainguns !hmg !kami !haste

<strong>intermissionplus.py</strong> - allow players to set custom victory songs
- set your songs in the py file SONGS list
- country anthems option <strong>REQUIRES</strong> http://steamcommunity.com/sharedfiles/filedetails/?id=1154034259 (add to workshop.txt and qlx_workshopReferences)
- players type !victorysongs to see song options and then !victorysong <song number> to set their victory song
- if no victory song is set your songs will be looped through as normal

<strong>mapoo.py</strong> - allows multiple mappool files that change automatically based on player number
- the mappool files should be all located in your baseq3 folder
- threshold variables are the number of players (in-game not spec) at which the mappool gets activated
- this requires 6 cvars to be set
- For example:
- set qlx_mapoo_small_file "mappool_ffa_small.txt"
- set qlx_mapoo_medium_file "mappool_ffa_medium.txt"
- set qlx_mapoo_large_file "mappool_ffa_large.txt"
- set qlx_mapoo_small_threshhold "1"
- set qlx_mapoo_medium_threshhold "6"
- set qlx_mapoo_large_threshhold "13"

<strong>motd.py</strong> - a replacement motd plugin that allows multiple motd/welcome sounds
- replace the default motd.py with this file
- add your motd sounds to the MOTD_SOUNDS list in the file

<strong>nextmap.py</strong> - announce nextmap and fix nextmap repeats
- NOTE: intended for servers with no end-game map voting
- announces nextmap at end of game or on !nextmap
- !currentmap to show..current map! (mind blowing i know!)

<strong>qltv.py</strong> - automatically spec the top player
- intended for FFA
- great for streaming
- updates every 10 frags
- !qltv to toggle

<strong>ragespec.py</strong> - !ragespec to...ragespec!

<strong>uberstats.py</strong> - various awards and stats added during and endgame
- !score for your scoreboard placement (when you are below the scoreboard during game)
- requires workshop item 1304624898 if you want weapon award sounds
- high scores shown on new map load or with !highscores trigger - !clearhighscores to clear them (admin only)
- example endgame output - https://thumb.gyazo.com/thumb/1200/_fb5d34fde51d1333da746ad90f25cf9f-png.jpg
- optional stats file SFTP upload setup:
  - requires pysftp, linux cmd line type: pip3 install pysftp 
  - requires following cvars: 
    - qlx_uberstats_sftp_hostname - sftp server hostname
    - qlx_uberstats_sftp_username
    - qlx_uberstats_sftp_password
    - qlx_uberstats_sftp_remote_path - remote path on sftp server where stats file will be uploads, format of file is hostname- uberstats.html
    - you can then include the file on your site, it will automatically fill in data to certain classes
    - records are the following (ignore the formatting codes): WEAPON_RECORDS = {
                    "kill_machine": ["KILL MACHINE", "{:0.2f} frags/min"],
                    "counterstrike": ["BEST COUNTERSTRIKE PLAYER", "{:0.2f} K/D ratio"],
                    "most_damage": ["DESTRUCTICATOR", "{:,} dmg given"],
                    "longest_spree": ["RAMBO", "{} kill streak"],
                    "best_rail_accuracy": ["LASER EYES", "{:0.2f} percent rail accuracy"],
                    "most_nade_kills": ["PINEAPPLE POWER", "{} grenade frags"],
                    "most_pummels": ["PUMMEL LORD", "{} pummels"],
                    "most_dmg_taken": ["BIGGEST PINCUSHION", "{:,} dmg taken"],
                    "most_world_deaths": ["CLUMSIEST FOOL", "{:,} deaths by world"],
                    "most_dmg_per_kill": ["GOOD SAMARITAN", "{:0.2f} damage per frag"]
                  }
     - so for instance, a span with the class "kill_machine_record and another with the class "kill_machine_players" would automatically fill the record and players into the span contents

<strong>weaponspawnfixer.py</strong> - override map-forced weapon spawn times
- <strong>REQUIRES</strong> at least minqlx 0.5.1
- will set all weapon spawn times to whatever g_weaponrespawn is set to
- for such maps as almostlost (5s grenade launcher), heroskeep (5s rocket launcher), verticalvengeance (10s railgun i think?) and bitterembrace (10s on all weapons..wtf?).. so for example g_weaponrespawn 1 would set all those respawn times to 1s instead :)

<strong>weather.py</strong> - lets you check weather and forecast in-game!
- you will need an API key (free) from https://www.wunderground.com/weather/api/d/login.html
- set qlx_WeatherUndergroundKey "YOURAPIKEYHERE" in your server.cfg
- usage: !weather (postal or zip code) or (countryname or state/city> - eg. !weather M4S1C4, !weather 90210, !weather USA/newyork, !weather CA/losangeles, !weather vostok, antarctica - using postal or zip code is usually best as it prevents multiple locations from being found (no data gets returned).

<strong>winneranthem.py</strong> - plays anthem for winner's country at end of match!
  - <strong>REQUIRES</strong> http://steamcommunity.com/sharedfiles/filedetails/?id=1154034259 (add to workshop.txt and qlx_workshopReferences)
  - <strong>NOTE:</strong> this conflicts with the intermission plugin so remove it from your qlx_plugins before use
  - will play Mr. Roboto when bots win match :P

Enjoy! :D - roasticle (roast on quakenet IRC). Donations are appreciated! You can Paypal me @ killernick@hotmail.com. Email/msg me if you are interested in having me develop a plugin for you.
