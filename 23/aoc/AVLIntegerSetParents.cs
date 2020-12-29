using System;

// This Adelson-Velsky and Landis (AVL) tree implementation is based on AVLIntegerSet.cs
// but uses child->parent links instead of a temporary stack.
// See https://en.wikipedia.org/wiki/AVL_tree for an introduction to AVL trees.
// In this implementation:
// * the AVL tree acts as an ordered set of integers, with O(log N) insertion and removal
// * there is a "parent" reference at each node
// * children are numbered 0 and 1, so that rotation procedures can be generic
// * Insert and Delete operations are not recursive
// * a "head" node is always present so that the "empty" set is not a special case

namespace aoc
{

    public class AVLIntegerList
    {
        protected AVLNode head;

        public AVLIntegerList()
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

            public int a()
            {
                return (direction == 0) ? -1 : 1;
            }

            public void AssertChildIs(AVLNode c)
            {
                if ((this.child[0] != c) && (this.child[1] != c))
                {
                    throw new Exception("not a child");
                }
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
                    p.AssertChildIs(q);
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
                p.parent.AssertChildIs(p);
            }
            else
            {
                t.child[0] = p;
                p.parent = t;
                p.direction = 0;
                p.parent.AssertChildIs(p);
            }
            return false;
        }

        private AVLNode SingleRotation(AVLNode r, AVLNode s, int direction)
        {
            // page 457 A8 single rotation
            // as applied to case 1 (top of page 454) in which s is A and r is B
            // initially B is a child of A (i.e. r is a child of s)
            // In the book, direction = 1

            AVLNode p = r;
            s.child[direction] = r.child[1 - direction];   // beta subtree moved from B to A
            r.child[1 - direction] = s;                    // node A becomes child of B
            s.balance = 0;
            r.balance = 0;
            r.AssertChildIs(s);
            //r.parent = s.parent;
            //r.direction = s.direction;
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
            // as applied to case 2 (top of page 454) in which s is A and r is B
            // initially B is a child of A (i.e. r is a child of s)
            // In the book, direction = 1

            int a = (direction > 0) ? 1 : -1;
            AVLNode p;

            p = r.child[1 - direction];                     // p is node X
            r.child[1 - direction] = p.child[direction];    // gamma subtree moved from X to B
            p.child[direction] = r;                         // B becomes child of X
            s.child[direction] = p.child[1 - direction];    // beta subtree moved from X to A
            p.child[1 - direction] = s;                     // A becomes child of X
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

        // The auxiliary stack is only used for deletion
        private class AuxStack
        {
            public AVLNode p = null;
            public int direction = 0;  // 0 = left, 1 = right
            public int a = -1;         // -1 = left, 1 = right

            public AuxStack(AVLNode p, int a)
            {
                this.direction = (a < 0) ? 0 : 1;
                this.a = a;
                this.p = p;
            }
        }

        // Delete returns true if removed and false if not present
        public bool Delete(int k)
        {
            System.Collections.Generic.Stack<AuxStack> stack = new System.Collections.Generic.Stack<AuxStack>();
            AVLNode p = head;

            stack.Push(new AuxStack(head, 1));
            p = p.child[1];

            while (true)
            {
                if (p == null)
                {
                    // not found
                    return false;
                }
                else if (k < p.value)
                {
                    stack.Push(new AuxStack(p, -1));
                    p = p.child[0];
                }
                else if (k > p.value)
                {
                    stack.Push(new AuxStack(p, 1));
                    p = p.child[1];
                }
                else
                {
                    // found
                    break;
                }
            }

            // found the node to delete (p)
            AuxStack parent = stack.Peek();
            if ((p.child[0] != null) && (p.child[1] != null))
            {
                // non-leaf node with two children being deleted
                // page 429 Tree deletion (is for a non-balanced binary tree)

                // In this case we find another node with 0 or 1 child which can be
                // deleted instead. We swap this node into the tree.

                // q - the node we would like to remove
                AVLNode q = p;
                AuxStack q_parent = parent;
                AuxStack q_item = new AuxStack(p, 1);
                stack.Push(q_item);

                // find p, a node we can actually remove
                p = p.child[1];
                while (p.child[0] != null)
                {
                    stack.Push(new AuxStack(p, -1));
                    p = p.child[0];
                }

                // Now we found p, a node with zero or one child - easily removed:
                AVLNode p_child_1 = p.child[1];

                // swap "p" and "q" within the tree structure
                // so that "q" moves out of the tree and can be deleted
                // and "p" takes its place
                q_parent.p.child[q_parent.direction] = p;
                p.child[0] = q.child[0];
                p.child[1] = q.child[1];
                p.parent = q.parent;
                p.balance = q.balance;
                q_item.p = p;

                // fix up a connection to p's child (if p had a child)
                parent = stack.Peek();
                parent.p.child[parent.direction] = p_child_1;
                if (p_child_1 != null)
                {
                    p_child_1.parent = parent.p;
                }
                p.child[0].parent = p;
                if (p.child[1] != null)
                {
                    p.child[1].parent = p;
                }
            }
            else if (p.child[0] != null)
            {
                // Node has one child - so it's easily removed:
                parent.p.child[parent.direction] = p.child[0];
                p.child[0].parent = parent.p;
            }
            else
            {
                // Node has zero or one child - again easily removed.
                parent.p.child[parent.direction] = p.child[1];
                if (p.child[1] != null)
                {
                    p.child[1].parent = parent.p;
                }
            }

            // The process of deleting node p sets parent.p.child[parent.direction]
            // and so the balance factor at parent.p is adjusted
            while (stack.Count > 1)
            {
                AuxStack adjust = stack.Pop();
                if (adjust.p.balance == adjust.a)
                {
                    // page 466 i: repeat adjustment procedure for parent
                    adjust.p.balance = 0;
                }
                else if (adjust.p.balance == 0)
                {
                    // page 466 ii: tree is balanced
                    adjust.p.balance = -adjust.a;
                    return true;
                }
                else
                {
                    // page 466 iii - rebalancing required
                    AVLNode s = adjust.p; // parent of subtree requiring rotation
                    AVLNode r = adjust.p.child[1 - adjust.direction]; // child requiring rotation is the OPPOSITE of the one removed
                    parent = stack.Peek();

                    if (r.balance == -adjust.a)
                    {
                        // page 454 case 1
                        p = SingleRotation(r, s, 1 - adjust.direction);
                        parent.p.child[parent.direction] = p;                     
                        p.parent = parent.p;
                        p.direction = parent.direction;
                    }
                    else if (r.balance == adjust.a)
                    {
                        // page 454 case 2
                        p = DoubleRotation(r, s, 1 - adjust.direction);
                        parent.p.child[parent.direction] = p;
                        p.parent = parent.p;
                        p.direction = parent.direction;
                    }
                    else if (r.balance == 0)
                    {
                        // case 3: like case 1 except that beta has height h + 1 (same as gamma)
                        p = SingleRotation(r, s, 1 - adjust.direction);
                        parent.p.child[parent.direction] = p;
                        adjust.p.balance = -adjust.a;
                        p.balance = adjust.a;
                        p.parent = parent.p;
                        p.direction = parent.direction;
                        return true; // balanced after single rotation
                    }
                    else
                    {
                        throw new Exception("unexpected balance value");
                    }
                }

            }
            return true;
        }
    }

    // This test class is used to check that the AVL data structure is consistent
    class TestAVL2 : AVLIntegerList
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

        private bool IsConsistentNode(TestAVLNode node, int visit)
        {
            if (node.visit == visit)
            {
                return false; // cycle detected
            }
            node.visit = visit;
            for (int i = 0; i <= 1; i++)
            {
                if (node.child[i] != null)
                {
                    if (!IsConsistentNode((TestAVLNode)node.child[i], visit))
                    {
                        return false;
                    }
                    if (node.child[i].parent != node)
                    {
                        return false;
                    }
                    if (node.child[i].direction != i)
                    {
                        return false;
                    }
                }
            }
            int x = GetBalance(node);
            if (!((-1 <= x) && (x <= 1)))
            {
                return false;
            }
            if (x != node.balance)
            {
                return false;
            }
            return true;
        }

        public bool IsConsistent()
        {
            if (this.head.child[1] == null)
            {
                return true;
            }
            if (this.head.child[1].parent != this.head)
            {
                return false;
            }
            if (this.head.child[1].direction != 1)
            {
                return false;
            }
            visit++;
            return this.IsConsistentNode((TestAVLNode)this.head.child[1], visit);
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
                    sw.WriteLine("N" + src + " -> N" + dest + ";");
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

            for (int i = 1; i <= 10; i++)
            {
                t.Insert(i);
                s.Add(i);
                if (!t.IsConsistent())
                {
                    throw new Exception("became imbalanced");
                }
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
                }
                if (!t.IsConsistent())
                {
                    throw new Exception("became imbalanced");
                }
                s.Add(v);
            }
            t.OutputTree("test.dot");
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
                if (!t.IsConsistent())
                {
                    throw new Exception("became imbalanced");
                }
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
                if (!t.IsConsistent())
                {
                    throw new Exception("became imbalanced");
                }
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
                if (!t.IsConsistent())
                {
                    throw new Exception("became imbalanced");
                }
            }
            t.OutputTree("test.dot");
        }
    }
}
