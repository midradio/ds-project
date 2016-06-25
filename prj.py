import sys
import copy
sys.setrecursionlimit(150000)
WHITE = 0
GRAY = 1
BLACK = 2

class User:
    def __init__(self):
        self.idn = 0
        self.sign_date=""
        self.name=""
        self.friend = []
        self.tweets = []
        self.followers = []
        self.num_friend = 0
        self.num_tweets = 0

    def set_user(self, idn, date, name):
        self.idn = idn
        self.sign_date = date
        self.name = name

    def add_friend(self, usr):
        self.friend.append(usr)
        usr.add_follower(self)
        self.num_friend = self.num_friend + 1

    def delete_friend(self, follower):
        friend = self.friend
        for i in range(len(friend)):
            if friend[i].name == follower.name:
                del friend[i]
                break
        self.num_friend -= 1

    def add_follower(self, usr):
        self.followers.append(usr)

    def delete_follower(self, friend):
        followers = self.followers
        for i in range(len(followers)):
            if followers[i].name == friend.name:
                del followers[i]
                break

    def add_tweet(self, word):
        self.tweets.append(word)
        self.num_tweets = self.num_tweets + 1

    def delete_tweet(self, word):
        tweets = self.tweets
        for i in range(len(tweets)):
            if tweets[i].string == word.string:
                del tweets[i]
                break
        self.num_tweets -= 1

class UserNode:
    def __init__(self):
        self.key = 0
        self.user = None
        self.left = None
        self.right = None
        self.parent = None
        self.n = 0

    def set_user(self, user):
        self.user = user
        self.key = self.user.idn

class UserAdj:
    def __init__(self):
        self.n = 0
        self.next = None

class UserVertex:
    def __init__(self):
        self.color = WHITE
        self.parent = -1
        self.key = 0
        self.name = ""
        self.n = 0
        self.first = None
        self.d = 0
        self.f = 0
        self.weight = 0

    def add(self, v):
        a = UserAdj()
        a.n = v.n
        a.next = self.first
        self.first = a

    def copy(self, other):
        self.color = other.color
        self.parent = other.parent
        self.key = other.key
        self.name = other.name
        self.n = other.n
        self.first = other.first
        self.d = other.d
        self.f = other.f
        self.weight = other.weight


class UserTree:
    def __init__(self):
        self.root = None
        self.max_friends = -1
        self.min_friends = 1E6
        self.max_tweets = -1
        self.min_tweets = 1E6
        self.i = 0

    def insert_node(self, node):
        y = None
        x = self.root
        while x is not None:
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right
        node.parent = y
        if y is None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node

    def search_tree(self, node, key):
        x = node
        while True:
            if x == None or key == x.key:
                return x
            if key < x.key:
                x = x.left
            else:
                x = x.right

    def user_traverse(self, node):
        if node.left != None:
            self.user_traverse(node.left)
        friends = node.user.num_friend
        tweets = node.user.num_tweets
        if friends > self.max_friends:
            self.max_friends = friends
        if friends < self.min_friends:
            self.min_friends = friends
        if tweets > self.max_tweets:
            self.max_tweets = tweets
        if tweets < self.min_tweets:
            self.min_tweets = tweets
        if node.right != None:
            self.user_traverse(node.right)

    def reset_i(self):
        self.i = 0

    def vertex_traverse(self, node):
        if node.left != None:
            self.vertex_traverse(node.left)
        node.n = self.i
        self.i += 1
        if node.right != None:
            self.vertex_traverse(node.right)

    def make_uservertex(self, node, vlist):
        if node.left != None:
            self.make_uservertex(node.left, vlist)
        n = node.n
        vlist[n].key = node.key
        vlist[n].name = node.user.name
        vlist[n].n = n
        friends = node.user.friend
        for f in friends:
            sf = self.search_tree(self.root, f.idn)
            fn = sf.n
            vlist[n].add(vlist[fn])
        followers = node.user.followers
        vlist[n].weight = len(followers)
        if node.right != None:
            self.make_uservertex(node.right, vlist)

    def tree_minimum(self, node):
        while node.left is not None:
            node = node.left
        return node

    def transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v is not None:
            v.parent = u.parent

    def delete_node(self, node):
        if node.left is None:
            self.transplant(node, node.right)
        elif node.right is None:
            self.transplant(node, node.left)
        else:
            y = self.tree_minimum(node.right)
            if y.parent != node:
                self.transplant(y, y.right)
                y.right = node.right
                y.right.parent = y
            self.transplant(node, y)
            y.left = node.left
            y.left.parent = y

    def statistics(self, users, friends, tweets):
        avg_friends = round(friends / users)
        avg_tweets = round(tweets / users)
        self.user_traverse(self.root)
        print("Average number of friends: " + str(avg_friends))
        print("Minimum friends: " + str(self.min_friends))
        print("Maximum number of friends: " + str(self.max_friends))
        print("")
        print("Average tweets per user: " + str(avg_tweets))
        print("Minimum tweets per user: " + str(self.min_tweets))
        print("Maximum tweets per user: " + str(self.max_tweets))

    def make_userlist(self, empty_list, node):
        if node.left != None:
            self.make_userlist(empty_list, node.left)
        empty_list.append(node)
        if node.right != None:
            self.make_userlist(empty_list, node.right)

    def user_merge(self, tmp, A, p, q, r):
        for i in range(p, r):
            tmp[i] = A[i]
        i = p
        j = q
        while i < q and j < r:
            if tmp[i].user.num_tweets > tmp[j].user.num_tweets:
                A[p] = tmp[i]
                i = i + 1
            else :
                A[p] = tmp[j]
                j = j + 1
            p = p + 1
        while i < q:
            A[p] = tmp[i]
            i = i + 1
            p = p + 1
        while j < r:
            A[p] = tmp[j]
            j = j + 1
            p = p + 1

    def user_mergesort(self, tmp, A, p, r):
        if p < r - 1:
            q = (p + r) // 2
            self.user_mergesort(tmp, A, p, q)
            self.user_mergesort(tmp, A, q, r)
            self.user_merge(tmp, A, p, q, r)

    def user_top5(self):
        userlist = []
        self.make_userlist(userlist, self.root)
        tmp = userlist[:]
        self.user_mergesort(tmp, userlist, 0, len(userlist))
        for i in range(5):
            print(str(i + 1) + ". " + userlist[i].user.name + "\tid: " + str(userlist[i].user.idn) + "\ttweets: " + str(userlist[i].user.num_tweets))

class Word:
    def __init__(self):
        self.string = ""
        self.tweet_date = ""
        self.user = None

    def set_word(self, string, date, usr):
        self.string = string
        self.tweet_date = date
        self.user = usr

class WordNode:
    def __init__(self):
        self.word = ""
        self.count = 0
        self.user_list = []
        self.user_set = []
        self.prev = None
        self.next = None

    def update_word(self, word, usr_wd):
        self.word = word
        self.count = self.count + 1
        self.user_list.append(usr_wd)

class WordHash:
    def __init__(self, init_num):
        self.hash_size = init_num
        self.hashtable = []
        for i in range(init_num):
            a = WordNode()
            self.hashtable.append(a)

    def hash(self, string):
        m = 0
        for c in string:
            m = m + ord(c)
        return m % (self.hash_size)

    def add_word(self, word, usr_wd):
        hash_num = self.hash(word)
        wn = self.hashtable[hash_num]
        if wn.word == word:
            wn.update_word(word, usr_wd)
        else:
            if wn.word == "":
                wn.update_word(word, usr_wd)
            else:
                nn = wn.next
                found = False
                while nn is not None:
                    if nn.word == word:
                        nn.update_word(word, usr_wd)
                        found = True
                    nn = nn.next
                if found is False:
                    a = WordNode()
                    a.update_word(word, usr_wd)
                    a.prev = None
                    a.next  = wn
                    wn.prev = a
                    self.hashtable[hash_num] = a

    def search_word(self, word):
        hash_num = self.hash(word)
        wn = self.hashtable[hash_num]
        if wn is None:
            print("Error: There is no such word!")
            sys.exit(-1)
        if wn.word == word:
            return wn
        else:
            nn = wn.next
            while nn is not None:
                if nn.word == word:
                    return nn
                nn = nn.next
            return None

    def delete_word(self, word):
        hn = self.hash(word)
        wn = self.search_word(word)
        if wn is None:
            print("Error: There is no such word!")
            sys.exit(-1)
        else:
            if wn.prev is not None:
                wn.prev.next = wn.next
            else:
                self.hashtable[hn] = wn.next
            if wn.next is not None:
                wn.next.prev = wn.prev
            elif wn.prev is None and wn.next is None:
                self.hashtable[hn] = WordNode()

    def make_wordlist(self):
        wordlist = []
        for i in range(self.hash_size):
            wn = self.hashtable[i]
            if wn.word != "":
                wordlist.append(wn)
                nn = wn.next
                while nn is not None:
                    wordlist.append(nn)
                    nn = nn.next
        return wordlist

    def word_merge(self, tmp, A, p, q, r):
        for i in range(p, r):
            tmp[i] = A[i]
        i = p
        j = q
        while i < q and j < r:
            if tmp[i].count > tmp[j].count:
                A[p] = tmp[i]
                i = i + 1
            else:
                A[p] = tmp[j]
                j = j + 1
            p = p + 1
        while i < q:
            A[p] = tmp[i]
            i = i + 1
            p = p + 1
        while j < r:
            A[p] = tmp[j]
            j = j + 1
            p = p + 1

    def word_mergesort(self, tmp, A, p, r):
        if p < r - 1:
            q = (p + r) // 2
            self.word_mergesort(tmp, A, p, q)
            self.word_mergesort(tmp, A, q, r)
            self.word_merge(tmp, A, p, q, r)

    def word_top5(self):
        wordlist = self.make_wordlist()
        tmp = wordlist[:]
        self.word_mergesort(tmp, wordlist, 0, len(wordlist))
        for i in range(5):
            print(str(i+1)+". " + wordlist[i].word + "\tcount: " + str(wordlist[i].count))

class DFS:
    def __init__(self):
        self.time = 0
        self.vertices = None
        self.scc_list = []
        self.scc_sorted_indices = None

    def set_vertices(self, vertices):
        self.vertices = vertices

    def dfs(self):
        for u in self.vertices:
            u.color = WHITE
            u.parent = -1
        self.time = 0
        for u in self.vertices:
            if u.color == WHITE:
                self.dfs_visit(u)

    def dfs_visit(self, u):
        self.time = self.time + 1
        u.d = self.time
        u.color = GRAY
        v = u.first
        while v:
            if self.vertices[v.n].color == WHITE:
                self.vertices[v.n].parent = u.n
                self.dfs_visit(self.vertices[v.n])
            v = v.next
        u.color = BLACK
        self.time = self.time + 1
        u.f = self.time

    def transpose(self):
        vertices1 = []
        for v in self.vertices:
            v1 = UserVertex()
            v1.copy(v)
            vertices1.append(v1)
        self.g_transpose(self.vertices, vertices1)
        self.set_vertices(vertices1)

    def g_transpose(self, vertices, vertices1):
        for i in range(len(vertices1)):
            vertices1[i].first = None
        for v in vertices:
            p = v.first
            while p:
                vertices1[p.n].add(v)
                p = p.next

    def scc(self):
        self.dfs()
        self.transpose()
        sorted = self.sort_by_f()
        vset = self.vertices
        for v in vset:
            v.color = WHITE
            v.parent = -1
        for n in sorted:
            if self.vertices[n].color == WHITE:
                self.scc_find(vset[n])

    def sort_by_f(self):
        vset = self.vertices
        sorted_indices = list(range(len(vset)))
        self.heapsort(sorted_indices)
        return sorted_indices

    def left(self, n):
        return 2 * n + 1

    def right(self, n):
        return 2 * n + 2

    def heapify(self, A, i, heapsize):
        vset = self.vertices
        l = self.left(i)
        r = self.right(i)
        if l < heapsize and vset[A[l]].f < vset[A[i]].f:
            largest = l
        else:
            largest = i
        if r < heapsize and vset[A[r]].f < vset[A[largest]].f:
            largest = r
        if largest != i:
            A[i], A[largest] = A[largest], A[i]
            self.heapify(A, largest, heapsize)

    def buildheap(self, A):
        for i in range(len(A) // 2 + 1, 0, -1):
            self.heapify(A, i - 1, len(A))

    def heapsort(self, A):
        self.buildheap(A)
        for i in range(len(A), 1, -1):
            A[i - 1], A[0] = A[0], A[i - 1]
            self.heapify(A, 0, i - 1)

    def scc_find(self, u):
        u.color = GRAY
        v = u.first
        found = False
        while v:
            if self.vertices[v.n].color == WHITE:
                found = True
                self.vertices[v.n].parent = u.n
                self.scc_find(self.vertices[v.n])
            v = v.next
        if not found:
            print("SCC:", end=" ")
            self.scc_print(u)
            print("")
        u.color = BLACK

    def scc_sort(self):
        vset = self.vertices
        print(len(self.scc_list))
        for node in self.scc_list:
            idx = 1
            p = node.parent
            while p >= 0:
                idx = idx + 1
                p = vset[p].parent
            node.f = idx
            print(idx)
        self.scc_sorted_indices = list(range(len(self.scc_list)))
        for i in range(5):
            print(str(i+1) + ".")
            print("\t", end='')
            idx = self.scc_sorted_indices[i]
            self.scc_print(self.scc_list[idx])
            print("")

    def scc_print(self, u):
        vset = self.vertices
        print(u.name + "(" + str(u.key) + ")", end=" ")
        if u.parent >= 0:
            self.scc_print(vset[u.parent])

class WordTweetSystem:
    def __init__(self):
        self.total_users = 0
        self.total_friends = 0
        self.total_tweets = 0
        
        self.avg_friends = 0
        self.min_friends = 0
        self.max_friends = 0

        self.avg_tweets = 0
        self.min_tweets = 0
        self.max_tweets = 0

        self.usertree = UserTree()
        self.wordhash = WordHash(1000)

        self.mentioned_word = None

    def main(self):
            while True:
                print("0. Read data files\n"+
                     "1. display statistics\n"+
                     "2. Top 5 most tweeted words\n"+
                     "3. Top 5 most tweeted users\n"+
                     "4. Find users who tweeted a word (e.g., ’연세대’)\n"+
                     "5. Find all people who are friends of the above users\n"+
                     "6. Delete all mentions of a word\n"+
                     "7. Delete all users who mentioned a word\n"+
                     "8. Find strongly connected components\n"+
                     "9. Find shortest path from a given user\n"+
                     "99. Quit\n"+
                     "Select Menu:")
                select = int(input())
                print("")
                if select == 0:
                    self.read_data()
                elif select == 1:
                    self.statistics()
                elif select == 2:
                    self.word_top5()
                elif select == 3:
                    self.user_top5()
                elif select == 4:
                    self.find_user()
                elif select == 5:
                    self.find_friend()
                elif select == 6:
                    self.delete_mention()
                elif select == 7:
                    self.delete_user()
                elif select == 8:
                    self.scc_top5()
                elif select == 99:
                    sys.exit()
                else:
                    print("Error:Unknown Command.")
                    print("")

    def read_data(self):
         # read user.txt
         user_txt = open("user.txt", 'r')
         user_lines = user_txt.readlines()
         user_lines_num = 0
         user_data_list = ["", "", ""]
         for line in user_lines:
             if user_lines_num == 0:
                 user_data_list[0] = line[0:-1]
                 user_lines_num = user_lines_num + 1
             elif user_lines_num == 1:
                 user_data_list[1] = line[0:-1]
                 user_lines_num = user_lines_num + 1
             elif user_lines_num == 2:
                 user_data_list[2] = line[0:-1]
                 user_lines_num = user_lines_num + 1
             elif user_lines_num == 3:
                 usr = User()
                 idn = int(user_data_list[0])
                 date = user_data_list[1]
                 name = user_data_list[2]
                 usr.set_user(idn, date, name)
                 un = UserNode()
                 un.set_user(usr)
                 self.usertree.insert_node(un)
                 self.total_users = self.total_users + 1
                 user_lines_num = 0
         user_txt.close()
         print("Total users: " + str(self.total_users))

         # read friend.txt
         friend_txt = open("friend.txt", 'r')
         friend_lines = friend_txt.readlines()
         friend_lines_num = 0
         now_user = -1
         up = None
         for line in friend_lines:
             if friend_lines_num == 0:
                 idn = int(line[0:-1])
                 if idn != now_user:
                     now_user = idn
                     up = self.usertree.search_tree(self.usertree.root, idn)
                 friend_lines_num = friend_lines_num + 1
             elif friend_lines_num == 1:
                 idn = int(line[0:-1])
                 friend = self.usertree.search_tree(self.usertree.root, idn)
                 up.user.add_friend(friend.user)
                 self.total_friends = self.total_friends + 1
                 friend_lines_num = friend_lines_num + 1
             elif friend_lines_num == 2:
                 friend_lines_num = 0
         friend_txt.close()
         print("Total friendship records: " + str(self.total_friends))

         #read word.txt
         word_txt = open("word.txt", 'r')
         word_lines = word_txt.readlines()
         word_lines_num = 0
         now_user = -1
         up = None
         word_data_list = ["", ""]
         for line in word_lines:
             if word_lines_num == 0:
                 idn = int(line[0:-1])
                 if idn != now_user:
                     now_user = idn
                     up = self.usertree.search_tree(self.usertree.root, idn)
                 word_lines_num = word_lines_num + 1
             elif word_lines_num == 1:
                 word_data_list[0] = line[0:-1]
                 word_lines_num = word_lines_num + 1
             elif word_lines_num == 2:
                 word_data_list[1] = line[0:-1]
                 word_lines_num = word_lines_num + 1
             elif word_lines_num == 3:
                 wd = Word()
                 wd.set_word(word_data_list[1], word_data_list[0], up.user)
                 up.user.add_tweet(wd)
                 self.wordhash.add_word(word_data_list[1], wd)
                 self.total_tweets = self.total_tweets + 1
                 word_lines_num = 0
         word_txt.close()
         print("Total tweets: " + str(self.total_tweets))
         print("")

    def statistics(self):
        self.usertree.statistics(self.total_users, self.total_friends, self.total_tweets)
        print("")

    def word_top5(self):
        self.wordhash.word_top5()
        print("")

    def user_top5(self):
        self.usertree.user_top5()
        print("")

    def find_user(self):
        print("Which word?")
        word = input()
        self.mentioned_word = self.wordhash.search_word(word)
        print("")
        mentioned_user = self.mentioned_word.user_list
        mentioned_set = self.mentioned_word.user_set
        for u in mentioned_user:
            if mentioned_set == []:
                mentioned_set.append(u)
            else:
                found = False
                for s in mentioned_set:
                    if s.user.name == u.user.name:
                        found = True
                if found == False:
                    mentioned_set.append(u)
            print("User: " + u.user.name + "(" + str(u.user.idn) + ") mentioned at " + u.tweet_date)
        print("")

    def find_friend(self):
        user_set = self.mentioned_word.user_set
        for u in user_set:
            friends = u.user.friend
            print("mentioned user: " + u.user.name + "(" + str(u.user.idn) + ")")
            print("\tfriends: ")
            for f in friends:
                print("\t-> " + f.name + "(" + str(f.idn) + ")")
            print("")
        print("")

    def delete_mention(self):
        mentioned_word = self.mentioned_word
        mentioned_user = self.mentioned_word.user_list
        self.wordhash.delete_word(mentioned_word.word)
        for u in mentioned_user:
            u.user.delete_tweet(u)
            self.total_tweets -= 1
            print("deleted mention of user: " + u.user.name + "(" + str(u.user.idn) + ")")
        mentioned_word = None
        print("*mentioned word deleted*")
        print("")

    def delete_user(self):
        mentioned_word = copy.deepcopy(self.mentioned_word)
        mentioned_user = copy.deepcopy(self.mentioned_word.user_set)
        for u in mentioned_user:
            followers = u.user.followers
            for f in followers:
                f.delete_friend(u.user)
            friends = u.user.friend
            for f in friends:
                f.delete_follower(u.user)
            self.total_friends -= 1
            mentions = u.user.tweets
            for m in mentions:
                word = m.string
                wn = self.wordhash.search_word(word)
                wn.count -= 1
                self.total_tweets -= 1
                if wn.count <= 0:
                    self.wordhash.delete_word(word)

        for u in mentioned_user:
            idn = u.user.idn
            un = self.usertree.search_tree(self.usertree.root, idn)
            if un is not None:
                print("User: " + un.user.name + "(" + str(un.user.idn) + ") deleted")
                self.usertree.delete_node(un)
                self.total_users -= 1
        print("*mentioned users deleted*")
        print("")

    def scc_top5(self):
        vlist = []
        ut = self.usertree
        ut.reset_i()
        ut.vertex_traverse(ut.root)
        for j in range(ut.i):
            uv = UserVertex()
            vlist.append(uv)
        ut.make_uservertex(ut.root, vlist)
        print(vlist[0].first.n)
        User_DFS = DFS()
        User_DFS.set_vertices(vlist)
        User_DFS.scc()
        #User_DFS.scc_sort()
        print("")


wt = WordTweetSystem()
wt.main()