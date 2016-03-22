class ActionMachine:
    def __init__(self):
        self.__actions = {}
        self.__events = {}

    def register(self, name, action):
        self.__actions[name] = action

    def bind(self, event, action_name):
        assert(action_name in self.__actions)
        self.__events[event] = action_name

    def get_action_names(self):
        return list(self.__actions.keys())

    def get_events(self):
        return self.__events

    def notify_event(self, event):
        assert(event in self.__events)
        action_name = self.__events[event]
        action = self.__actions[action_name]
        action.start()
