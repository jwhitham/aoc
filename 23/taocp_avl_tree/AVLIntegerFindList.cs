using System;

// This Adelson-Velsky and Landis (AVL) tree implementation is based on AVLIntegerList.cs
// and it implements a list of integers in which any element can be inserted, deleted or
// accessed in O(log N) time, based on its index.
//
// Provided that element values are unique, you can find an element's index from
// its value in O(log N) time too, as there is also a dictionary linking values to tree nodes.

namespace taocp_avl_tree
{

    public class AVLIntegerFindList
    {
        protected AVLNode head;
        protected System.Collections.Generic.Dictionary<int, AVLNode> first;

        public AVLIntegerFindList()
        {
            this.head = AVLNodeFactory();
            this.first = new System.Collections.Generic.Dictionary<int, AVLNode>();
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
            public int rank = 0;
            public AVLNode parent = null;

            public AVLNode()
            {
                this.child = new AVLNode[2];
            }

            public int left_rank()
            {
                if (this.child[0] == null)
                {
                    return 0;
                } else
                {
                    return this.child[0].rank;
                }
            }
        }

        public int Index(int value)
        {
            AVLNode p = null;
            if (!this.first.TryGetValue(value, out p))
            {
                return -1; // This value does not exist
            }
            if (p.value != value)
            {
                throw new Exception("value is unexpected");
            }
            int index = p.left_rank();
            AVLNode end = head.child[1];
            while (p != end) {
                if (p.direction == 1)
                {
                    p = p.parent;
                    index += p.left_rank() + 1;
                } else
                {
                    p = p.parent;
                }
            }
            return index;
        }

        public int Value(int index)
        {
            AVLNode p = head.child[1];

            while (true)
            {
                if (p == null)
                {
                    return -1; // index does not exist
                }
                else if (index < p.left_rank())
                {
                    p = p.child[0];
                }
                else if (index == p.left_rank())
                {
                    return p.value;  // index found
                }
                else
                {
                    index -= p.left_rank() + 1;
                    p = p.child[1];
                }
            }
        }

        public void Insert(int index, int value)
        {
            AVLNode p = head.child[1];  // the pointer variable p will move down the tree
            AVLNode s = head.child[1];  // s will point to the place where rebalancing may be necessary
            AVLNode t = head;           // t will always point to the parent of s
            AVLNode q, r;
            int direction;
            int s_index = index; // index at the point where rebalancing was necessary

            if (p == null)
            {
                // empty tree special case
                head.child[1] = AVLNodeFactory();
                head.child[1].value = value;
                head.child[1].parent = head;
                head.child[1].direction = 1;
                head.child[1].rank = 1;
                first[value] = head.child[1];
                return;
            }

            while (true)
            {
                if (index <= p.left_rank())
                {
                    // move left
                    direction = 0;
                }
                else
                {
                    // move right
                    direction = 1;
                    index -= p.left_rank() + 1;
                }

                // inserting something below p - therefore, rank of p increases
                p.rank++;

                q = p.child[direction];
                if (q != null)
                {
                    // Continue search
                    if (q.balance != 0)
                    {
                        t = p;
                        s = q;
                        s_index = index;
                    }
                    p = q;
                }
                else
                {
                    // New child (appending)
                    q = AVLNodeFactory();
                    p.child[direction] = q;
                    q.parent = p;
                    q.direction = direction;
                    q.rank = 1;
                    first[value] = q;
                    break;
                }
            }

            q.value = value;
            q.balance = 0;
            // adjust balance factors
            index = s_index;
            if (index <= s.left_rank())
            {
                r = p = s.child[0];
            }
            else
            {
                index -= s.left_rank() + 1;
                r = p = s.child[1];
            }
            while (p != q)
            {
                if (index <= p.left_rank())
                {
                    p.balance = -1;
                    p = p.child[0];
                }
                else
                {
                    index -= p.left_rank() + 1;
                    p.balance = 1;
                    p = p.child[1];
                }
            }
            // A7 balancing act
            int a;
            if (s_index <= s.left_rank())
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
                return;
            }
            else if (s.balance == -a)
            {
                // case ii. The tree has gotten more balanced
                s.balance = 0;
                return;
            }
            // case iii. The tree is not balanced
            // note: r = s.child[direction]
            if (r.balance == a)
            {
                // page 454 case 1
                p = SingleRotation(r, s, direction);
                Rerank(s);
                Rerank(r);
                Rerank(p);
            }
            else if (r.balance == -a)
            {
                // page 454 case 2
                p = DoubleRotation(r, s, direction);
                Rerank(s);
                Rerank(r);
                Rerank(p);
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
            r.child[1 - direction] = s;                    // node r becomes child of s
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

        private void Rerank(AVLNode node)
        {
            node.rank = 1;
            for (int i = 0; i <= 1; i++)
            {
                if (node.child[i] != null)
                {
                    node.rank += node.child[i].rank;
                }
            }            
        }

        public void Delete(int index)
        {
            AVLNode p = head.child[1];
            AVLNode adjust_p = head;
            int adjust_direction = 1;

            if ((p == null) || (index < 0) || (index >= p.rank))
            {
                // unable to delete element outside of list
                return;
            }

            while (true)
            {
                if (p == null)
                {
                    // this should not be possible due to the index check at the start of the Delete method
                    throw new Exception("missing index");
                }

                // element will be removed below p
                p.rank--;
                if (index < p.left_rank())
                {
                    adjust_p = p;
                    adjust_direction = 0;
                    p = p.child[0];
                }
                else if (index > p.left_rank())
                {
                    adjust_p = p;
                    adjust_direction = 1;
                    index -= p.left_rank() + 1;
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
                    p.rank--;
                    adjust_p = p;
                    adjust_direction = 0;
                    p = p.child[0];
                }
                p.rank--;

                // Now we found p, a node with zero or one child - easily removed:
                AVLNode p_child_1 = p.child[1];

                // move p's contents to q
                first.Remove(q.value);
                first[p.value] = q;
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
                first.Remove(p.value);
                adjust_p.child[adjust_direction] = p.child[0];
                p.child[0].parent = adjust_p;
                p.child[0].direction = adjust_direction;
            }
            else
            {
                // Node has zero or one child - again easily removed.
                first.Remove(p.value);
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
                    return;
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
                        Rerank(s);
                        Rerank(r);
                        Rerank(p);
                    }
                    else if (r.balance == adjust_a)
                    {
                        // page 454 case 2
                        p = DoubleRotation(r, s, 1 - adjust_direction);
                        next_adjust_p.child[next_adjust_direction] = p;
                        p.parent = next_adjust_p;
                        p.direction = next_adjust_direction;
                        Rerank(s);
                        Rerank(r);
                        Rerank(p);
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
                        Rerank(s);
                        Rerank(r);
                        Rerank(p);
                        return; // balanced after single rotation
                    }
                    else
                    {
                        throw new Exception("unexpected balance value");
                    }
                }
                adjust_direction = next_adjust_direction;
                adjust_p = next_adjust_p;

            }
        }
    }
    // This test class is used to check that the AVL data structure is consistent
    class TestAVL4 : AVLIntegerFindList
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

        private int GetRank(AVLNode node)
        {
            int rank = 1;
            for (int i = 0; i <= 1; i++)
            {
                if (node.child[i] != null)
                {
                    rank += GetRank(node.child[i]);
                }
            }
            return rank;
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
            int r = GetRank(node);
            if (node.rank != r)
            {
                throw new Exception("node rank is incorrect");
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

        private void CheckWithListNode(AVLNode node, System.Collections.Generic.List<int> s)
        {
            int size = 0;
            if (node.child[0] != null)
            {
                size += node.child[0].rank;
                CheckWithListNode(node.child[0], s.GetRange(0, size));
            }
            if (s[size] != node.value)
            {
                throw new Exception("value should be " + s[size] + " actually is " + node.value);
            }
            AVLNode node2 = null;
            if (!first.TryGetValue(node.value, out node2))
            {
                throw new Exception("first does not have an entry for " + node.value);
            }
            if (node2 != node)
            {
                throw new Exception("first has the wrong entry for " + node.value + ": should always be correct "
                                    + "if values are unique");
            }
            size++;
            if (node.child[1] != null)
            {
                CheckWithListNode(node.child[1], s.GetRange(size, s.Count - size));
                size += node.child[1].rank;
            }
            if (size != s.Count)
            {
                throw new Exception("size of subtree should be " + s.Count + " actually is " + s.Count);
            }
        }

        public void CheckWithList(System.Collections.Generic.List<int> s)
        {
            if (head.child[1] == null)
            {
                if (s.Count != 0)
                {
                    throw new Exception("size of tree should be non-zero");
                }
                return;
            }
            if (head.child[1].rank != first.Count)
            {
                throw new Exception("size of 'first' hash should match size of tree if values are unique");
            }
            CheckWithListNode(head.child[1], s);
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
            TestAVL4 t = new TestAVL4();
            System.Collections.Generic.List<int> s = new System.Collections.Generic.List<int>();
            t.CheckConsistent();
            t.CheckWithList(s);

            Random r = new Random(1);
            for (int k = 1; k <= 1000; k++)
            {
                int i = r.Next(s.Count + 1);
                t.Insert(i, k);
                s.Insert(i, k);
                t.CheckConsistent();
                t.CheckWithList(s);
                if (t.Value(s.Count) != -1)
                {
                    throw new Exception("end of list should be -1");
                }
                if (t.Value(-1) != -1)
                {
                    throw new Exception("before start of list should be -1");
                }
            }
            for (int k = 1; k <= 1000; k++)
            {
                int j = t.Index(k);
                if ((j < 0) || (s[j] != k) || (t.Value(j) != k))
                {
                    throw new Exception("index for value is wrong");
                }
            }
            for (int k = 1; k <= 1000; k++)
            {
                int i = r.Next(s.Count);
                t.Delete(i);
                s.RemoveAt(i);
                t.CheckConsistent();
                t.CheckWithList(s);
            }
            for (int k = 0; k < 10000; k++)
            {
                if ((r.Next(2) == 0) && (s.Count > 0))
                {
                    int i = r.Next(s.Count);
                    int v = s[i];

                    if (t.Index(v) != i)
                    {
                        throw new Exception("index for value is wrong");
                    }
                    s.RemoveAt(i);
                    t.Delete(i);
                }
                else
                {
                    int i = r.Next(s.Count + 1);
                    s.Insert(i, k);
                    t.Insert(i, k);
                    int j = t.Index(k);
                    if (j != i)
                    {
                        throw new Exception("index for value is wrong: got " + j + " should be " + i);
                    }
                }
                t.CheckConsistent();
                t.CheckWithList(s);
            }
            t.OutputTree("test.dot");
            while (s.Count > 0)
            {
                s.RemoveAt(0);
                t.Delete(0);
                t.CheckConsistent();
                t.CheckWithList(s);
            }
        }
    }

}
