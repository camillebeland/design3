import requests


class RobotService:
    def __init__(self, island_server_address):
        self.island_server_address = island_server_address

    def ask_target_island(self, manchester_letter):
        payload = {'code': manchester_letter}
        care_about_ssl_certificate = False
        response = requests.get(str(self.island_server_address), params=payload, verify=care_about_ssl_certificate)
        return response.text
