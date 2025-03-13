import time

class EventDatabase:
    # other code no change

    def save_events(self, events):
        with open(self.json_file, "w") as file:
            json.dump([event.__dict__ for event in events], file, indent=4)
        backup_file = f"events_backup_{int(time.time())}.json"
        with open(backup_file, "w") as backup:
            json.dump([event.__dict__ for event in events], backup, indent=4)