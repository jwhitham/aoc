import std.stdio;
import std.string;
import std.conv;
import std.algorithm.sorting;
import std.algorithm.mutation : SwapStrategy;
import std.stdint;

struct Bus {
    uint64_t period;
    uint64_t offset;
    char[1] name;
}

bool order(Bus x, Bus y)
{
    return x.period > y.period;
}

void main(string[] args)
{
    Bus[] buses;

    {
        stdin.readln(); // ignore first line
        string bus_list = stdin.readln();
        int offset = 0;
        char name = 'a';

        foreach (string item; bus_list.split(",")) {
            Bus bus;

            item = item.strip();
            if (item != "x") {
                bus.period = to!uint64_t(item);
                bus.offset = offset;
                bus.name[0] = name;
                buses ~= [bus];
                name++;
            }
            offset++;
        }
    }

    sort!(order)(buses);

    foreach (Bus bus; buses) {
        writeln("t = ", bus.period, bus.name, " - ", bus.offset);
    }

    uint64_t best_delta = buses[0].period;
    int best_score = 1;
    writeln("initial best_delta = ", best_delta, " for 1 bus");

    for (uint64_t t0 = buses[0].period - buses[0].offset; ;
                t0 += best_delta) {
        bool ok = true;
        int score = 1;

        foreach (Bus bus; buses[1 .. $]) {
            uint64_t tN = t0 + bus.offset;

            if ((tN % bus.period) != 0) {
                ok = false;
                break;
            }
            score ++;
        }
        if (ok) {
            writeln("The time t is ", t0);
            break;
        }
        if (score > best_score) {
            best_score = score;
            best_delta = 1;
            foreach (Bus bus; buses[0 .. score]) {
                best_delta *= bus.period;
            }
            writeln("new best_delta = ", best_delta, " for ",
                            best_score, " buses");
        }
    }
}

