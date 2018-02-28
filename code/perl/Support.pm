package Support;
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
    open(my $fh, "<:encoding(UTF-8)", $file) or die "$file: $!";

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

sub log_matches {
    my ($query, $offset, $page_size, $matches) = @_;
    printf(q{'%s'[%i:%i] = %s}, $query, $offset, $offset + $page_size,
            join(' ', @$matches));
    print "\n";
}

sub numbers_from_string {
    my $string = shift;
    return unless $string;
    my @all;
    while ($string =~ m/([\d\.]*\d[\d\.]*)/g) {
        push @all, $1;
    }
    return @all;
}

1;
