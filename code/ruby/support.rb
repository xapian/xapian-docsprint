# frozen_string_literal: true

require 'csv'

def parse_csv_file(datapath)
  CSV.read(datapath, headers: true)
end

def log_matches(querystring, offset, pagesize, matches)
  puts "'#{querystring}'[#{offset}:#{offset + pagesize}] = #{matches.join(' ')}"
end

def numbers_from_string(s)
  out = []
  s.scan(/[\d.]*\d[\d.]*/) do |n|
    out << n.to_f
  end
  return out
end
