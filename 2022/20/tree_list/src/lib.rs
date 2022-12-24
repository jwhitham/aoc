//
// This data structure implements an indexed list (like a Vec) in which
// you can insert/remove/access elements at any index with O(log N) operations.
//
// Provided that element values are unique, you can find an element's index from
// its value in O(log N) time too.
//
// A balanced binary tree (AVL) is used.
// See https://en.wikipedia.org/wiki/AVL_tree for an introduction to AVL trees.
// This Adelson-Velsky and Landis (AVL) tree implementation comes from Knuth's TAOCP textbook,
// volume 3, "Sorting and Searching". Page numbers refer to the 1973 edition. I have used
// Knuth's variable names where possible and replicated the algorithm steps from the book.
//
// In this implementation:
// * the AVL tree acts as an indexed list of integers, with O(log N) insertion and removal
// * there is a "parent" reference at each node
// * there is also a "direction" at each node, such that node == node.parent.child[node.direction]
// * the rank of a node is the total number of nodes in its subtree (including itself)
// * children are numbered 0 and 1, so that rotation procedures can be generic
// * insert and remove operations are not recursive
// * a "head" node is always present so that the "empty" set is not a special case
//

use std::collections::HashMap;

type ValueType = usize;
type InternalIndex = usize;
type ExternalIndex = usize;
type Direction = u8;
type Balance = i8;
const NO_INDEX: InternalIndex = 10000;
const HEAD_INDEX: InternalIndex = NO_INDEX + 1;

pub struct TreeList {
    first: HashMap<ValueType, InternalIndex>,
    data: HashMap<InternalIndex, AVLNode>,
    next: InternalIndex,
}

struct AVLNode {
    child: [InternalIndex; 2],
    value: ValueType,
    balance: Balance,
    direction: Direction,
    rank: ExternalIndex,
    parent: InternalIndex,
}

impl TreeList {

    pub fn new() -> Self {
        let mut s = TreeList {
            next: HEAD_INDEX,
            data: HashMap::new(),
            first: HashMap::new(),
        };
        let c = s.new_node();
        assert_eq!(c, HEAD_INDEX);
        return s;
    }

    fn iget(self: &Self, index: InternalIndex) -> &AVLNode {
        return self.data.get(&index).unwrap();
    }

    fn iget_mut(self: &mut Self, index: InternalIndex) -> &mut AVLNode {
        return self.data.get_mut(&index).unwrap();
    }

    fn head(self: &Self) -> &AVLNode {
        return self.iget(HEAD_INDEX);
    }

    fn left_rank(self: &Self, index: InternalIndex) -> ExternalIndex {
        let c = self.iget(index).child[0];
        if c != NO_INDEX {
            return self.iget(c).rank;
        }
        return 0;
    }

    // Returns the number of items in the list
    pub fn len(self: &Self) -> ExternalIndex {
        let c = self.head().child[1];
        if c == NO_INDEX {
            return 0;
        } else {
            return self.iget(c).rank;
        }
    }

    // This returns the index where value can be found (if any).
    pub fn find(self: &Self, value: ValueType) -> Option<ExternalIndex> {
        let pp: Option<&InternalIndex> = self.first.get(&value);

        if pp.is_none() {
            return None; // This value does not exist
        }
        let mut p: InternalIndex = *pp.unwrap();
        assert_eq!(self.iget(p).value, value);

        let mut ext_index: ExternalIndex = self.left_rank(p);
        let end: InternalIndex = self.head().child[1];
        while p != end {
            if self.iget(p).direction == 1 {
                p = self.iget(p).parent;
                ext_index += self.left_rank(p) + 1;
            } else {
                p = self.iget(p).parent;
            }
        }
        return Some(ext_index);
    }

    // This returns the item at index (if index is less than the length of the list)
    pub fn get(self: &Self, ext_index: ExternalIndex) -> Option<ValueType> {
        let mut p: InternalIndex = self.head().child[1];
        let mut ext_index_copy = ext_index;

        loop {
            if p == NO_INDEX {
                return None; // index does not exist
            } else if ext_index_copy < self.left_rank(p) {
                p = self.iget(p).child[0];
            } else if ext_index_copy == self.left_rank(p) {
                return Some(self.iget(p).value);  // index found
            } else {
                ext_index_copy -= self.left_rank(p) + 1;
                p = self.iget(p).child[1];
            }
        }
    }

    fn new_node(self: &mut Self) -> InternalIndex {
        let n = AVLNode {
            child: [NO_INDEX, NO_INDEX],
            value: 0,
            balance: 0,
            direction: 0,
            rank: 0,
            parent: NO_INDEX,
        };
        self.data.insert(self.next, n);
        self.next += 1;
        return self.next - 1;
    }

    // Insert a new element at the given index. All items at greater indexes are shifted +1.
    pub fn insert(self: &mut Self, ext_index: ExternalIndex, value: ValueType) {
        let mut p: InternalIndex = self.head().child[1];  // the pointer variable p will move down the tree
        let mut s: InternalIndex = self.head().child[1];  // s will point to the place where rebalancing may be necessary
        let mut t: InternalIndex = HEAD_INDEX;            // t will always point to the parent of s
        let mut q: InternalIndex;
        let r: InternalIndex;
        let mut direction: Direction;
        let mut s_index: ExternalIndex = ext_index; // index at the point where rebalancing was necessary
        let mut c_index: ExternalIndex = ext_index;

        if p == NO_INDEX {
            // empty tree special case
            let i = self.new_node();
            self.iget_mut(HEAD_INDEX).child[1] = i;
            let mut n = self.iget_mut(i);
            n.value = value;
            n.direction = 1;
            n.rank = 1;
            n.parent = HEAD_INDEX;
            self.first.insert(value, i);
            return;
        }

        loop {
            if c_index <= self.left_rank(p) {
                // move left
                direction = 0;
            } else {
                // move right
                direction = 1;
                c_index -= self.left_rank(p) + 1;
            }

            // inserting something below p - therefore, rank of p increases
            self.iget_mut(p).rank += 1;

            q = self.iget(p).child[direction as usize];
            if q != NO_INDEX {
                // Continue search
                if self.iget(q).balance != 0 {
                    t = p;
                    s = q;
                    s_index = c_index;
                }
                p = q;
            } else {
                // New child (appending)
                q = self.new_node();
                let mut n = self.iget_mut(q);
                n.value = value;
                n.direction = direction;
                n.rank = 1;
                n.parent = p;
                self.iget_mut(p).child[direction as usize] = q;
                self.first.insert(value, q);
                break;
            }
        }

        self.iget_mut(q).value = value;
        self.iget_mut(q).balance = 0;
        // adjust balance factors
        c_index = s_index;
        if c_index <= self.left_rank(s) {
            p = self.iget(s).child[0];
            r = p;
        } else {
            c_index -= self.left_rank(s) + 1;
            p = self.iget(s).child[1];
            r = p;
        }
        while p != q {
            if c_index <= self.left_rank(p) {
                self.iget_mut(p).balance = -1;
                p = self.iget(p).child[0];
            } else {
                c_index -= self.left_rank(p) + 1;
                self.iget_mut(p).balance = 1;
                p = self.iget(p).child[1];
            }
        }
        // A7 balancing act
        let a: Balance;
        if s_index <= self.left_rank(s) {
            a = -1;
            direction = 0;
        } else {
            a = 1;
            direction = 1;
        }
        if self.iget(s).balance == 0 {
            // case i. The tree has grown higher
            self.iget_mut(s).balance = a;
            return;
        } else if self.iget(s).balance == -a {
            // case ii. The tree has gotten more balanced
            self.iget_mut(s).balance = 0;
            return;
        }
        // case iii. The tree is not balanced
        // note: r = s.child[direction]
        if self.iget(r).balance == a {
            // page 454 case 1
            p = self.single_rotation(r, s, direction);
            self.rerank(s);
            self.rerank(r);
            self.rerank(p);
        } else if self.iget(r).balance == -a {
            // page 454 case 2
            p = self.double_rotation(r, s, direction);
            self.rerank(s);
            self.rerank(r);
            self.rerank(p);
        } else {
            // unbalanced in an unexpected way
            panic!();
        }
        // A10 finishing touch
        if s == self.iget(t).child[1] {
            self.iget_mut(t).child[1] = p;
            self.iget_mut(p).parent = t;
            self.iget_mut(p).direction = 1;
        } else {
            self.iget_mut(t).child[0] = p;
            self.iget_mut(p).parent = t;
            self.iget_mut(p).direction = 0;
        }
    }

    fn single_rotation(self: &mut Self, r: InternalIndex, s: InternalIndex, direction: Direction) -> InternalIndex {
        // page 457 A8 single rotation
        // as applied to case 1 (top of page 454) in which s is A and r is B
        // Initially r is a child of s. In the book, direction = 1, as follows:
        //
        //      |               ->            |
        //      s               ->            r
        //    /   \        SingleRotation   /   \
        // alpha   r            ->        s     gamma
        //       /   \          ->      /   \
        //    beta   gamma      ->  alpha   beta
        //
        // direction = 0 is the same operation applied to a mirror image.

        let p = r;
        self.iget_mut(s).child[direction as usize] = self.iget(r).child[1 - direction as usize];   // beta subtree moved from r to s
        self.iget_mut(r).child[1 - direction as usize] = s;                    // node r becomes child of s
        self.iget_mut(s).balance = 0;
        self.iget_mut(r).balance = 0;
        self.iget_mut(s).direction = 1 - direction;
        self.iget_mut(s).parent = r;

        if self.iget(s).child[direction as usize] != NO_INDEX {
            let c = self.iget(s).child[direction as usize];
            self.iget_mut(c).parent = s;
            self.iget_mut(c).direction = direction;
        }
        return p;
    }

    fn double_rotation(self: &mut Self, r: InternalIndex, s: InternalIndex, direction: Direction) -> InternalIndex {
        // A9 double rotation
        // as applied to case 2 (top of page 454) in which s is A, r is B, and p is X
        // Initially r is a child of s. In the book, direction = 1, as follows:
        //
        //         |            ->                     |
        //         s            ->                     p
        //       /   \      DoubleRotation           /    \
        //    alpha   r         ->                 s        r  
        //          /   \       ->               /   \    /   \
        //         p    delta   ->           alpha beta gamma delta
        //       /   \          ->
        //     beta  gamma      ->
        //
        // direction = 0 is the same operation applied to a mirror image.

        let a: Balance = if direction > 0 { 1 } else { -1 };

        let p: InternalIndex = self.iget(r).child[1 - direction as usize];              // p is child of r (node X in the book)
        self.iget_mut(r).child[1 - direction as usize] = self.iget(p).child[direction as usize]; // gamma subtree moved from p to r
        self.iget_mut(p).child[direction as usize] = r;                                 // r becomes child of p
        self.iget_mut(s).child[direction as usize] = self.iget(p).child[1 - direction as usize]; // beta subtree moved from p to s
        self.iget_mut(p).child[1 - direction as usize] = s;                             // s becomes child of p
        if self.iget(p).balance == a {
            self.iget_mut(s).balance = -a;
            self.iget_mut(r).balance = 0;
        } else if self.iget(p).balance == 0 {
            self.iget_mut(s).balance = 0;
            self.iget_mut(r).balance = 0;
        } else {
            self.iget_mut(s).balance = 0;
            self.iget_mut(r).balance = a;
        }
        self.iget_mut(p).balance = 0;

        self.iget_mut(s).parent = p;
        self.iget_mut(s).direction = 1 - direction;
        let sc = self.iget(s).child[direction as usize];
        if sc != NO_INDEX {
            self.iget_mut(sc).parent = s;
            self.iget_mut(sc).direction = direction;
        }

        self.iget_mut(r).parent = p;
        self.iget_mut(r).direction = direction;
        let rc = self.iget(r).child[1 - direction as usize];
        if rc != NO_INDEX {
            self.iget_mut(rc).parent = r;
            self.iget_mut(rc).direction = 1 - direction;
        }

        return p;
    }

    fn rerank(self: &mut Self, node: InternalIndex) {
        self.iget_mut(node).rank = 1;
        for i in 0 .. 2 {
            if self.iget(node).child[i] != NO_INDEX {
                self.iget_mut(node).rank += self.iget(self.iget(node).child[i]).rank;
            }
        }
    }

    // Remove the element at the specified index. All elements with greater indexes are shifted -1.
    pub fn remove(self: &mut Self, ext_index: ExternalIndex) {
        let mut p: InternalIndex = self.head().child[1];
        let mut adjust_p: InternalIndex = HEAD_INDEX;
        let mut adjust_direction: Direction = 1;
        let mut c_index: ExternalIndex = ext_index;

        if (p == NO_INDEX) || (ext_index >= self.iget(p).rank) {
            // unable to delete element outside of list
            return;
        }

        loop {
            if p == NO_INDEX {
                // this should not be possible due to the index check at the start of the Delete method
                panic!();
            }

            // element will be removed below p
            self.iget_mut(p).rank -= 1;
            if c_index < self.left_rank(p) {
                adjust_p = p;
                adjust_direction = 0;
                p = self.iget(p).child[0];
            } else if c_index > self.left_rank(p) {
                adjust_p = p;
                adjust_direction = 1;
                c_index -= self.left_rank(p) + 1;
                p = self.iget(p).child[1];
            } else {
                // found
                break;
            }
        }

        // found the node to delete (p)
        if (self.iget(p).child[0] != NO_INDEX) && (self.iget(p).child[1] != NO_INDEX) {
            // non-leaf node with two children being deleted
            // page 429 Tree deletion (is for a non-balanced binary tree)

            // In this case we find another node with 0 or 1 child which can be
            // deleted instead. We swap this node into the tree.

            // q - the node we would like to remove
            let q = p;
            adjust_p = p;
            adjust_direction = 1;

            // find p, a node we can actually remove
            p = self.iget(p).child[1];
            while self.iget(p).child[0] != NO_INDEX {
                self.iget_mut(p).rank -= 1;
                adjust_p = p;
                adjust_direction = 0;
                p = self.iget(p).child[0];
            }
            self.iget_mut(p).rank -= 1;

            // Now we found p, a node with zero or one child - easily removed:
            let p_child_1 = self.iget(p).child[1];

            // move p's contents to q
            let v = self.iget(q).value;
            self.first.remove(&v);
            self.first.insert(self.iget(p).value, q);
            self.iget_mut(q).value = self.iget(p).value;
            self.data.remove(&p); // free p
            p = q;

            // fix up a connection to p's child (if p had a child)
            self.iget_mut(adjust_p).child[adjust_direction as usize] = p_child_1;
            if p_child_1 != NO_INDEX {
                self.iget_mut(p_child_1).parent = adjust_p;
                self.iget_mut(p_child_1).direction = adjust_direction;
            }
            self.iget_mut(self.iget(p).child[0]).parent = p;
            self.iget_mut(self.iget(p).child[0]).direction = 0;
            if self.iget(p).child[1] != NO_INDEX {
                self.iget_mut(self.iget(p).child[1]).parent = p;
                self.iget_mut(self.iget(p).child[1]).direction = 1;
            }
        } else if self.iget(p).child[0] != NO_INDEX {
            // Node has one child - so it's easily removed:
            let v = self.iget(p).value;
            self.first.remove(&v);
            self.iget_mut(adjust_p).child[adjust_direction as usize] = self.iget(p).child[0];
            self.iget_mut(self.iget(p).child[0]).parent = adjust_p;
            self.iget_mut(self.iget(p).child[0]).direction = adjust_direction;
            self.data.remove(&p); // free p
        } else {
            // Node has zero or one child - again easily removed.
            let v = self.iget(p).value;
            self.first.remove(&v);
            self.iget_mut(adjust_p).child[adjust_direction as usize] = self.iget(p).child[1];
            let c = self.iget(p).child[1];
            if c != NO_INDEX {
                self.iget_mut(c).parent = adjust_p;
                self.iget_mut(c).direction = adjust_direction;
            }
            self.data.remove(&p); // free p
        }

        // The process of deleting node p sets parent.p.child[parent.direction]
        // and so the balance factor at parent.p is adjusted
        while self.iget(adjust_p).parent != NO_INDEX {
            let next_adjust_direction: Direction = self.iget(adjust_p).direction;
            let next_adjust_p: InternalIndex = self.iget(adjust_p).parent;
            let adjust_a: Balance = if adjust_direction == 1 { 1 } else { -1 };

            if self.iget(adjust_p).balance == adjust_a {
                // page 466 i: repeat adjustment procedure for parent
                self.iget_mut(adjust_p).balance = 0;
            } else if self.iget(adjust_p).balance == 0 {
                // page 466 ii: tree is balanced
                self.iget_mut(adjust_p).balance = -adjust_a;
                return;
            } else {
                // page 466 iii - rebalancing required
                let s = adjust_p; // parent of subtree requiring rotation
                let r = self.iget(adjust_p).child[1 - adjust_direction as usize]; // child requiring rotation is the OPPOSITE of the one removed

                if self.iget(r).balance == -adjust_a {
                    // page 454 case 1
                    p = self.single_rotation(r, s, 1 - adjust_direction);
                    self.iget_mut(next_adjust_p).child[next_adjust_direction as usize] = p;
                    self.iget_mut(p).parent = next_adjust_p;
                    self.iget_mut(p).direction = next_adjust_direction;
                    self.rerank(s);
                    self.rerank(r);
                    self.rerank(p);
                } else if self.iget(r).balance == adjust_a {
                    // page 454 case 2
                    p = self.double_rotation(r, s, 1 - adjust_direction);
                    self.iget_mut(next_adjust_p).child[next_adjust_direction as usize] = p;
                    self.iget_mut(p).parent = next_adjust_p;
                    self.iget_mut(p).direction = next_adjust_direction;
                    self.rerank(s);
                    self.rerank(r);
                    self.rerank(p);
                } else if self.iget(r).balance == 0 {
                    // case 3: like case 1 except that beta has height h + 1 (same as gamma)
                    p = self.single_rotation(r, s, 1 - adjust_direction);
                    self.iget_mut(next_adjust_p).child[next_adjust_direction as usize] = p;
                    self.iget_mut(adjust_p).balance = -adjust_a;
                    self.iget_mut(p).balance = adjust_a;
                    self.iget_mut(p).parent = next_adjust_p;
                    self.iget_mut(p).direction = next_adjust_direction;
                    self.rerank(s);
                    self.rerank(r);
                    self.rerank(p);
                    return; // balanced after single rotation
                } else {
                    // unexpected balance value
                    panic!();
                }
            }
            adjust_direction = next_adjust_direction;
            adjust_p = next_adjust_p;
        }
    }
}



#[test]
fn test() {
    type Rank = usize;
    type Depth = usize;

    fn get_max_depth(t: &TreeList, node: InternalIndex) -> Depth {
        let mut d1: Depth = 0;
        let mut d2: Depth = 0;
        let c1 = t.iget(node).child[0];
        if c1 != NO_INDEX {
            d1 = 1 + get_max_depth(t, c1);
        }
        let c2 = t.iget(node).child[1];
        if c2 != NO_INDEX {
            d2 = 1 + get_max_depth(t, c2);
        }
        return Depth::max(d1, d2);
    }

    fn get_balance(t: &TreeList, node: InternalIndex) -> Balance {
        let mut d1: Depth = 0;
        let mut d2: Depth = 0;
        let c1 = t.iget(node).child[0];
        if c1 != NO_INDEX {
            d1 = 1 + get_max_depth(t, c1);
        }
        let c2 = t.iget(node).child[1];
        if c2 != NO_INDEX {
            d2 = 1 + get_max_depth(t, c2);
        }
        return ((d2 as isize) - (d1 as isize)) as Balance;
    }

    fn get_rank(t: &TreeList, node: InternalIndex) -> Rank {
        let mut rank: Rank = 1;
        for i in 0 .. 2 {
            let c = t.iget(node).child[i];
            if c != NO_INDEX {
                rank += get_rank(t, c);
            }
        }
        return rank;
    }

    fn check_consistent_node(
            t: &TreeList,
            node: InternalIndex,
            visited: &mut HashMap<InternalIndex, bool>) {
       
        assert!(!visited.contains_key(&node));
        visited.insert(node, true);

        assert!(t.data.contains_key(&node));
        for i in 0 .. 2 as Direction {
            let child = t.iget(node).child[i as usize];
            if child != NO_INDEX {
                check_consistent_node(t, child, visited);
                assert_eq!(t.iget(child).parent, node);
                assert_eq!(t.iget(child).direction, i);
            }
        }
        let r = get_rank(t, node);
        assert_eq!(r, t.iget(node).rank);
        let x = get_balance(t, node);
        assert!(x >= -1);
        assert!(x <= 1);
        assert_eq!(x, t.iget(node).balance);
    }

    fn check_consistent(t: &TreeList) {
        if t.head().child[1] == NO_INDEX {
            return;
        }
        assert_eq!(t.iget(t.head().child[1]).parent, HEAD_INDEX);
        assert_eq!(t.iget(t.head().child[1]).direction, 1);
        let mut visited: HashMap<InternalIndex, bool> = HashMap::new();
        check_consistent_node(t, t.head().child[1], &mut visited);
    }

    fn check_with_list_node(t: &TreeList,
                            node: InternalIndex,
                            s: &[ValueType]) {
        let mut size: Rank = 0;
        let c1 = t.iget(node).child[0];
        if c1 != NO_INDEX {
            size += t.iget(c1).rank;
            check_with_list_node(t, c1, &s[0 .. size]);
        }
        assert_eq!(s[size], t.iget(node).value);

        let node2 = t.first.get(&t.iget(node).value);
        assert!(node2.is_some());
        assert_eq!(*node2.unwrap(), node);
        size += 1;

        let c2 = t.iget(node).child[1];
        if c2 != NO_INDEX {
            check_with_list_node(t, c2, &s[size .. s.len()]);
            size += t.iget(c2).rank;
        }
        assert_eq!(size, s.len());
    }

    fn check_with_list(t: &TreeList, s: &Vec<ValueType>) {
        assert_eq!(t.first.len(), s.len());
        assert_eq!(t.data.len(), s.len() + 1); // +1 for HEAD_INDEX element
        assert_eq!(t.len(), s.len());
        assert!(t.get(s.len()).is_none());

        let c = t.head().child[1];
        if c == NO_INDEX {
            assert!(s.len() == 0);
        } else {
            assert!(s.len() != 0); // size of tree should be non-zero
            // size of 'first' hash should match size of tree if values are unique
            assert_eq!(t.iget(c).rank, t.first.len());
            check_with_list_node(t, c, &s.as_slice());
        }
    }

    let mut t = TreeList::new();
    let mut s: Vec<ValueType> = Vec::new();

    check_consistent(&t);
    check_with_list(&t, &s);

    let mut r_state: u64 = 0x853c49e6748fea9b;
    let r_inc: u64 = 0xda3e39cb94b95bdb;
    let mut next_random = || -> ValueType {
        let oldstate = r_state;
        let (v, _) = oldstate.overflowing_mul(6364136223846793005);
        (r_state, _) = v.overflowing_add(r_inc);
        let xorshifted = ((oldstate >> 18) ^ oldstate) >> 27;
        let rot = oldstate >> 59;
        return (((xorshifted >> rot)
                 | (xorshifted << ((32 - rot) & 31)))
                    & 0xffffffff) as ValueType;
    };
    let test_size: ValueType = 1000;

    for k in 1 .. test_size + 1{
        let i = next_random() % ((s.len() + 1) as ValueType);
        t.insert(i as usize, k);
        s.insert(i as usize, k);
        check_consistent(&t);
        check_with_list(&t, &s);
    }
    for k in 1 .. test_size + 1 {
        let j = t.find(k);
        assert!(j.is_some());
        assert!(j.unwrap() < s.len());
        assert!(s[j.unwrap() ] == k);
    }
    for _ in 1 .. test_size + 1 {
        let i = next_random() % (s.len() as ValueType);
        t.remove(i as usize);
        s.remove(i as usize);
        check_consistent(&t);
        check_with_list(&t, &s);
    }
    for k in 1 .. (test_size * 10) + 1 {
        if ((next_random() % 2) == 0) && (s.len() > 0) {
            let i: usize = (next_random() % (s.len() as ValueType)) as usize;
            let v: ValueType = *s.get(i).unwrap();

            assert_eq!(t.find(v).unwrap() as usize, i);
            s.remove(i);
            t.remove(i);
        } else {
            let i: usize = (next_random() % ((s.len() + 1) as ValueType)) as usize;
            s.insert(i, k);
            t.insert(i, k);
            let j = t.find(k);
            assert_eq!(j.unwrap() as usize, i);
        }
        check_consistent(&t);
        check_with_list(&t, &s);
    }
    while s.len() > 0 {
        s.remove(0);
        t.remove(0);
        check_consistent(&t);
        check_with_list(&t, &s);
    }
}
