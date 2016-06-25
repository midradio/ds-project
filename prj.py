import sys
sys.setrecursionlimit(150000)

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

    def add_follower(self, usr):
        self.followers.append(usr)

    def add_tweet(self, word):
        self.tweets.append(word)
        self.num_tweets = self.num_tweets + 1

class UserNode:
    def __init__(self):
        self.key = 0
        self.user = None
        self.left = None
        self.right = None
        self.parent = None

    def set_user(self, user):
        self.user = user
        self.key = self.user.idn

class UserTree:
    def __init__(self):
        self.root = None
        self.max_friends = -1
        self.min_friends = 1E6
        self.max_tweets = -1
        self.min_tweets = 1E6

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
        self.user_idn = 0
        self.user_name = ""

    def set_word(self, string, date, idn, name):
        self.string = string
        self.tweet_date = date
        self.user_idn = idn
        self.user_name = name

class WordNode:
    def __init__(self):
        self.word = ""
        self.count = 0
        self.user_list = []
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
        if wn.word == word:
            return wn
        else:
            nn = wn.next
            while nn is not None:
                if nn.word == word:
                    return nn
                nn = nn.next
            return None

    def make_wordlist(self):
        wordlist = []
        for i in range(self.hash_size):
            wn = self.hashtable[i]
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
                 wd.set_word(word_data_list[1], word_data_list[0], now_user, up.user.name)
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
        for u in mentioned_user:
            print("User: " + u.user_name + "(" + str(u.user_idn) + ") mentioned at " + u.tweet_date)
        print("")

wt = WordTweetSystem()
wt.main()
