#include <fstream>
#include <string>
#include <vector>

bool csv_parse_line(std::ifstream & csv, std::vector<std::string> & fields);

std::string get_field(const std::string & data, size_t field);

bool max_number_in_string(const std::string & s, double *n_ptr);

bool first_number_in_string(const std::string & s, double *n_ptr);
