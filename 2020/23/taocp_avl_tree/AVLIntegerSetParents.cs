using System;

// This Adelson-Velsky and Landis (AVL) tree implementation is based on AVLIntegerSet.cs
// but it uses child->parent links instead of a temporary stack.
// This design is more complex than AVLIntegerSet.cs.
//
// See https://en.wikipedia.org/wiki/AVL_tree for an introduction to AVL trees.
//
// In this implementation:
// * the AVL tree acts as an ordered set of integers, with O(log N) insertion and removal
// * there is a "parent" reference at each node
// * there is also a "direction" at each node, such that node == node.parent.child[node.direction]
// * children are numbered 0 and 1, so that rotation procedures can be generic
// * Insert and Delete operations are not recursive
// * a "head" node is always present so that the "empty" set is not a special case

namespace taocp_avl_tree
{

    public class AVLIntegerSetParents
    {
        protected AVLNode head;

        public AVLIntegerSetParents()
        {
            this.head = AVLNodeFactory();
        }

        protected virtual AVLNode AVLNodeFactory()
        {
            return new AVLNode();
        }

        protected class AVLNode
        {
            public AVLNode[] child = null;
            public int value = 0;
            public int balance = 0;
            public int direction = 0;
            public AVLNode parent = null;

            public AVLNode()
            {
                this.child = new AVLNode[2];
            }
        }

        // Insert returns true if already present, false if added
        public bool Insert(int k)
        {
            // page 455, A1
            AVLNode p = head.child[1];  // the pointer variable p will move down the tree
            AVLNode s = head.child[1];  // s will point to the place where rebalancing may be necessary
            AVLNode t = head;           // t will always point to the parent of s
            AVLNode q, r;
            int direction;

            if (p == null)
            {
                // empty tree special case
                head.child[1] = AVLNodeFactory();
                head.child[1].value = k;
                head.child[1].parent = head;
                head.child[1].direction = 1;
                return false;
            }

            while (true)
            {
                // A2
                if (k < p.value)
                {
                    // A3 - move left
                    direction = 0;
                }
                else if (k == p.value)
                {
                    // finished - node already present
                    return true;
                }
                else
                {
                    // A4 - move right
                    direction = 1;
                }
                // A3 or A4
                q = p.child[direction];
                if (q != null)
                {
                    // Continue search
                    if (q.balance != 0)
                    {
                        t = p;
                        s = q;
                    }
                    p = q;
                }
                else
                {
                    // New child
                    q = AVLNodeFactory();
                    p.child[direction] = q;
                    q.parent = p;
                    q.direction = direction;
                    break;
                }
            }

            // page 456 A5 Insert
            q.value = k;
            q.balance = 0;
            // A6 adjust balance factors
            if (k < s.value)
            {
                r = p = s.child[0];
            }
            else
            {
                r = p = s.child[1];
            }
            while (p != q)
            {
                if (k < p.value)
                {
                    p.balance = -1;
                    p = p.child[0];
                }
                else
                {
                    p.balance = 1;
                    p = p.child[1];
                }
            }
            // A7 balancing act
            int a;
            if (k < s.value)
            {
                a = -1;
                direction = 0;
            }
            else
            {
                a = 1;
                direction = 1;
            }
            if (s.balance == 0)
            {
                // case i. The tree has grown higher
                s.balance = a;
                return false;
            }
            else if (s.balance == -a)
            {
                // case ii. The tree has gotten more balanced
                s.balance = 0;
                return false;
            }
            // case iii. The tree is not balanced
            // note: r = s.child[direction]
            if (r.balance == a)
            {
                // page 454 case 1
                p = SingleRotation(r, s, direction);
            }
            else if (r.balance == -a)
            {
                // page 454 case 2
                p = DoubleRotation(r, s, direction);
            }
            else
            {
                throw new Exception("unbalanced in an unexpected way");
            }
            // A10 finishing touch
            if (s == t.child[1])
            {
                t.child[1] = p;
                p.parent = t;
                p.direction = 1;
            }
            else
            {
                t.child[0] = p;
                p.parent = t;
                p.direction = 0;
            }
            return false;
        }

        private AVLNode SingleRotation(AVLNode r, AVLNode s, int direction)
        {
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

            AVLNode p = r;
            s.child[direction] = r.child[1 - direction];   // beta subtree moved from r to s
            r.child[1 - direction] = s;                    // node s becomes child of r
            s.balance = 0;
            r.balance = 0;
            s.direction = 1 - direction;
            s.parent = r;
            if (s.child[direction] != null)
            {
                s.child[direction].parent = s;
                s.child[direction].direction = direction;
            }
            return p;
        }

        private AVLNode DoubleRotation(AVLNode r, AVLNode s, int direction)
        {
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

            int a = (direction > 0) ? 1 : -1;
            AVLNode p;

            p = r.child[1 - direction];                     // p is child of r (node X in the book)
            r.child[1 - direction] = p.child[direction];    // gamma subtree moved from p to r
            p.child[direction] = r;                         // r becomes child of p
            s.child[direction] = p.child[1 - direction];    // beta subtree moved from p to s
            p.child[1 - direction] = s;                     // s becomes child of p
            if (p.balance == a)
            {
                s.balance = -a;
                r.balance = 0;
            }
            else if (p.balance == 0)
            {
                s.balance = 0;
                r.balance = 0;
            }
            else
            {
                s.balance = 0;
                r.balance = a;
            }
            p.balance = 0;

            s.parent = p;
            s.direction = 1 - direction;
            if (s.child[direction] != null)
            {
                s.child[direction].parent = s;
                s.child[direction].direction = direction;
            }
            r.parent = p;
            r.direction = direction;
            if (r.child[1 - direction] != null)
            {
                r.child[1 - direction].parent = r;
                r.child[1 - direction].direction = 1 - direction;
            }
            return p;
        }


        // Delete returns true if removed and false if not present
        public bool Delete(int k)
        {
            AVLNode p = head.child[1];
            AVLNode adjust_p = head;
            int adjust_direction = 1;

            while (true)
            {
                if (p == null)
                {
                    // not found
                    return false;
                }
                else if (k < p.value)
                {
                    adjust_p = p;
                    adjust_direction = 0;
                    p = p.child[0];
                }
                else if (k > p.value)
                {
                    adjust_p = p;
                    adjust_direction = 1;
                    p = p.child[1];
                }
                else
                {
                    // found
                    break;
                }
            }

            // found the node to delete (p)
            if ((p.child[0] != null) && (p.child[1] != null))
            {
                // non-leaf node with two children being deleted
                // page 429 Tree deletion (is for a non-balanced binary tree)

                // In this case we find another node with 0 or 1 child which can be
                // deleted instead. We swap this node into the tree.

                // q - the node we would like to remove
                AVLNode q = p;
                adjust_p = p;
                adjust_direction = 1;

                // find p, a node we can actually remove
                p = p.child[1];
                while (p.child[0] != null)
                {
                    adjust_p = p;
                    adjust_direction = 0;
                    p = p.child[0];
                }

                // Now we found p, a node with zero or one child - easily removed:
                AVLNode p_child_1 = p.child[1];

                // move p's contents to q
                q.value = p.value;
                p = q;

                // fix up a connection to p's child (if p had a child)
                adjust_p.child[adjust_direction] = p_child_1;
                if (p_child_1 != null)
                {
                    p_child_1.parent = adjust_p;
                    p_child_1.direction = adjust_direction;
                }
                p.child[0].parent = p;
                p.child[0].direction = 0;
                if (p.child[1] != null)
                {
                    p.child[1].parent = p;
                    p.child[1].direction = 1;
                }
            }
            else if (p.child[0] != null)
            {
                // Node has one child - so it's easily removed:
                adjust_p.child[adjust_direction] = p.child[0];
                p.child[0].parent = adjust_p;
                p.child[0].direction = adjust_direction;
            }
            else
            {
                // Node has zero or one child - again easily removed.
                adjust_p.child[adjust_direction] = p.child[1];
                if (p.child[1] != null)
                {
                    p.child[1].parent = adjust_p;
                    p.child[1].direction = adjust_direction;
                }
            }

            // The process of deleting node p sets parent.p.child[parent.direction]
            // and so the balance factor at parent.p is adjusted
            while (adjust_p.parent != null)
            {
                int next_adjust_direction = adjust_p.direction;
                AVLNode next_adjust_p = adjust_p.parent;
                int adjust_a = adjust_direction == 1 ? 1 : -1;

                if (adjust_p.balance == adjust_a)
                {
                    // page 466 i: repeat adjustment procedure for parent
                    adjust_p.balance = 0;
                }
                else if (adjust_p.balance == 0)
                {
                    // page 466 ii: tree is balanced
                    adjust_p.balance = -adjust_a;
                    return true;
                }
                else
                {
                    // page 466 iii - rebalancing required
                    AVLNode s = adjust_p; // parent of subtree requiring rotation
                    AVLNode r = adjust_p.child[1 - adjust_direction]; // child requiring rotation is the OPPOSITE of the one removed

                    if (r.balance == -adjust_a)
                    {
                        // page 454 case 1
                        p = SingleRotation(r, s, 1 - adjust_direction);
                        next_adjust_p.child[next_adjust_direction] = p;
                        p.parent = next_adjust_p;
                        p.direction = next_adjust_direction;
                    }
                    else if (r.balance == adjust_a)
                    {
                        // page 454 case 2
                        p = DoubleRotation(r, s, 1 - adjust_direction);
                        next_adjust_p.child[next_adjust_direction] = p;
                        p.parent = next_adjust_p;
                        p.direction = next_adjust_direction;
                    }
                    else if (r.balance == 0)
                    {
                        // case 3: like case 1 except that beta has height h + 1 (same as gamma)
                        p = SingleRotation(r, s, 1 - adjust_direction);
                        next_adjust_p.child[next_adjust_direction] = p;
                        adjust_p.balance = -adjust_a;
                        p.balance = adjust_a;
                        p.parent = next_adjust_p;
                        p.direction = next_adjust_direction;
                        return true; // balanced after single rotation
                    }
                    else
                    {
                        throw new Exception("unexpected balance value");
                    }
                }
                adjust_direction = next_adjust_direction;
                adjust_p = next_adjust_p;

            }
            return true;
        }
    }

    // This test class is used to check that the AVL data structure is consistent
    class TestAVL2 : AVLIntegerSetParents
    {
        private int visit = 0;

        protected override AVLNode AVLNodeFactory()
        {
            return new TestAVLNode();
        }

        protected class TestAVLNode : AVLNode
        {
            public int visit = 0;
        }

        private int GetMaxDepth(AVLNode node)
        {
            int d1 = 0;
            int d2 = 0;
            if (node.child[0] != null)
            {
                d1 = 1 + GetMaxDepth(node.child[0]);
            }
            if (node.child[1] != null)
            {
                d2 = 1 + GetMaxDepth(node.child[1]);
            }
            if (d2 > d1)
            {
                d1 = d2;
            }
            return d1;
        }

        private int GetBalance(AVLNode node)
        {
            int d1 = 0;
            int d2 = 0;
            if (node.child[0] != null)
            {
                d1 = 1 + GetMaxDepth(node.child[0]);
            }
            if (node.child[1] != null)
            {
                d2 = 1 + GetMaxDepth(node.child[1]);
            }
            return d2 - d1;
        }

        private void CheckConsistentNode(TestAVLNode node, int visit)
        {
            if (node.visit == visit)
            {
                throw new Exception("cycle detected");
            }
            node.visit = visit;
            for (int i = 0; i <= 1; i++)
            {
                if (node.child[i] != null)
                {
                    CheckConsistentNode((TestAVLNode)node.child[i], visit);
                    if (node.child[i].parent != node)
                    {
                        throw new Exception("node.child.parent != node");
                    }
                    if (node.child[i].direction != i)
                    {
                        throw new Exception("node.child direction is incorrect");
                    }
                }
            }
            int x = GetBalance(node);
            if (!((-1 <= x) && (x <= 1)))
            {
                throw new Exception("node balance is out of permitted range");
            }
            if (x != node.balance)
            {
                throw new Exception("node balance is incorrect");
            }
        }

        public void CheckConsistent()
        {
            if (this.head.child[1] == null)
            {
                return;
            }
            if (this.head.child[1].parent != this.head)
            {
                throw new Exception("head child 1 should have parent head");
            }
            if (this.head.child[1].direction != 1)
            {
                throw new Exception("head child 1 should have direction 1");
            }
            visit++;
            this.CheckConsistentNode((TestAVLNode)this.head.child[1], visit);
        }

        private void CheckWithSetNode(AVLNode node, System.Collections.Generic.HashSet<int> s)
        {
            for (int i = 0; i <= 1; i++)
            {
                if (node.child[i] != null)
                {
                    CheckWithSetNode(node.child[i], s);
                }
            }
            if (s.Contains(node.value))
            {
                throw new Exception("value " + node.value + " appears twice");
            }
            s.Add(node.value);
        }

        public void CheckWithSet(System.Collections.Generic.HashSet<int> s)
        {
            if (head.child[1] == null)
            {
                if (s.Count != 0)
                {
                    throw new Exception("size of tree should be non-zero");
                }
                return;
            }
            System.Collections.Generic.HashSet<int> s2 = new System.Collections.Generic.HashSet<int>();
            CheckWithSetNode(head.child[1], s2);
            if (!s.SetEquals(s2))
            {
                throw new Exception("sets do not match");
            }
        }

        private int outcounter = 0;

        private int OutputNode(System.IO.StreamWriter sw, TestAVLNode node, int visit)
        {
            int src = this.outcounter;
            this.outcounter++;
            if (node.visit == visit)
            {
                return src;
            }
            node.visit = visit;
            sw.WriteLine("N" + src + " [label=\"" + node.value + " ; " + node.balance + "\"];");
            for (int i = 0; i < 2; i++)
            {
                if (node.child[i] != null)
                {
                    int dest = OutputNode(sw, (TestAVLNode)node.child[i], visit);
                    sw.WriteLine("N" + src + " -> N" + dest + " [label=\"" + i + "\"];");
                }
            }
            return src;
        }

        public void OutputTree(String filename)
        {
            using (System.IO.StreamWriter sw = System.IO.File.CreateText(filename))
            {
                sw.WriteLine("digraph G {");
                outcounter = 0;
                visit++;
                OutputNode(sw, (TestAVLNode)head, visit);
                sw.WriteLine("}");
            }
        }

        public static void Test()
        {
            TestAVL2 t = new TestAVL2();
            System.Collections.Generic.HashSet<int> s = new System.Collections.Generic.HashSet<int>();
            t.CheckConsistent();
            t.CheckWithSet(s);
            for (int i = 1; i <= 10; i++)
            {
                t.Insert(i);
                s.Add(i);
                t.CheckConsistent();
                t.CheckWithSet(s);
            }
            Random r = new Random(1);
            for (int i = 0; i < 1000; i++)
            {
                int v = r.Next(110);
                if (s.Contains(v))
                {
                    if (t.Insert(v) != true)
                    {
                        throw new Exception("should already contain");
                    }
                }
                else
                {
                    if (t.Insert(v) != false)
                    {
                        throw new Exception("should not contain");
                    }
                    s.Add(v);
                }
                t.CheckConsistent();
                t.CheckWithSet(s);
            }
            for (int i = 0; i < 1000; i++)
            {
                int v = r.Next(100);
                if (s.Contains(v))
                {
                    s.Remove(v);
                    if (t.Delete(v) != true)
                    {
                        throw new Exception("should remove");
                    }
                }
                else
                {
                    if (t.Delete(v) != false)
                    {
                        throw new Exception("should not remove");
                    }
                }
                t.CheckConsistent();
                t.CheckWithSet(s);
            }
            for (int i = 0; i < 10000; i++)
            {
                int v = r.Next(100);
                if (s.Contains(v))
                {
                    s.Remove(v);
                    if (t.Delete(v) != true)
                    {
                        throw new Exception("should remove");
                    }
                }
                else
                {
                    s.Add(v);
                    if (t.Insert(v) != false)
                    {
                        throw new Exception("should insert");
                    }
                }
                t.CheckConsistent();
                t.CheckWithSet(s);
            }
            for (int i = 0; i <= 110; i++)
            {
                if (s.Contains(i))
                {
                    s.Remove(i);
                    if (t.Delete(i) != true)
                    {
                        throw new Exception("should remove");
                    }
                }
                else
                {
                    if (t.Delete(i) != false)
                    {
                        throw new Exception("should not be present");
                    }
                }
                t.CheckConsistent();
                t.CheckWithSet(s);
            }
            t.OutputTree("test.dot");
        }
    }
}
