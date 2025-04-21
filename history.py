"""
Temperature history storage and averaging.
"""

import settings


class History:
    def __init__(self):
        self.reload()

    def reload(self):
        other = settings.other_settings()
        roms = [
            other.get("SENSOR_1_ROM"),
            other.get("SENSOR_2_ROM"),
            other.get("SENSOR_3_ROM"),
        ]
        self.data = {rom: [] for rom in roms}

    def update(self, temps):
        other = settings.other_settings()
        length = other.get("HISTORY_LENGTH")
        for rom, temp in temps.items():
            if rom in self.data:
                self.data[rom].append(temp)
                if len(self.data[rom]) > length:
                    self.data[rom].pop(0)

    def averages(self):
        # Return dict of average temps for sensors with data
        return {rom: sum(vals) / len(vals) for rom, vals in self.data.items() if vals}


# Singleton instance
history = History()
