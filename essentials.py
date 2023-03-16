
class Participant():
    def __init__(self, age, gender, swedish_knowledge):
        self.ID = self.generate_unique_ID()
        self.age = age
        self.gender = gender
        self.swedish_knowledge = swedish_knowledge
        self.stimuli = {"verbal": [], "verbal_visual": []}

    def generate_unique_ID(self):
        pass

    def generate_random_stimulis(self):
        pass

class Stimuli():
    def __init__(self, visual, name, type_of_stimuli, length_of_stimuli, time_of_stimuli):
        self.visual = visual
        self.name = name
        self.type_of_stimuli = type_of_stimuli
        self.length_of_stimuli = length_of_stimuli
        self.time_of_stimuli = time_of_stimuli

