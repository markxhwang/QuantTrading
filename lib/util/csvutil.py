import csv

def readCsvTo2dDict(file,keyfield):
    print("Reading csv file:"+file)
    with open(file, 'r') as f:
        csvreader = csv.DictReader(f, delimiter=',')
        m = {}
        for mline in csvreader:
            m[mline[keyfield]] = mline
    return m

def writeDictToCsv(m,file,header,delimiter = ','):
    print("Writing csv file:"+file)
    with open(file, 'w') as f:
        w = csv.DictWriter(f, delimiter=delimiter, fieldnames=header)
        headers = {}
        for n in header:
            headers[n] = n
            w.writerow(headers)
            for row in m:
                w.writerow(row)
    return