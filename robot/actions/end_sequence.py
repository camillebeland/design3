from robot.action import Action

class EndSequenceAction(Action):
    def start(self):
        print('Sequence is done')