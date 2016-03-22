import requests


class TableCalibrationService:
    def __init__(self, host, port):
        self.calibration_data = {}
        while not self.calibration_data:
            try:
                self.calibration_data = requests.get('http://' + host + ':' + port + '/vision/calibration_data').json()
                print(self.calibration_data)
            except requests.exceptions.RequestException:
                print('can\'t fetch islands http://'+ host + ':' + port + '/vision/calibration_data' + ' is not available')
        self.pixel_per_meter_ratio = int(self.calibration_data['pixels_per_meter'])
        self.table_corners = self.calibration_data['table_corners']

    def get_pixel_per_meter_ratio(self):
        return self.pixel_per_meter_ratio

    def get_table_corners(self):
        return self.table_corners
