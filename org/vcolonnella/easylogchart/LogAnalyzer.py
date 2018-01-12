import re
import os
import math

from datetime import datetime
from org.vcolonnella.easylogchart.Event import Event
from org.vcolonnella.easylogchart.Sample import Sample


class LogAnalyzer:
    evtHist = {}
    sampleData = {}
    curEvt = {}
    minTime = datetime.max
    maxTime = datetime.min
    parseProgress = 0.0
    sampleSize = 300
    sampleCategory = set()
    sampleFreq = 0
    analyzeProgress = 0.0

    def parse(self, path, timeexpr, begin, end, channel):
        treg = re.compile(timeexpr)
        breg = re.compile(begin)
        ereg = re.compile(end)
        creg = re.compile(channel)
        totalParse = os.path.getsize(path)
        currentSize = 0
        with open(path) as logref:
            for logline in logref:
                currentSize += len(logline)
                self.parseProgress = float(currentSize) / float(totalParse)
                #print("Parsed %d bytes on %d total: %f%%" % (currentSize, totalParse, self.parseProgress * 100))
                bres = breg.search(logline)
                eres = None
                if bres is not None:
                    vname = bres.group(1)
                else:
                    eres = ereg.search(logline)
                    if eres is not None:
                        vname = eres.group(1)
                if bres is not None or eres is not None:
                    cres = creg.search(logline)
                    tres = treg.search(logline)
                    if cres is None or not cres.group(1) or tres is None or not tres.group(1):
                        continue
                    vchannel = cres.group(1)
                    vtime = datetime(int(tres.group('t1')), int(tres.group('t2')), int(tres.group('t3')), int(tres.group('t4')), int(tres.group('t5')), int(tres.group('t6')), int(tres.group('t7')) * 1000)
                if bres is not None:
                    event = Event(vname, vchannel, vtime)
                    self.curEvt[(vname, vchannel)] = event
                if eres is not None:
                    if (vname, vchannel) not in self.curEvt:
                        continue
                    self.curEvt[(vname, vchannel)].end = vtime
                    self.evtHist[(vname, vtime)] = self.curEvt[(vname, vchannel)]
                    del self.curEvt[(vname, vchannel)]
                if bres is not None or eres is not None:
                    self.minTime = vtime if vtime < self.minTime else self.minTime
                    self.maxTime = vtime if vtime > self.maxTime else self.maxTime

    def analyze(self):
        samplePeriod = (self.maxTime - self.minTime) / self.sampleSize
        totalAnalyze = float(len(self.evtHist))
        currentAnalyze = 0.0
        for vkey, event in self.evtHist.items():
            currentAnalyze += 1
            vname = vkey[0]
            vtime = vkey[1]
            timeKey = self.minTime + samplePeriod * math.floor((vtime - self.minTime) / samplePeriod)
            if (vname, timeKey) in self.sampleData:
                currentsample = self.sampleData[(vname, timeKey)]
                currentsample.eventCount
                currentduration = event.end - event.start
                currentsample.avgDuration = ((currentsample.avgDuration * currentsample.eventCount) + currentduration) / (currentsample.eventCount + 1)
                if currentduration < currentsample.minDuration:
                    currentsample.minDuration = currentduration
                if currentduration > currentsample.maxDuration:
                    currentsample.maxDuration = currentduration
                currentsample.eventCount += 1
            else:
                self.sampleData[(vname, timeKey)] = Sample(vname, timeKey, event.end - event.start)
                self.sampleCategory.add(vname)
            self.analyzeProgress = currentAnalyze / totalAnalyze
            #print("Analyzed %d bytes on %d total: %f%%" % (currentAnalyze, totalAnalyze, self.analyzeProgress * 100))