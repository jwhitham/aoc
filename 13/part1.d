import std.stdio;
import std.string;
import std.conv;

void main(string[] args)
{
    int arrival_estimate = to!int(stdin.readln().strip());
    string bus_list = stdin.readln();
    int smallest_wait_time = int.max;
    int best_bus = 0;

    writeln(arrival_estimate);
    foreach (string item; bus_list.split(",")) {
        item = item.strip();
        if (item == "x") {
            continue;
        }
        int period = to!int(item);

        int num_journeys_before = arrival_estimate / period;
        int journey_before = num_journeys_before * period;
        if (journey_before == arrival_estimate) {
            smallest_wait_time = 0;
            best_bus = period;
        } else {
            int journey_after = journey_before + period;
            int wait_time = journey_after - arrival_estimate;
            if (wait_time < smallest_wait_time) {
                smallest_wait_time = wait_time;
                best_bus = period;
            }
        }
    }
    writeln("wait ", smallest_wait_time, " for bus ", best_bus);
    writeln("answer is ", smallest_wait_time * best_bus);
}

