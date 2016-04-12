class ArduinoValidator:

    def validate_percentage(self, percentage):
        is_valid = True

        if not str(percentage).isnumeric():
            is_valid = False
        elif int(percentage) < 0 or int(percentage) > 100:
            is_valid = False

        return is_valid

