import threading


class ChargingStationPositionDeamon:
    def __init__(self, embedded_vision_service):
        self.embedded_vision_service = embedded_vision_service

    def get_position_from_vision(self):
        return self.embedded_vision_service.get_recharge_station_position()

    def __fetch_charging_station_position_from_vision__(self):
        while True:
            self.embedded_vision_service.track_marker()

    def start_fetching_position_from_vision(self):
        self.running = True
        self.thread = threading.Thread(target=self.__fetch_charging_station_position_from_vision__)
        self.thread.start()

    def stop_fetching_position_from_vision(self):
        self.running = False
