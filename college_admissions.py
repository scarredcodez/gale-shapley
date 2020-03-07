#大学選考問題

import random
import pandas

#学生クラスを定義
class Student:
    def __init__(self, number, college, favourite):
        self.number = number
        self.college = college
        self.favourite = favourite
    
    #大学リストをランダムに並び替えてサイズが1以上大学数以下の選好リストを作成
    def make_preference(self):
        length = random.randint(1, len(colleges))
        self.preference = random.sample(colleges, length)
    
    #選好順位取得メソッドの記述短縮
    def prefer(self, college):
        return self.preference.index(college)
    
    #選好順位で指定された大学に応募
    def apply(self, rank):
        if rank < len(self.preference):
            college = self.preference[rank]
            if self in college.preference:
                if len(college.waitinglist) < college.quota:
                    self.college = college
                    college.waitinglist.append(self)
                    college.sort_waitinglist()
                else:
                    college.choose(self)
            else:
                self.favourite += 1

#大学クラスを定義
class College:
    def __init__(self, number, waitinglist, quota):
        self.number = number
        self.waitinglist = waitinglist
        self.quota = quota
    
    def prefer(self, student):
        return self.preference.index(student)
    
    #学生リストをランダムに並び替えてサイズが割当て人数以上学生数以下の選好リストを作成
    def make_preference(self):
        length = random.randint(self.quota, len(students))
        self.preference = random.sample(students, length)
    
    #新たな応募者と待機リスト学生のうち最下位の者の選好順位を比較して好きな方を選ぶ
    def choose(self, applicant):
        worst = self.waitinglist[-1]
        if self.prefer(applicant) < self.prefer(worst):
            worst.favourite += 1
            worst.college = None
            self.waitinglist.remove(worst)
            self.waitinglist.append(applicant)
            applicant.college = self
            self.sort_waitinglist()
        else:
            applicant.favourite += 1
    
    #待機リストを選好順に並べ替える
    def sort_waitinglist(self):
        self.waitinglist.sort(key=self.preference.index)

#n人の学生とm校の大学をマッチング
def match(n, m):   
    #n人の学生、m校の大学インスタンスを生成してリストに格納    
    global students
    students = [Student(i, None, 0) for i in range(n)]
    global colleges
    colleges = []
    for i in range(m):
        #割当て人数をランダムに決める
        q = random.randint(1, n)
        college = College(i, [], q)
        colleges.append(college)
    
    #各インスタンスについて選好リスト作成メソッドを実行
    for student in students:
        student.make_preference()
    for college in colleges:
        college.make_preference()
    
    #受入れ保留手続きの実行(全学生が大学の待機リストに入るか出願できる大学がなくなるまで)
    stage = 0
    while next((student for student in students 
                if student.college == None and student.favourite < len(student.preference)), None):
        for student in students:
            if student.college == None:
                student.apply(student.favourite)
        stage += 1
    print("第" + str(stage) + "段階でマッチングが完了しました")

#安定性の確認
def check_stability():
    stable = True
    for student in students:
        for college in student.preference:
            if student in college.preference:
                if college.prefer(student) < college.prefer(college.waitinglist[-1]):
                    if student.college:
                        if student.prefer(college) < student.prefer(student.college):
                            stable = False
                    else:
                        stable = False
    if stable:
        print("このマッチングは安定的です")
    else:
        print("このマッチングは不安定です")

#選好リストの出力
def print_preferences():
    for student in students:
        print("学生[" + str(student.number) + "]の選好リスト: ", end="")
        for college in student.preference:
            print("大学[" + str(college.number) + "] ", end="")
        print("")
    for college in colleges:
        print("大学[" + str(college.number) + "]の選好リスト: ", end="")
        for student in college.preference:
            print("学生[" + str(student.number) + "] ", end="")
        print("")

#マッチング結果の出力
def print_result():
    for student in students:
        if student.college:
            print("学生[" + str(student.number) + "]の大学: 大学[" 
                      + str(student.college.number) + "] (選好順位: " 
                + str(student.prefer(student.college) + 1) + "位)")
        else:
            print("学生[" + str(student.number) + "]: 浪人")
    for college in colleges:
        if college.waitinglist:
            print("大学[" + str(college.number) + "]の新入生: ", end="")
            for student in college.waitinglist:
                print("学生[" + str(student.number) + "]("
                          + str(college.prefer(student) + 1) + "位) ", end="")
            print("")
        else:
            print("大学[" + str(college.number) + "]:　新入生なし")

#マッチング結果をCSVファイルで保存する
def save_result(path):
    #表の列をリストで作成
    students_list = ["student[" + str(student.number) + "]" for student in students]
    students_colleges = ["college[" + str(student.college.number) + "]" 
                            if student.college else "no college" for student in students]
    colleges_ranks = [student.prefer(student.college) + 1 
                         if student.college else "-" for student in students]
    colleges_list = []
    newcomers = []
    newcomers_ranks = []
    for college in colleges:
        if college.waitinglist:
            for i in range(len(college.waitinglist)):
                colleges_list.append("college[" + str(college.number) + "](" 
                                 + str(len(college.waitinglist)) + "/" 
                                 + str(college.quota) + ")")
            for student in college.waitinglist:
                newcomers.append("student[" + str(student.number) + "]")
                newcomers_ranks.append(college.prefer(student) + 1)
        else:
            newcomers.append("no student")
            newcomers_ranks.append("-")
    for student in students:
        if student.college == None:
            colleges_list.append("rejectee")
            newcomers.append("student[" + str(student.number) + "]")
            newcomers_ranks.append("-")
    
    #列の行数を揃える
    if len(students_list) < len(colleges_list):
        for i in range(len(colleges_list) - len(students_list)):
            students_list.append("")
            students_colleges.append("")
            colleges_ranks.append("")
    
    #データフレームの作成
    df = pandas.DataFrame(
            {"student" : students_list,
             "student's college" : students_colleges,
             "college's rank" : colleges_ranks,
             "|" : ["|" for i in range(len(students_list))],
             "college(students/quota)" : colleges_list,
             "newcomers" : newcomers,
             "newcomer's rank" : newcomers_ranks}, 
            columns=["student", "student's college", 
                     "college's rank", "|", 
                     "college(students/quota)", 
                     "newcomers", "newcomer's rank"])
    
    #データフレームをCSV形式で書き出す
    df.to_csv(path, index=False)
