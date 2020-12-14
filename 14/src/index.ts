import {Command, flags} from '@oclif/command'
import * as fs from 'fs';

const NUM_BITS: number = 36;


class FormatError extends Error {}

function applyMask(newData: bigint, mask: string): BigInt {
    let bit: bigint = 1n;
    for (let i = NUM_BITS - 1; i >= 0; i--) {
        switch (mask.substr(i, 1)) {
            case "0":
                // must be zero
                newData &= ~bit;
                break;
            case "1":
                // must be one
                newData |= bit;
                break;
            default:
                // unchanged
                break;
        }
        bit = bit << 1n;
    }
    return newData;
}


function processInput(err: NodeJS.ErrnoException | null, data: Buffer) {

    let mask = "X".repeat(NUM_BITS);
    let memory = new Map();

    for (let line of data.toString().split("\n")) {
        let fields = line.split("=");

        if (fields.length != 2) {
            if (line !== "") {
                throw new FormatError("Formatting invalid: '" + line + "'");
            }
            continue;
        }

        let lhs = fields[0].trim();
        let rhs = fields[1].trim();

        if (lhs === "mask") {
            if (rhs.length !== NUM_BITS) {
                throw new FormatError("Mask size invalid: '" + line + "'");
            }
            mask = rhs;
        } else if (lhs.startsWith("mem[") && lhs.endsWith("]")) {
            let addr = lhs.substr(4, lhs.length - 5);
            let loc: bigint = 0n;
            let value: bigint = 0n;

            try {
                loc = BigInt(addr);
            } catch (Error) {
                throw new FormatError("Unknown decimal value: '" + addr + "'");
            }
            try {
                value = BigInt(rhs);
            } catch (Error) {
                throw new FormatError("Unknown decimal value: '" + rhs + "'");
            }

            memory.set(loc, applyMask(value, mask));

        } else {
            throw new FormatError("Unknown command: '" + line + "'");
        }

    }
    let total: bigint = 0n;
    for (let value of memory.values()) {
        total += value;
    }
    console.log("total is " + total);
}


class PartN extends Command {
    static description = 'AOC 2020 day 14 part 1'

    static flags = {
        version: flags.version({char: 'v'}),
        help: flags.help({char: 'h'}),
    }

    static args = [{name: 'file'}]

    async run() {
        const {args, flags} = this.parse(PartN);

        if (!args.file) {
            args.file = "input";
        }

        fs.readFile(args.file, processInput);

    }
}

export = PartN;
