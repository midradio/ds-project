#자료구조 프로젝트 매뉴얼(manual)
=========================================================================================
## 필수사항
한글 Windows 시스템에 Python 버전 3이상이 설치되어 있어야 합니다. 
리눅스나 Mac OS X의 경우에는 정상적으로 작동하지 않을 수 있습니다.

##실행 전 준비 
본 repository에서 prj.py 파일을 다운로드 한 뒤 cp949로 인코딩 된 friend.txt, user.txt, word.txt 파일들과 같은 폴더에 저장합니다.

##실행 
저장한 폴더 안의 prj.py를 실행합니다. 인터페이스가 로딩되면 **반드시** 0번 메뉴를 선택해 데이터를 불러온 뒤 조작하십시오.

##주의사항
1. 1번 메뉴(display statistics)의 경우 '평균 친구 수', '평균 트윗 수'는 반올림한 값입니다.

2. 5번, 6번, 7번 메뉴를 실행하기 전에는 **반드시** 4번 메뉴를 실행하여 탐색할 word를 저장해야 합니다.

3. 6번, 7번의 delete 메뉴를 실행하면 저장된 word가 초기화 됩니다. 추가적인 삭제가 필요하다면, 4번 메뉴를 다시 실행해주세요.

4. 8번, 9번 메뉴는 현재 작업중입니다. 정말 죄송합니다.

## 문제해결
간혹 큰 파일 데이터를 사용할 시 "maximum recursion depth exceeded"에러가 발생 할 수 있습니다.
prj.py 파일을 열어 3번째 라인의 `sys.setrecursionlimit(150000)` 의 150000을 더 큰 값으로 바꾸어주세요.

#자료구조 프로젝트 리포트(report)
===================================================================================
## What data structure you chose and why?
* 이 프로젝트에서 중요한 데이터는 user, friendship relation, word입니다. 이때, user와 word 데이터는 friendship 데이터보다 한번에 저장되는 양이 많고, 프로그램 명령의 대부분이 user와 word 데이터를 빠르게 찾고, 추가하며, 제거하는 일을 요구하고 있습니다. 따라서 저는 user 데이터의 경우에는 평균적으로 탐색에 O(nlogn)이 소모되는 binary search tree로, word 데이터의 경우는 이상적인 경우에는 O(1)이 소모되는 hash table을 이용하 빠르게 탐색하고 수정 가능하게 하였고, 상대적으로 수정 빈도가 적고, 한번에 탐색하는 데이터 양이 적은 friendship data의 경우는 python의 내장 list를 통해 저장하였습니다. 

* 세부적으로 들어가면, 각 유저의 id, name, sign date같은 기본적인 정보와 mention list, friend list, 그리고 7번 명령을 실행하고 난 뒤, friend list 관리를 더욱 쉽게 하기 위해 나를 follow하는 사람, 즉 나를 friend list에 넣은 user들을 저장하는 리스트인 follower list까지 이 프로그램에서 유저 하나하나에게 중요한 정보는 user 클래스에 저장됩니다. 위에 언급된 정보들을 수정하는 함수도 모두 user 클래스에 구현하였습니다. 그 다음 user 클래스를 binary search tree에 저장하기 위해 usernode라는 클래스로 둘러쌌고, usernode class는 usertree 클래스에서 bst를 형성합니다. word 데이터의 경우는 각 멘션 하나하나는 word 클래스에 저장되고, wordnode 클래스에서는 같은 string을 가진 mention 들을 user_list에 넣어 관리합니다. wordnode 클래스는 해쉬 테이블을 의미하는 wordhash 클래스의 hashtable 리스트에 저장됩니다. 이때, wordnode의 삽입과 삭제를 효율적으로 하기 위해, wordnode를 doubly linked list로 구현하였습니다.

* 그런데 2번 혹은 3번 명령의 경우는 해쉬나 트리 형태로 구성되어 있는 데이터 구조를 특정 데이터 필드를 기준으로 정렬하는 것을 요구합니다. 따라서 저는 이를 구현하기 위해 usertree의 각 usernode와 wordhash의 각 wordnode를 모두 순회하여 두 개의 리스트를 만들었고, 각 리스트에 대해 트윗 갯수나 단어 빈도를 기준으로 정렬하는 mergesort함수를 구현하여 리스트를 정렬한 뒤, 앞에서부터 5개의 원소를 추출하는 것으로 해결하였습니다. 구현을 완성하지는 못했지만, 8번 명령의 경우에도 heapsort를 이용해 ssc를 찾고, 추가적인 heapsort를 구현하여 ssc의 크기를 기준으로 정렬해 문제를 해결하는 것을 시도해 보았습니다.

## What is your expected performance?
* 0번 명령에서 user파일을 읽고 data structure를 형성하는 것은 O(n)으로, friend파일을 읽을 때에는 O(nlogn), word파일은 O(n)에 가까운 시간 복잡도를 가질 것 같습니다.

* 1번 명령의 경우는 모든 usernode를 방문해야 하므로 O(n)이 걸릴 것 같습니다.

* 2,3번 명령은 user, word 데이터에 대해 리스트를 형성하고, 이를 merge sort로 정렬해야 하므로, 각각 O(nlogn)의 시간 복잡도를 예상합니다.

* 4번의 경우 hash탐색:O(1) + usertree탐색:O(logn) * mention list 탐색:O(n) 이어서 O(nlogn)을 예상하고 있습니다.

* 5번의 경우, 유저의 친구까지 함께 탐색해야 하므로 O(n^2logn)이 될 것 같습니다.

* 6번의 경우 O(n) ~ O(nlogn) 사이의 성능을 기대 중입니다.

* 7번의 경우 O(n) * O(logn) * + O(n) or O(logn)이어서 O(nlogn)에서 살짝 더 계산복잡도가 높을 것 같습니다.

## How would you improve the system in the future?
* 일단 현재 구현하지 못한 두 기능을 먼저 구현해보고 싶습니다. SCC에 대한 이해도가 부족해서 구현하지 못한 것 같은데 좀 더 공부한다면 구현할 수 있을 것 같습니다.

* 또한 위에서는 usertree의 성능이 O(nlogn)이라고 적었지만, RB tree가 아니고서는 이 성능을 보장할 수 없습니다. 시간이 더 있다면 RB tree를 확실하게 구현해보고 싶습니다.

* 그리고 코드를 작성하면서 제 자신이 깨끗하고 깔끔하지 못한 코드를 작성하고 있다는 사실을 너무 크게 느꼈습니다. 마감시간에 쫒기면서 프로그램을 작성하였고, 그 코드의 품질이 좋지 못해서 제 자신에게 너무 부끄러웠습니다. 만약 시간이 조금 더 주어진다면, 더 깔끔하고 정확한 코드를 작성해 보고 싶습니다.

#자료구조 자기평가(self-evaluation)
========================================================================
* Submit a github account (10): 8
* Commit source code displaying menu (10) : 9
* Commit the first draft of manual (10) : 9
* Read data files (20) : 17
* Statistics (20) : 18
* Top 5 most tweeted words (10) : 8
* Top 5 most tweeted users (5) : 5
* Find all users who mentioned a word (10) : 6
* Find all users who are friend of the above user (5) : 3
* Top 5 strongly connected components (10) : 3 
* Find shortest path from a user (id) (10) : 0

