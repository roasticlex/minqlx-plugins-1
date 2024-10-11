#run this script in minqlx-plugins folder
mkdir soundcontrol
cd soundcontrol
touch soundbans.txt
touch category_sound_delays.txt
touch config.txt
printf "short\nmedium\nlong\nsoundautobanthreshold,none\nsoundautobanduration,none\n" >> config.txt
echo "soundcontrol folder and initial config files created"
