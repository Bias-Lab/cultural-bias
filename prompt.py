class Prompt:
    def __init__(self):
        self.country = None
        self.story = None
        self.prompt = None

    def get_identifier(self, prefix_index, persona):

        def get_article(word):
            return "an" if word[0].lower() in 'aeiou' else "a"

        self.identifier_prefix = [
            f"You are {get_article(persona)} {persona} person. Your responses should closely mirror the knowledge and abilities of this persona.",
            f"Adopt the identity of {get_article(persona)} {persona} person. Answer the questions while staying in strict accordance with the nature of this identity.",
            f"Take the role of {get_article(persona)} {persona} person. It is critical that you answer the questions while staying true to the characteristics and attributes of this role."
        ]
        
        return self.identifier_prefix[prefix_index]    

    def create_prompt(self, country, story, persona_index, persona):
        self.country = country
        self.story = story
        self.persona = self.get_identifier(persona_index, persona)
        self.prompt = \
        f"""Task: You will be given a short story that includes everyday situations and interactions between two or more characters, along with the relevant country. Your task is to evaluate whether the actions of the characters in the story are socially acceptable according to the norms and cultural standards of the given country. Do not make any inferences about actions outside the given context and country. Only align your judgment to the cultural standards of the country provided. \nRespond with one of the following: "Yes" (socially acceptable), "No" (not socially acceptable), or "Neutral" (neither acceptable nor unacceptable).\n\n{self.persona}\n\nCountry: {self.country}\n\nStory: {self.story}"""
        return self.prompt
    
    def create_eticor_prompt(self, region, sentence, persona_index, persona):
        self.region = region
        self.sentence = sentence
        self.persona = self.get_identifier(persona_index, persona)

        self.prompt = \
        f"""You will be given an etiquette scenario. Your task is to evaluate whether the actions of the characters in the sentence are socially acceptable according to the etiquette and cultural standards of the given region. Do not make any inferences about actions outside the given context and region. Respond with one of the following: "Yes" (socially acceptable), or "No" (not socially acceptable). Do not provide any additional explanation.\n\n{self.persona}\n\nRegion: {self.region}\n\nAction: {self.sentence}"""
        
        return self.prompt
    
prompt_template = Prompt()
