require 'csv'

def parse_csv_file(datapath)
  CSV.read(datapath, headers: true)
end

def log_matches(querystring, offset, pagesize, matches)
  puts "'#{querystring}'[#{offset}:#{offset + pagesize}] = #{matches.join(' ')}"
end
