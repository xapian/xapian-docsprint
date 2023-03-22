require 'csv'

def parse_csv_file(datapath)
  CSV.read(datapath, headers: true)
end
