package Support;
use strict;
use warnings;
use Text::CSV;
use Data::Dumper;
use DateTime;
use DateTime::Format::Strptime;;

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

sub parse_states {
    my @records = parse_csv(@_);
    return grep { length($_->{order}) } @records;
}

sub format_numeral {
    my $number = shift;
    if ($number =~ m/\A[0-9]+\z/) {
        if ($number eq '0') {
            return $number;
        }
        else {
            my @out;
            my @all = reverse(split('', $number));
            for (my $i = 0; $i < @all; $i++) {
                if ($i and (($i % 3) == 0)) {
                    push @out, ',';
                }
                push @out, $all[$i];
            }
            return join('', reverse @out);
        }
    }
    else {
        die "Numeral should be an integer";
    }
}

sub format_date {
    my $date = shift;
    my $strp = DateTime::Format::Strptime->new(pattern => '%Y%m%d');
    my $dt = $strp->parse_datetime($date);
    return $dt->month_name . ' ' . $dt->day . ', ' . $dt->year;
};

1;
