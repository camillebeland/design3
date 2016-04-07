import threading


class TreasurePositionDeamon:
    def __init__(self, embedded_vision_service):
        self.embedded_vision_service = embedded_vision_service
        self.start_fetching_treasure_position_from_vision()

    def get_position_from_vision(self):
        self.embedded_vision_service.get_tracked_treasure_position()

    def __fetch_treasure_position_from_vision__(self):
        while self.running:
            self.embedded_vision_service.track_treasure()

    def start_fetching_treasure_position_from_vision(self):
        self.thread = threading.Thread(target=self.__fetch_treasure_position_from_vision__)
        self.running = True
        self.thread.start()

    def stop_fetching_robot_position_from_vision(self):
        self.running = False
