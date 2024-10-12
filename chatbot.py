import minqlx
import cohere

class chatbot(minqlx.Plugin):

    def __init__(self):
        super().__init__()

        self.add_command("chatbot", self.cmd_chatbot, usage="<message>")

        self.api_key = self.get_cvar("qlx_chatbot_api_key")

    @minqlx.thread
    def cmd_chatbot(self, player, msg, channel):
        if len(msg) < 2:
            return minqlx.RET_USAGE
        
        if not self.api_key:
            channel.reply("Missing Cohere API key for ChatBot")
            return
        
        co = cohere.Client(self.api_key)

        response = co.generate(
            model='command-nightly',
            prompt=" ".join(msg),
            max_tokens=300,
            temperature=0.9,
            k=0,
            p=0.75,
            stop_sequences=[],
            return_likelihoods='NONE'
        )

        output = response.generations[0].text
        channel.reply("^2ChatBot: ^7" + output)
        
