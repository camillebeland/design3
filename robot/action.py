class Action:
    def __init__(self, context, end_message):
        self._context = context
        self._end_message = end_message

    def start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

