#include <fstream>
#include <string>
#include <vector>

bool csv_parse_line(std::ifstream & csv, std::vector<std::string> & fields);

std::string get_field(const std::string & data, size_t field);
