# frozen_string_literal: true

require 'csv'
require 'date'

def parse_csv_file(datapath)
  CSV.read(datapath, headers: true)
end

def parse_states(datapath)
  CSV.read(datapath, headers: true).select { |r| r['order'] }
end

def log_matches(querystring, offset, pagesize, matches)
  puts "'#{querystring}'[#{offset}:#{offset + pagesize}] = #{matches.join(' ')}"
end

def numbers_from_string(string)
  out = []
  string.scan(/[\d.]*\d[\d.]*/) do |n|
    out << n.to_f
  end
  out
end

def format_numeral(numeral, sep: ',')
  raise 'Numeral must be an int type to format' unless numeral.is_a?(Integer)

  out = []
  numeral.to_s.split('').reverse.each_with_index do |s, i|
    out << sep if i.positive? && (i % 3).zero? && i != numeral.to_s.size
    out << s
  end
  out.reverse.join('')
end

def format_date(datestr)
  raise "Could not parse date to format 'YYYYMMDD'" unless datestr.is_a? String

  date = DateTime.strptime(datestr, '%Y%m%d')
  "#{date.strftime('%B')} #{date.day}, #{date.year}"
end
