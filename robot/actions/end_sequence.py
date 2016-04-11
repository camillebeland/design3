from robot.action import Action


class EndSequenceAction(Action):
    def start(self):
        self.running = True
        print('Sequence is done')

    def stop(self):
        print("End sequence action asked to stop")
        self.running = False
