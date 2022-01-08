
use strict;

my $target = 2020;

open(my $fd, "<", "input") or die "unable to open input file";
my %input_set = ();
my @input_list = ();
while (my $value = <$fd>) {
    $input_set{int($value)} = 1;
    push(@input_list, int($value));
}
close($fd);

my $count = 0;

@input_list = sort { $a <=> $b } (@input_list);

for (my $i1 = 0; $i1 < scalar(@input_list); $i1++) {
    my $value1 = $input_list[$i1];
    my $limit = $target - $value1;

    for (my $i2 = 0; $i2 < $i1; $i2++) {
        my $value2 = $input_list[$i2];
        if ($value2 > $limit) {
            last;
        }

        my $value3 = $limit - $value2;
        if (defined $input_set{$value3}) {
            # all three values are present
            my $result = $value1 * $value2 * $value3;
            print("$value1 + $value2 + $value3 = $target\n");
            print("$value1 * $value2 * $value3 = $result\n");
            delete $input_set{$value1};
            delete $input_set{$value2};
            delete $input_set{$value3};
            $count++;
        }
    }
}

if ($count > 1) {
    die "more than one possible answer";
}
if ($count < 1) {
    die "no answers";
}

