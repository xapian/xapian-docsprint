# frozen_string_literal: true

require 'csv'
require 'date'

def parse_csv_file(datapath)
  CSV.read(datapath, headers: true)
end

def parse_states(datapath)
  CSV.read(datapath, headers: true).select {|r| r['order'] }
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

def format_numeral(numeral, sep: ',')
  if numeral.is_a? Integer
    _numeral = []
    numeral.to_s.split('').reverse.each_with_index do |s,i|
      if i > 0 and i % 3 == 0 and i != numeral.to_s.size
        _numeral << sep
      end
      _numeral << s
    end
    return _numeral.reverse.join('')
  else
    raise "Numeral must be an int type to format"
  end
end

def format_date(datestr)
  if datestr.is_a? String
    _date = DateTime.strptime(datestr, '%Y%m%d')
    return "#{_date.strftime('%B')} #{_date.day}, #{_date.year}"
  else
    raise "Could not parse date to format 'YYYYMMDD'"
  end
end
