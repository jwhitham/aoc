//! TreeList implements an indexed list in which
//! you can `insert`, `remove` and `get` values at any index with O(log N) time,
//! where N is the length of the list.
//!
//! Provided that values have always been unique, you can find an index for a value
//! in O(log N) time with the `find` method.
//!
//! In a conventional indexed list such as [`Vec`], it is possible to access values
//! in O(1) time, but inserting, removing, and finding by value requires O(N)
//! time in general cases. Insertion and removal require moving all of the following
//! items in the list, while finding by value requires a search of the whole list
//! in the worst case.
//!
//! TreeList is implemented using a self-balancing binary tree. These are most commonly used
//! to implement ordered associative data structures, similar to [`HashMap`] but with values
//! stored in key order. But they can also be used to implement indexed data structures such
//! as lists, by using the index (or "rank") of each value as the ordering criteria. This
//! is not possible with most generic tree structures (e.g. [`std::collections::BTreeMap`])
//! because they do not provide structural information to the comparison function. Therefore,
//! TreeList uses its own binary tree implementation, which is an [AVL] tree based on pseudocode
//! from [Knuth's TAOCP] volume 3, "Sorting and Searching". 
//!
//! [AVL]: https://en.wikipedia.org/wiki/AVL_tree 
//! [Knuth's TAOCP]: https://en.wikipedia.org/wiki/The_Art_of_Computer_Programming
//!
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

use std::collections::HashMap;

type InternalIndex = usize;
type ExternalIndex = usize;
type Direction = u8;
type Balance = i8;
const NO_INDEX: InternalIndex = usize::MAX;
const HEAD_INDEX: InternalIndex = 0;

/// TreeList implements an indexed list in which
/// you can `insert`, `remove` and `get` values at any index with O(log N) time,
/// where N is the length of the list.
///
/// Provided that values have always been unique, you can find an index for a value
/// in O(log N) time with the `find` method.
pub struct TreeList<ValueType> where ValueType: std::hash::Hash + Eq + std::default::Default + Clone {
    lookup: HashMap<ValueType, InternalIndex>,
    data: Vec<AVLNode<ValueType>>,
}

struct AVLNode<ValueType> {
    child: [InternalIndex; 2],
    value: ValueType,
    balance: Balance,
    direction: Direction,
    rank: ExternalIndex,
    parent: InternalIndex,
}

impl<ValueType> TreeList<ValueType> where ValueType: std::hash::Hash + Eq + std::default::Default + Clone {

    /// Makes a new, empty TreeList.
    pub fn new() -> Self {
        let mut s = TreeList {
            data: Vec::new(),
            lookup: HashMap::new(),
        };
        let c = s.new_node();
        assert_eq!(c, HEAD_INDEX);
        return s;
    }

    fn iget(self: &Self, index: InternalIndex) -> &AVLNode<ValueType> {
        return self.data.get(index).unwrap();
    }

    fn iget_mut(self: &mut Self, index: InternalIndex) -> &mut AVLNode<ValueType> {
        return self.data.get_mut(index).unwrap();
    }

    fn head(self: &Self) -> &AVLNode<ValueType> {
        return self.iget(HEAD_INDEX);
    }

    fn left_rank(self: &Self, index: InternalIndex) -> ExternalIndex {
        let c = self.iget(index).child[0];
        if c != NO_INDEX {
            return self.iget(c).rank;
        }
        return 0;
    }

    /// Returns the number of items in the list
    pub fn len(self: &Self) -> ExternalIndex {
        let c = self.head().child[1];
        if c == NO_INDEX {
            return 0;
        } else {
            return self.iget(c).rank;
        }
    }

    /// Returns the index where `value` can be found, or `None` if `value` is not present.
    ///
    /// Note: If values have not always been unique within the list, then the `find` method's
    /// return is not defined.
    pub fn find(self: &Self, value: ValueType) -> Option<ExternalIndex> {
        let pp: Option<&InternalIndex> = self.lookup.get(&value);

        if pp.is_none() {
            return None; // This value does not exist (or the rule about uniqueness wasn't followed)
        }
        let mut p: InternalIndex = *pp.unwrap();
        if self.iget(p).value != value {
            return None; // The value has changed, the rule about uniqueness wasn't followed
        }

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

    /// Returns a reference to the value at `index`, if `index` is less than the length of the list.
    /// Otherwise returns `None`.
    pub fn get(self: &Self, index: ExternalIndex) -> Option<&ValueType> {
        let mut p: InternalIndex = self.head().child[1];
        let mut ext_index_copy = index;

        loop {
            if p == NO_INDEX {
                return None; // index does not exist
            } else if ext_index_copy < self.left_rank(p) {
                p = self.iget(p).child[0];
            } else if ext_index_copy == self.left_rank(p) {
                return Some(&self.iget(p).value);  // index found
            } else {
                ext_index_copy -= self.left_rank(p) + 1;
                p = self.iget(p).child[1];
            }
        }
    }

    fn new_node(self: &mut Self) -> InternalIndex {
        let n: AVLNode<ValueType> = AVLNode {
            child: [NO_INDEX, NO_INDEX],
            value: Default::default(),
            balance: 0,
            direction: 0,
            rank: 0,
            parent: NO_INDEX,
        };
        self.data.push(n);
        return self.data.len() - 1;
    }

    fn free_node(self: &mut Self, remove_index: InternalIndex) {
        // Swap with the item at the end
        let replacement: AVLNode<ValueType> = self.data.pop().unwrap();
        let replacement_index: InternalIndex = self.data.len();

        if remove_index >= replacement_index {
            // remove_index was at the end, so nothing more is needed - it's gone!
            return;
        }

        // Change the index of "replacement" to be "remove_index" by making
        // new child-parent links
        if let Some(parent) = self.data.get_mut(replacement.parent) {
            for i in 0 .. 2 as Direction {
                if parent.child[i as usize] == replacement_index {
                    parent.child[i as usize] = remove_index;
                }
            }
        }
        for i in 0 .. 2 as Direction {
            if let Some(child) = self.data.get_mut(replacement.child[i as usize]) {
                child.parent = remove_index;
            }
        }

        // Change the index for this value
        self.lookup.insert(replacement.value.clone(), remove_index);

        // replace the node itself
        *self.data.get_mut(remove_index).unwrap() = replacement;
    }

    /// Insert `value` at `index`, causing the indexes of all items with index >= `index`
    /// to be increased by 1.
    pub fn insert(self: &mut Self, index: ExternalIndex, value: ValueType) {
        let mut p: InternalIndex = self.head().child[1];  // the pointer variable p will move down the tree
        let mut s: InternalIndex = self.head().child[1];  // s will point to the place where rebalancing may be necessary
        let mut t: InternalIndex = HEAD_INDEX;            // t will always point to the parent of s
        let mut q: InternalIndex;
        let r: InternalIndex;
        let mut direction: Direction;
        let mut s_index: ExternalIndex = index; // index at the point where rebalancing was necessary
        let mut c_index: ExternalIndex = index;

        if p == NO_INDEX {
            // empty tree special case
            let i = self.new_node();
            self.iget_mut(HEAD_INDEX).child[1] = i;
            let mut n = self.iget_mut(i);
            n.value = value.clone();
            n.direction = 1;
            n.rank = 1;
            n.parent = HEAD_INDEX;
            self.lookup.insert(value, i);
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
                n.value = value.clone();
                n.direction = direction;
                n.rank = 1;
                n.parent = p;
                n.balance = 0;
                self.iget_mut(p).child[direction as usize] = q;
                self.lookup.insert(value, q);
                break;
            }
        }

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

    /// Remove the value at `index`, causing the indexes of all items with index > `index`
    /// to be decreased by 1.
    pub fn remove(self: &mut Self, index: ExternalIndex) {
        let mut p: InternalIndex = self.head().child[1];
        let mut adjust_p: InternalIndex = HEAD_INDEX;
        let mut adjust_direction: Direction = 1;
        let mut c_index: ExternalIndex = index;

        if (p == NO_INDEX) || (index >= self.iget(p).rank) {
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
        let free_before_returning: InternalIndex;

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
            self.lookup.remove(&self.iget(q).value.clone());
            self.lookup.insert(self.iget(p).value.clone(), q);
            self.iget_mut(q).value = self.iget(p).value.clone();
            free_before_returning = p;
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
            self.lookup.remove(&self.iget(p).value.clone());
            self.iget_mut(adjust_p).child[adjust_direction as usize] = self.iget(p).child[0];
            self.iget_mut(self.iget(p).child[0]).parent = adjust_p;
            self.iget_mut(self.iget(p).child[0]).direction = adjust_direction;
            free_before_returning = p;
        } else {
            // Node has zero or one child - again easily removed.
            self.lookup.remove(&self.iget(p).value.clone());
            self.iget_mut(adjust_p).child[adjust_direction as usize] = self.iget(p).child[1];
            let c = self.iget(p).child[1];
            if c != NO_INDEX {
                self.iget_mut(c).parent = adjust_p;
                self.iget_mut(c).direction = adjust_direction;
            }
            free_before_returning = p;
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
                break;
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
                    break; // balanced after single rotation
                } else {
                    // unexpected balance value
                    panic!();
                }
            }
            adjust_direction = next_adjust_direction;
            adjust_p = next_adjust_p;
        }
        // Don't free any nodes while we have copies of the indexes, because
        // indexes will be invalidated.
        self.free_node(free_before_returning);
    }
}



#[test]
fn test() {
    use rand::rngs::StdRng;
    use rand::SeedableRng;
    use rand::Rng;
    type Rank = usize;
    type Depth = usize;
    type TestValueType = u16;
    type TestTreeList = TreeList<TestValueType>;

    fn get_max_depth(test_me: &TestTreeList, node: InternalIndex) -> Depth {
        let mut d1: Depth = 0;
        let mut d2: Depth = 0;
        let c1 = test_me.iget(node).child[0];
        if c1 != NO_INDEX {
            d1 = 1 + get_max_depth(test_me, c1);
        }
        let c2 = test_me.iget(node).child[1];
        if c2 != NO_INDEX {
            d2 = 1 + get_max_depth(test_me, c2);
        }
        return Depth::max(d1, d2);
    }

    fn get_balance(test_me: &TestTreeList, node: InternalIndex) -> Balance {
        let mut d1: Depth = 0;
        let mut d2: Depth = 0;
        let c1 = test_me.iget(node).child[0];
        if c1 != NO_INDEX {
            d1 = 1 + get_max_depth(test_me, c1);
        }
        let c2 = test_me.iget(node).child[1];
        if c2 != NO_INDEX {
            d2 = 1 + get_max_depth(test_me, c2);
        }
        return ((d2 as isize) - (d1 as isize)) as Balance;
    }

    fn get_rank(test_me: &TestTreeList, node: InternalIndex) -> Rank {
        let mut rank: Rank = 1;
        for i in 0 .. 2 {
            let c = test_me.iget(node).child[i];
            if c != NO_INDEX {
                rank += get_rank(test_me, c);
            }
        }
        return rank;
    }

    fn check_consistent_node(
            test_me: &TestTreeList,
            node: InternalIndex,
            visited: &mut HashMap<InternalIndex, bool>) {
       
        assert!(!visited.contains_key(&node));
        visited.insert(node, true);

        assert!(node < test_me.data.len());
        for i in 0 .. 2 as Direction {
            let child = test_me.iget(node).child[i as usize];
            if child != NO_INDEX {
                check_consistent_node(test_me, child, visited);
                assert_eq!(test_me.iget(child).parent, node);
                assert_eq!(test_me.iget(child).direction, i);
            }
        }
        let r = get_rank(test_me, node);
        assert_eq!(r, test_me.iget(node).rank);
        let x = get_balance(test_me, node);
        assert!(x >= -1);
        assert!(x <= 1);
        assert_eq!(x, test_me.iget(node).balance);
    }

    fn check_consistent(test_me: &TestTreeList) {
        if test_me.head().child[1] == NO_INDEX {
            return;
        }
        assert_eq!(test_me.iget(test_me.head().child[1]).parent, HEAD_INDEX);
        assert_eq!(test_me.iget(test_me.head().child[1]).direction, 1);
        let mut visited: HashMap<InternalIndex, bool> = HashMap::new();
        check_consistent_node(test_me, test_me.head().child[1], &mut visited);
    }

    fn check_with_list_node(test_me: &TestTreeList,
                            node: InternalIndex,
                            ref_list: &[TestValueType]) {
        let mut size: Rank = 0;
        let c1 = test_me.iget(node).child[0];
        if c1 != NO_INDEX {
            size += test_me.iget(c1).rank;
            check_with_list_node(test_me, c1, &ref_list[0 .. size]);
        }
        assert_eq!(ref_list[size], test_me.iget(node).value);

        let node2 = test_me.lookup.get(&test_me.iget(node).value);
        assert!(node2.is_some());
        assert_eq!(*node2.unwrap(), node);
        size += 1;

        let c2 = test_me.iget(node).child[1];
        if c2 != NO_INDEX {
            check_with_list_node(test_me, c2, &ref_list[size .. ref_list.len()]);
            size += test_me.iget(c2).rank;
        }
        assert_eq!(size, ref_list.len());
    }

    fn check_with_list(test_me: &TestTreeList, ref_list: &Vec<TestValueType>) {
        assert_eq!(test_me.lookup.len(), ref_list.len());
        assert_eq!(test_me.data.len(), ref_list.len() + 1); // +1 for HEAD_INDEX element
        assert_eq!(test_me.len(), ref_list.len());
        assert!(test_me.get(ref_list.len()).is_none());

        let c = test_me.head().child[1];
        if c == NO_INDEX {
            assert!(ref_list.len() == 0);
        } else {
            assert!(ref_list.len() != 0); // size of tree should be non-zero
            // size of 'lookup' hash should match size of tree if values are unique
            assert_eq!(test_me.iget(c).rank, test_me.lookup.len());
            check_with_list_node(test_me, c, &ref_list.as_slice());
        }
    }

    let mut test_me: TestTreeList = TreeList::new();
    let mut ref_list: Vec<TestValueType> = Vec::new();

    check_consistent(&test_me);
    check_with_list(&test_me, &ref_list);

    let mut rng = StdRng::seed_from_u64(1);
    let test_size: TestValueType = 1000;

    for k in 1 .. test_size + 1{
        let i = rng.gen_range(0 .. (ref_list.len() + 1) as TestValueType);
        test_me.insert(i as usize, k);
        ref_list.insert(i as usize, k);
        check_consistent(&test_me);
        check_with_list(&test_me, &ref_list);
    }
    for k in 1 .. test_size + 1 {
        let j = test_me.find(k);
        assert!(j.is_some());
        assert!(j.unwrap() < ref_list.len());
        assert!(ref_list[j.unwrap() ] == k);
    }
    for _ in 1 .. test_size + 1 {
        let i = rng.gen_range(0 .. ref_list.len() as TestValueType);
        test_me.remove(i as usize);
        ref_list.remove(i as usize);
        check_consistent(&test_me);
        check_with_list(&test_me, &ref_list);
    }
    for k in 1 .. (test_size * 10) + 1 {
        if rng.gen_ratio(1, 2) && (ref_list.len() > 0) {
            // test removing a random value
            let i: usize = (rng.gen_range(0 .. ref_list.len() as TestValueType)) as usize;
            let v: TestValueType = *ref_list.get(i).unwrap();

            assert_eq!(test_me.find(v).unwrap() as usize, i);
            ref_list.remove(i);
            test_me.remove(i);
        } else {
            // test adding a random value
            let i: usize = rng.gen_range(0 .. ref_list.len() + 1);
            ref_list.insert(i, k);
            test_me.insert(i, k);
            let j = test_me.find(k);
            assert_eq!(j.unwrap() as usize, i);
        }
        check_consistent(&test_me);
        check_with_list(&test_me, &ref_list);
    }
    while ref_list.len() > 0 {
        let i: usize = (rng.gen_range(0 .. ref_list.len() as TestValueType)) as usize;
        ref_list.remove(i);
        test_me.remove(i);
        check_consistent(&test_me);
        check_with_list(&test_me, &ref_list);
    }
}
