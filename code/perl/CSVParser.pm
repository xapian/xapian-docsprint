package CSVParser;
use strict;
use warnings;

use Text::CSV;

sub parse_csv {
    my $file = shift;
    my $csv = Text::CSV->new ({
                               eol => "\r\n",
                               sep_char => ',',
                               binary => 1,
                              })
      or die "Cannot use CSV: ".Text::CSV->error_diag ();
    open(my $fh, "<:encoding(utf8)", $file) or die "$file: $!";

    my $header = $csv->getline($fh);

    $csv->column_names(@$header);
    my @out;
    while (my $ref = $csv->getline_hr($fh)) {
        push @out, $ref;
    }
    $csv->eof or die $csv->error_diag();
    close $fh or die "$file: $!";
    return @out;
}

1;
