from datetime import datetime


class Sample:
    sampleName = ""
    sampleTime = datetime.min
    eventCount = 0
    avgDuration = 0.0
    minDuration = 0.0
    maxDuration = 0.0

    def __init__(self, name, time, duration):
        self.eventCount = 1
        self.sampleName = name
        self.sampleTime = time
        self.avgDuration = duration
        self.minDuration = duration
        self.maxDuration = duration
