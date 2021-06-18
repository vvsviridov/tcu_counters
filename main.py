import gzip
import glob
import datetime
import matplotlib.pyplot as plt

from lxml import etree


COUNTERS = []


def parser(xmlstring):
    tree = etree.fromstring(xmlstring)
    counters = tree.xpath(
        '//mv[./moid/text()="EthernetInterface=WAN"]/r/text()'
    )
    rop_time = tree.xpath('//cbt/text()')[0]
    csv_time = datetime.datetime.strptime(rop_time, '%Y%m%d%H%M')
    COUNTERS.append((csv_time, sum([int(c) for c in counters])))


def utilization():
    for t, octets in COUNTERS:
        mbits = octets*8/1024**2/900
        with open('result.csv', 'w') as f:
            f.write(f'{t};{mbits}\n')


def main():
    files = glob.glob('./TCU_PM0798/*.gz')
    files.sort()
    for file in files:
        unzipped = gzip.open(file, 'rb')
        xmlstring = unzipped.read()
        parser(xmlstring)
    utilization()
    plt.plot(
        [t[0] for t in COUNTERS],
        [t[1] for t in COUNTERS],
    )
    plt.show()


if __name__ == '__main__':
    main()
