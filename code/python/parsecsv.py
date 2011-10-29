import csv

def parse_csv_file(datapath):
    fd = open(datapath)
    reader = csv.reader(fd)
    titles = reader.next()
    for row in reader:
        yield dict(zip(titles, map(lambda x: x.decode('iso-8859-1'), row)))
    fd.close()
