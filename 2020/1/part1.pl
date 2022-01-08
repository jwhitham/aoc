
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

foreach my $value1 (@input_list) {
    my $value2 = $target - $value1;
    if (defined $input_set{$value2}) {
        # both values are present
        my $result = $value1 * $value2;
        print("$value1 + $value2 = $target\n");
        print("$value1 * $value2 = $result\n");
        delete $input_set{$value1};
        delete $input_set{$value2};
        $count++;
    }
}

if ($count > 1) {
    die "more than one possible answer";
}
if ($count < 1) {
    die "no answers";
}

