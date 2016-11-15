#include <xapian.h>

#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <ctime>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

bool
csv_parse_line(ifstream & csv, vector<string> & fields)
{
    fields.resize(0);

    char line[4096];
    if (!csv.getline(line, sizeof(line)))
	return false;

    // If the input has \r\n line endings, drop the \r.
    size_t gcount = csv.gcount();
    if (gcount > 1 && line[gcount - 1] == '\0' && line[gcount - 2] == '\r')
	line[gcount - 2] = '\0';

    bool in_quotes = false;
    string field;

    const unsigned END_OF_FIELD = 0x100;
    for (Xapian::Utf8Iterator i(line); i != Xapian::Utf8Iterator(); ++i) {
	unsigned ch = *i;

	if (!in_quotes) {
	    // If not already in double quotes, '"' starts quoting and
	    // ',' starts a new field.
	    if (ch == '"') {
		in_quotes = true;
		continue;
	    }
	    if (ch == ',')
		ch = END_OF_FIELD;
	} else if (ch == '"') {
	    // In double quotes, '"' either ends double quotes, or
	    // if followed by another '"', means a literal '"'.
	    if (++i == Xapian::Utf8Iterator())
		break;
	    ch = *i;
	    if (ch != '"') {
		in_quotes = false;
		if (ch == ',')
		    ch = END_OF_FIELD;
	    }
	}

	if (ch == END_OF_FIELD) {
	    fields.push_back(field);
	    field.resize(0);
	    continue;
	}

	Xapian::Unicode::append_utf8(field, ch);
    }
    fields.push_back(field);
    return true;
}

string
get_field(const string & data, size_t field)
{
    size_t start = 0;
    while (true) {
	size_t end = data.find('\n', start);
	if (field == 0)
	    return string(data, start, end - start);
	start = end;
	if (start != string::npos) ++start;
	--field;
    }
}

bool max_number_in_string(const string & s, double *n_ptr)
{
    istringstream is(s);
    bool found = false;
    double max = 0;
    while (!is.eof()) {
	double n;
        if (is >> n) {
	    if (!found || n > max) {
		max = n;
		found = true;
	    }
	} else {
	    is.clear();
	}
	// Skip character.
	(void)is.get();
    }
    *n_ptr = max;
    return found;
}

bool first_number_in_string(const string & s, double *n_ptr)
{
    istringstream is(s);
    while (!(is >> *n_ptr)) {
	is.clear();
	// Skip character.
	(void)is.get();
	if (is.eof()) return false;
    }
    return true;
}

string
format_date(const string& yyyymmdd)
{
    struct tm tm;
    tm.tm_year = 100;
    tm.tm_mon = atoi(yyyymmdd.substr(4, 2).c_str()) - 1;
    tm.tm_mday = 1;
    char month[20];
    strftime(month, sizeof(month), "%B", &tm);
    char date[40];
    sprintf(date, "%s %d, %d", month,
	    atoi(yyyymmdd.substr(6, 2).c_str()),
	    atoi(yyyymmdd.substr(0, 4).c_str()));
    return date;
}

string
format_numeral(string n)
{
    for (int pos = n.size() - 3; pos > 0; pos -= 3)
	n.insert(size_t(pos), ",");
    return n;
}

double
distance_between_coords(const pair<double, double>& a,
			const pair<double, double>& b)
{
    // For simplicity we treat these as planar coordinates and use
    // Pythagoras. Note that you should really use something like
    // Haversine; there's an implementation in Xapian's geo support.
    return sqrt(pow(a.first - b.first, 2) + pow(a.second - b.second, 2));
}
