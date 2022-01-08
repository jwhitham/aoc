
class Node {

    public value: bigint; // value of a node is the total below it
    public t: Node | null = null;
    public f: Node | null = null;

    constructor(value: bigint) {
        this.value = value;
    }

    public amend(new_key: string, new_value: bigint): void {
        if ((this.t == null) || (this.f == null)) {
            this.value = new_value;
            return;
        }

        if (new_key.substr(0, 1) === "X") {
            if (this.t !== this.f) {
                // graph is not X: fork the step
                this.t.amend(new_key.substr(1, new_key.length), new_value);
                this.f.amend(new_key.substr(1, new_key.length), new_value);
            } else {
                // graph is X: just continue
                this.t.amend(new_key.substr(1, new_key.length), new_value);
            }
        } else {
            if (this.t === this.f) {
                // graph is X: divide the graph
                this.t = this.t.copy_subtree();
            }

            // graph is not X: just continue
            if (new_key.substr(0, 1) === "1") {
                this.t.amend(new_key.substr(1, new_key.length), new_value);
            } else {
                this.f.amend(new_key.substr(1, new_key.length), new_value);
            }
        }

        // recombine if subtrees are equal
        if (this.t != this.f) {
            if (this.t.is_equal(this.f)) {
                this.t = this.f;
            }
        }

        // value of a node is the total below it
        this.value = this.t.value + this.f.value;
    }

    private copy_subtree(): Node {
        let copy = new Node(this.value);

        if ((this.t === null) || (this.f === null)) {
        } else if (this.t === this.f) {
            copy.t = copy.f = this.t.copy_subtree();
        } else {
            copy.t = this.t.copy_subtree();
            copy.f = this.f.copy_subtree();
        }
        return copy;
    }

    private is_equal(other: Node): boolean {
        if (this.value !== other.value) {
            return false;
        } else if ((this.t === null) || (this.f === null)) {
            return true;
        } else if (this.t === this.f) {
            if ((other.t !== null) && (other.f !== null) && (other.t === other.f)) {
                return this.t.is_equal(other.t);
            }
            return false;
        } else {
            if ((other.t !== null) && (other.f !== null) && (other.t !== other.f)) {
                return this.t.is_equal(other.t) && this.f.is_equal(other.f);
            }
            return false;
        }
    }
}

export class Puzzle {

    private key_size: number;
    private root: Node;

    constructor(key_size: number) {
        this.key_size = key_size;
        this.root = new Node(0n);
        let previous = this.root;

        for (let position = 0; position <= key_size; position++) {
            let here = new Node(0n);
            previous.t = here;
            previous.f = here;
            previous = here;
        }
    }

    public amend(new_key: string, new_value: bigint): void {
        this.root.amend(new_key, new_value);
    }

    public total(): bigint {
        return this.root.value;
    }
}

