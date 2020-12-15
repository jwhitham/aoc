import {Command, flags} from '@oclif/command'
import * as fs from 'fs';

const NUM_BITS: number = 36;


class FormatError extends Error {}

abstract class PartN {

    protected mask = "X".repeat(NUM_BITS);
    protected memory = new Map();


    public processInput(data: Buffer) {

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
                this.mask = rhs;
                let x = 0;
                for (let i = 0; i < NUM_BITS; i++) {
                    if (rhs.substr(i, 1) === "X") {
                        x++;
                    }
                }
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

                this.process(loc, value);

            } else {
                throw new FormatError("Unknown command: '" + line + "'");
            }

        }
        let total: bigint = 0n;
        for (let value of this.memory.values()) {
            total += value;
        }
        console.log("total is " + total);
    }

    protected abstract process(loc: bigint, value: bigint): void;
}

class Part1 extends PartN {
    private applyMask(newData: bigint): bigint {
        let bit: bigint = 1n;
        for (let i = NUM_BITS - 1; i >= 0; i--) {
            switch (this.mask.substr(i, 1)) {
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


    protected process(loc: bigint, value: bigint): void {
        this.memory.set(loc, this.applyMask(value));
    }
}

class Part2 extends PartN {

    protected process(loc: bigint, value: bigint): void {
        this.doFork(NUM_BITS - 1, 1n, loc, value);
    }

    private doFork(forkAt: number,
                   bit: bigint,
                   loc: bigint,
                   value: bigint) {

        for (let i = forkAt; i >= 0; i--) {
            switch (this.mask.substr(i, 1)) {
                case "0":
                    // unchanged
                    break;
                case "1":
                    // must be one
                    loc |= bit;
                    break;
                default:
                    loc &= ~bit;
                    this.doFork(i - 1, bit << 1n, loc, value);
                    loc |= bit;
                    this.doFork(i - 1, bit << 1n, loc, value);
                    return;
            }
            bit = bit << 1n;
        }
        this.memory.set(loc, value);
    }
}

class PartCommand extends Command {
    static description = 'AOC 2020 day 14 part 1'

    static flags = {
        version: flags.version({char: 'v'}),
        help: flags.help({char: 'h'}),
    }

    static args = [{name: 'file'}, {name: 'part'}]

    async run() {
        const {args, flags} = this.parse(PartCommand);

        if (!args.file) {
            args.file = "input";
        }
        if (!args.part) {
            args.part = "1";
        }
        switch (args.part) {
            case "1":
                fs.readFile(args.file, (err, data) => { new Part1().processInput(data); } );
                break;
            case "2":
                fs.readFile(args.file, (err, data) => { new Part2().processInput(data); } );
                break;
            default:
                throw new FormatError("Unknown part: " + args.part);
        }
    }
}

export = PartCommand;
