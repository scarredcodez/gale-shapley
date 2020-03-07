#安定結婚問題

import random
import pandas

#男性クラスを定義
class Man:
    def __init__(self, number, girlfriend, favourite):
        self.number = number
        self.girlfriend = girlfriend
        self.favourite = favourite
    
    #女性リストをランダムに並び替えて選好リストを作成
    def make_preference(self):
        self.preference = random.sample(women, len(women))
    
    #選好順位取得メソッドの記述短縮
    def prefer(self, woman):
        return self.preference.index(woman)
    
    #選好順位で指定された女性に求婚
    def propose(self, rank):
        if rank < len(self.preference):
            proposee = self.preference[rank]
            if proposee.boyfriend == None:
                self.girlfriend = proposee
                proposee.boyfriend = self
            else:
                proposee.choose(self)

#女性クラスを定義
class Woman:
    def __init__(self, number, boyfriend):
        self.number = number
        self.boyfriend = boyfriend
    
    def prefer(self, man):
        return self.preference.index(man)
    
    def make_preference(self):
        self.preference = random.sample(men, len(men))
        
    #新たな求婚者と保留している男性の選好順位を比較して好きな方を選ぶ
    def choose(self, proposer):
        if self.prefer(proposer) < self.prefer(self.boyfriend):
            self.boyfriend.favourite += 1
            self.boyfriend.girlfriend = None
            self.boyfriend = proposer
            proposer.girlfriend = self
        else:
            proposer.favourite += 1
            
#b人の男性とg人の女性をマッチング
def match(b, g):
    #b人の男性、g人の女性インスタンスを生成してリストに格納
    global men
    men = [Man(i, None, 0) for i in range(b)]
    global women
    women = [Woman(i, None) for i in range(g)]
    
    #各インスタンスについて選好リスト作成メソッドを実行
    for man in men:
        man.make_preference()    
    for woman in women:
        woman.make_preference()
    
    #受入れ保留手続きの実行(全男性が、誰かに保留されるか全女性に拒否されるまで)
    stage = 0
    while next((man for man in men 
                if man.girlfriend == None and man.favourite < g), None):
        for man in men:
            if man.girlfriend == None:
                man.propose(man.favourite)
        stage += 1
    print("第" + str(stage) + "段階でマッチングが完了しました")

#安定性の確認
def check_stability():
    stable = True
    for man in men:
        for woman in man.preference:
            if man.girlfriend:
                if man.prefer(woman) < man.prefer(man.girlfriend):
                    if woman.prefer(man) < woman.prefer(woman.boyfriend):
                        stable = False
            else:
                if woman.prefer(man) < woman.prefer(woman.boyfriend):
                    stable = False
    if stable:
        print("このマッチングは安定的です")
    else:
        print("このマッチングは不安定です")

#選好リストの出力
def print_preferences():
    for man in men:
        print("男性[" + str(man.number) + "]の選好リスト: ", end="")
        for woman in man.preference:
            print("女性[" + str(woman.number) + "] ", end="")
        print("")
    for woman in women:
        print("女性[" + str(woman.number) + "]の選好リスト: ", end="")
        for man in woman.preference:
            print("男性[" + str(man.number) + "] ", end="")
        print("")

#マッチング結果の出力
def print_result():
    for man in men:
        if man.girlfriend:
            print("男性[" + str(man.number) + "]の妻: 女性[" 
                      + str(man.girlfriend.number) + "] (選好順位: " 
                + str(man.prefer(man.girlfriend) + 1) + "位)")
        else:
            print("男性[" + str(man.number) + "]: 独身")
    for woman in women:
        if woman.boyfriend:
            print("女性[" + str(woman.number) + "]の夫: 男性["
                      + str(woman.boyfriend.number) + "] (選好順位: " 
                + str(woman.prefer(woman.boyfriend) + 1) + "位)")
        else:
            print("女性[" + str(woman.number) + "]: 独身")

#マッチング結果をCSVファイルで保存する
def save_result(path):
    #表の列をリストで作成
    men_list = ["man[" + str(man.number) + "]" for man in men]
    wives = ["woman[" + str(man.girlfriend.number) + "]" 
                 if man.girlfriend else "single" for man in men]
    wives_ranks = [man.prefer(man.girlfriend) + 1 
                       if man.girlfriend else "-" for man in men]
    women_list = ["woman[" + str(woman.number) + "]" for woman in women]
    husbands = ["man[" + str(woman.boyfriend.number) + "]" 
                    if woman.boyfriend else "single" for woman in women]
    husbands_ranks = [woman.prefer(woman.boyfriend) + 1 
                         if woman.boyfriend else "-" for woman in women]
    
    #列の行数を揃える
    if len(men_list) < len(women_list):
        for i in range(len(women_list) - len(men_list)):
            men_list.append("")
            wives.append("")
            wives_ranks.append("")
    elif len(women_list) < len(men_list):
        for i in range(len(men_list) - len(women_list)):
            women_list.append("")
            husbands.append("")
            husbands_ranks.append("")
    
    #データフレームの作成
    df = pandas.DataFrame(
            {"man" : men_list,
             "wife" : wives,
             "wife's rank" : wives_ranks,
             "|" : ["|" for i in range(len(men_list))],
             "woman" : women_list,
             "husband" : husbands,
             "husband's rank" : husbands_ranks}, 
            columns=["man", "wife", "wife's rank", "|", 
                     "woman", "husband", "husband's rank"])
    
    #データフレームをCSV形式で書き出す
    df.to_csv(path, index=False)