import PySide
from PySide.QtGui import QWindow
from PySide.QtGui import QApplication
from PySide.QtGui import QGridLayout
import pyqtgraph as pg

from org.vcolonnella.easylogchart.LogAnalyzer import LogAnalyzer

p = LogAnalyzer()
t_re = '^\[(?P<t3>\d{2})/(?P<t2>\d{2})/(?P<t1>\d{4}) (?P<t4>\d{2}):(?P<t5>\d{2}):(?P<t6>\d{2}),(?P<t7>\d{3})\]'
b_re = '\+\+ (\w+) '
e_re = '-- (\w+) '
c_re = '\[.*-8009-(\d+)\]'
p.parse('/home/folial/Lab/Informatica/dev/Python/pycharm/PycharmProjects/easy-log-chart/testset/qms_engine.log', t_re, b_re, e_re, c_re)
p.analyze()

for (sampleKey, sampleValue) in p.sampleData.items():
    print("Method %s at time %s: %d events with average duration %s" % (sampleKey[0], sampleKey[1], sampleValue.eventCount, sampleValue.avgDuration))
for category in p.sampleCategory:
    print("Found %s category" % category)
print("Completed analyze of %d results for %d categories" % (len(p.sampleData), len(p.sampleCategory)))

app = QApplication([])

# Create a simple dialog box
window = QWindow()
layout = QGridLayout()
window.setLayout(layout)
chart = pg.PlotWidget()
layout.addWidget(chart)

window.show()
app.exec_()
pg.plot(p.sampleData)