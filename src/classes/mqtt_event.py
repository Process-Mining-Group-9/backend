class MqttEvent:
    def __init__(self, base, source, process, activity, payload):
        self.base: str = base
        self.source: str = source
        self.process: str = process
        self.activity: str = activity
        self.payload: str = payload

    def __str__(self):
        return f'{self.base}/{self.source}/{self.process}/{self.activity}: {self.payload}'
