#include <xapian.h>

#include <iostream>
#include <string>

using namespace std;

// Start of example code.
static void delete_docs(const string &dbpath, char ** identifiers)
{
    // Open the database we're going to be deleting from.
    Xapian::WritableDatabase db(dbpath, Xapian::DB_OPEN);

    while (*identifiers) {
	string idterm = "Q";
	idterm += *identifiers;
	db.delete_document(idterm);
	++identifiers;
    }
}
// End of example code.

int main(int argc, char** argv) {
    if (argc < 3) {
	cerr << "Usage: " << argv[0] << " DBPATH ID...\n";
	return 1;
    }
    delete_docs(argv[1], argv + 2);
}
