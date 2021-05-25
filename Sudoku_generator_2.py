import tkinter as tk
import copy
import random

"""2021/05/05 retest"""
"""method refer to https://gamedev.stackexchange.com/questions/56149/how-can-i-generate-sudoku-puzzles"""
"""this is a copy and modify based on Sudoku_generator.py"""

window = tk.Tk()
window.title("October's Sudoku generator  (V_20210227)")
window.geometry('470x400')
window.configure(background='SkyBlue1')



class Sudoku_generator():
    def init(self, tk):
        self.zip_element = []
        self.test_counter = 0
        self.element = []
        # every element is a dict
        for i in range(9):
            temp_element = []
            for j in range(9):
                norm = {
                    "row": i,
                    "row_group": self.find_row_group(i),
                    "col": j,
                    "col_group": self.find_col_group(j),
                    "block": self.find_blk(i, j),
                    "find": 0,
                    "candidate": [1, 2, 3, 4, 5, 6, 7, 8, 9]
                    # "zip" : 0
                }
                temp_element.append(norm)
            self.element.append(temp_element)
        #  assign the color to every element_entry
        self.element_entry = []
        for i in range(9):
            temp_list = []
            for j in range(9):
                temp = tk.Entry(width=3, bg=self.find_color(i, j))
                temp.grid(row=i + 1, column=j)
                temp_list.append(temp)
            self.element_entry.append(temp_list)

    def check_validity(self):
        for r in range(9):
            candi = list(range(1, 10))
            temp = set()
            for i in range(9):
                if self.element[r][i]["find"] != 0:
                    candi.remove(self.element[r][i]["find"])
                else:
                    temp |= set(self.element[r][i]["candidate"])
            if temp != set(candi):
                return False

        for c in range(9):
            candi = list(range(1, 10))
            temp = set()
            for i in range(9):
                if self.element[i][c]["find"] != 0:
                    candi.remove(self.element[i][c]["find"])
                else:
                    temp |= set(self.element[i][c]["candidate"])
            if temp != set(candi):
                return False

        for b in range(9):
            candi = list(range(1, 10))
            temp = set()
            for r in range(9):
                for c in range(9):
                    if self.element[r][c]["block"] == b:
                        if self.element[r][c]["find"] != 0:
                            candi.remove(self.element[r][c]["find"])
                        else:
                            temp |= set(self.element[r][c]["candidate"])
            if temp != set(candi):
                return False

        return True

    def gen(self):

        # step 0 init
        self.init(tk)

        # step 1 setup solution
        ref = list(range(1, 10))
        random.shuffle(ref)
        #ref = [8,9,3,2,7,6,4,5,1]
        res = [ref]
        for i in range(1, 9):
            if i % 3 != 0:
                temp = res[-1][3:] + res[-1][:3]
                res.append(temp)
            else:
                temp = res[-1][1:] + res[-1][:1]
                res.append(temp)
        print(res)

        # step 2 based on the res randomly choose total_shown elements and set the answer


        while self.done() != 1:
            collection = []
            self.init(tk)
            total_shown = 30
            counter = 0
            while counter != total_shown:

                r = random.randint(0, 8)
                c = random.randint(0, 8)
                if self.element[r][c]["find"] != 0:
                    continue

                self.element[r][c]["candidate"] = []
                self.element[r][c]["candidate"].append(res[r][c])
                self.element[r][c]["find"] = res[r][c]

                self.element_entry[r][c].insert(0, str(res[r][c]))
                collection.append([r,c])

                counter += 1

            self.ready()
            self.run()

        self.init(tk)
        for c in collection:
            self.element_entry[c[0]][c[1]].insert(0, str(res[c[0]][c[1]]))







    # basic setting
    def find_row_group(self, i):
        if i < 3:
            return 0
        elif i < 6:
            return 1
        else:
            return 2

    def find_col_group(self, j):
        if j < 3:
            return 0
        elif j < 6:
            return 1
        else:
            return 2

    def find_blk(self, i, j):
        return i // 3 + 3 * (j // 3)

    def return_blk(self, b):
        result = []
        for r in range(9):
            for c in range(9):
                if self.element[r][c]["block"] == int(b):
                    result.append(self.element[r][c])
        return result

    def find_color(self, i, j):
        if i > 2 and i < 6 and j > 2 and j < 6:
            return "grey"
        elif i > 2 and i < 6 or j > 2 and j < 6:
            return "white"
        else:
            return "grey"

    # reset to clear status
    def reset(self):
        for i in range(9):
            for j in range(9):
                self.element_entry[i][j].delete(0, "end")
                self.element[i][j]["find"] = 0
                self.element[i][j]["candidate"] = list(range(1, 10))

    # ready , if entry has value , set find and candidate
    def ready(self):
        for i in range(9):
            for j in range(9):
                if self.element_entry[i][j].get() != "":
                    self.element[i][j]["find"] = int(self.element_entry[i][j].get())
                    self.element[i][j]["candidate"] = []
                    self.element[i][j]["candidate"].append(int(self.element_entry[i][j].get()))

    # answer handling, in each attemp see if new answer has been found !
    def find_any_answer(self):
        for r in range(9):
            for c in range(9):
                if self.element[r][c]["find"] == 0 and len(self.element[r][c]["candidate"]) == 1:
                    return 1
        return 0

    def update_answer(self):
        for r in range(9):
            for c in range(9):
                if self.element[r][c]["find"] == 0 and len(self.element[r][c]["candidate"]) == 1:
                    self.element[r][c]["find"] = int(self.element[r][c]["candidate"][0])
                    self.element_entry[r][c].insert(0, str(self.element[r][c]["candidate"][0]))

    def done(self):
        for i in range(9):
            for j in range(9):
                if self.element[i][j]["find"] == 0:
                    return 0
        return 1

    # define key logic
    def remove_candidate_in_same_row(self, candidate, r):
        for i in range(9):
            if self.element[r][i]["find"] == 0:
                if int(candidate) in self.element[r][i]["candidate"]:
                    self.element[r][i]["candidate"].remove(int(candidate))

    def remove_candidate_in_same_col(self, candidate, c):
        for i in range(9):
            if self.element[i][c]["find"] == 0:
                if int(candidate) in self.element[i][c]["candidate"]:
                    self.element[i][c]["candidate"].remove(int(candidate))

    def remove_candidate_in_same_blk(self, candidate, b):
        for i in range(9):
            for j in range(9):
                if self.element[i][j]["block"] == b:
                    if self.element[i][j]["find"] == 0:
                        if int(candidate) in self.element[i][j]["candidate"]:
                            self.element[i][j]["candidate"].remove(int(candidate))

    # the first skill
    def remove_basic(self):
        for i in range(9):
            for j in range(9):
                if self.element[i][j]["find"] > 0:
                    self.remove_candidate_in_same_row(self.element[i][j]["find"], i)
                    self.remove_candidate_in_same_col(self.element[i][j]["find"], j)
                    self.remove_candidate_in_same_blk(self.element[i][j]["find"], self.element[i][j]["block"])

        if self.find_any_answer() == 1 and self.done() == 0:
            self.update_answer()
            self.remove_basic()

    def the_only_candidate_in_row(self):
        for r in range(9):
            temp_r = list(range(1, 10))
            for c in range(9):
                if self.element[r][c]["find"] > 0:
                    temp_r.remove(self.element[r][c]["find"])
            if len(temp_r) == 0:
                continue
            else:
                for n in temp_r:
                    counter = 0
                    for c in range(9):
                        if self.element[r][c]["find"] == 0 and n in self.element[r][c]["candidate"]:
                            counter += 1
                            temp_pos = c
                    if counter == 1:
                        self.element[r][temp_pos]["candidate"] = []
                        self.element[r][temp_pos]["candidate"].append(n)

    def the_only_candidate_in_col(self):
        for c in range(9):
            temp_c = list(range(1, 10))
            for r in range(9):
                if self.element[r][c]["find"] > 0:
                    temp_c.remove(self.element[r][c]["find"])
            if len(temp_c) == 0:
                continue
            else:
                for n in temp_c:
                    counter = 0
                    for r in range(9):
                        if self.element[r][c]["find"] == 0 and n in self.element[r][c]["candidate"]:
                            counter += 1
                            temp_pos = r
                    if counter == 1:
                        self.element[temp_pos][c]["candidate"] = []
                        self.element[temp_pos][c]["candidate"].append(n)

    def the_only_candidate_in_blk(self):
        for b in range(9):
            temp_b = list(range(1, 10))
            element_in_b = self.return_blk(b)
            for el in element_in_b:
                if el["find"] > 0:
                    temp_b.remove(el["find"])
            if len(temp_b) == 0:
                continue
            else:
                for n in temp_b:
                    counter = 0
                    for el in element_in_b:
                        if el["find"] == 0 and n in el["candidate"]:
                            counter += 1
                            pos_r = el["row"]
                            pos_c = el["col"]
                    if counter == 1:
                        self.element[pos_r][pos_c]["candidate"] = []
                        self.element[pos_r][pos_c]["candidate"].append(n)

    # the second skill
    def the_only_candidate(self):
        self.the_only_candidate_in_row()
        self.the_only_candidate_in_col()
        self.the_only_candidate_in_blk()

        if self.find_any_answer() == 1 and self.done() == 0:
            self.update_answer()
            self.remove_basic()
            self.the_only_candidate()

    def remove_2_candidates_in_same_row(self):
        for r in range(9):
            for c in range(9):
                if self.element[r][c]["find"] == 0 and len(self.element[r][c]["candidate"]) == 2:
                    for c1 in range(c + 1, 9):
                        if self.element[r][c1]["find"] == 0 and len(self.element[r][c1]["candidate"]) == 2:
                            self.element[r][c]["candidate"].sort()
                            self.element[r][c1]["candidate"].sort()
                            if self.element[r][c]["candidate"] == self.element[r][c1]["candidate"]:
                                for c2 in range(9):
                                    if c2 != c and c2 != c1 and self.element[r][c2]["find"] == 0:
                                        if self.element[r][c]["candidate"][0] in self.element[r][c2]["candidate"]:
                                            self.element[r][c2]["candidate"].remove(self.element[r][c]["candidate"][0])
                                        if self.element[r][c]["candidate"][1] in self.element[r][c2]["candidate"]:
                                            self.element[r][c2]["candidate"].remove(self.element[r][c]["candidate"][1])

    def remove_2_candidates_in_same_col(self):
        for c in range(9):
            for r in range(9):
                if self.element[r][c]["find"] == 0 and len(self.element[r][c]["candidate"]) == 2:
                    for r1 in range(r + 1, 9):
                        if self.element[r1][c]["find"] == 0 and len(self.element[r1][c]["candidate"]) == 2:
                            self.element[r][c]["candidate"].sort()
                            self.element[r1][c]["candidate"].sort()
                            if self.element[r][c]["candidate"] == self.element[r1][c]["candidate"]:
                                for r2 in range(9):
                                    if r2 != r and r2 != r1 and self.element[r2][c]["find"] == 0:
                                        if self.element[r][c]["candidate"][0] in self.element[r2][c]["candidate"]:
                                            self.element[r2][c]["candidate"].remove(self.element[r][c]["candidate"][0])
                                        if self.element[r][c]["candidate"][1] in self.element[r2][c]["candidate"]:
                                            self.element[r2][c]["candidate"].remove(self.element[r][c]["candidate"][1])

    def remove_2_candidates_in_same_blk(self):
        global element
        for b in range(9):
            element_in_b = self.return_blk(b)
            for i in range(9):
                if element_in_b[i]["find"] == 0 and len(element_in_b[i]["candidate"]) == 2:
                    for i1 in range(i + 1, 9):
                        if element_in_b[i1]["find"] == 0 and len(element_in_b[i1]["candidate"]) == 2:
                            element_in_b[i]["candidate"].sort()
                            element_in_b[i1]["candidate"].sort()
                            if element_in_b[i]["candidate"] == element_in_b[i1]["candidate"]:
                                for i2 in range(9):
                                    if i2 != i and i2 != i1 and element_in_b[i2]["find"] == 0:
                                        if element_in_b[i]["candidate"][0] in element_in_b[i2]["candidate"]:
                                            element_in_b[i2]["candidate"].remove(element_in_b[i]["candidate"][0])
                                        if element_in_b[i]["candidate"][1] in element_in_b[i2]["candidate"]:
                                            element_in_b[i2]["candidate"].remove(element_in_b[i]["candidate"][1])

    # the third skill
    def two_in_the_group(self):
        self.remove_2_candidates_in_same_row()
        self.remove_2_candidates_in_same_col()
        self.remove_2_candidates_in_same_blk()
        if self.find_any_answer() == 1 and self.done() == 0:
            self.update_answer()
            self.remove_basic()
            self.the_only_candidate()
            self.two_in_the_group()

    # the 4th skill for final guessing !
    def find_unknown_with_candidate_2(self):
        result = []
        for r in range(9):
            for c in range(9):
                if self.element[r][c]["find"] == 0 and len(self.element[r][c]["candidate"]) == 2:
                    result.append(self.element[r][c])
        return result

    def test_candidate(self, test_element):
        self.reset()
        self.recall()
        self.element_entry[test_element["row"]][test_element["col"]].insert(0, str(test_element["candidate"][0]))
        self.ready()
        # print(element[1][8])
        try:
            self.remove_basic()
            self.the_only_candidate()
            self.two_in_the_group()
            # print(element[1][8])
        except:
            return 2

        if self.done() == 1:
            return 1
        else:
            return 3

    # run
    def run(self):
        self.remove_basic()
        self.the_only_candidate()
        self.two_in_the_group()

        if self.done() == 0:
            self.save()
            while self.test_counter < 30:
                test_list = copy.deepcopy(self.find_unknown_with_candidate_2())

                for tester in test_list:
                    if self.test_counter % 2 != 0:
                        tester["candidate"].reverse()
                    test_result = self.test_candidate(tester)
                    if test_result == 1:
                        break
                    elif test_result == 2:
                        self.reset()
                        self.recall()
                        self.element_entry[tester["row"]][tester["col"]].insert(0, str(tester["candidate"][1]))
                        # print(element[1][8])
                        self.ready()
                        self.remove_basic()
                        self.the_only_candidate()
                        self.two_in_the_group()
                        if self.done() == 1:
                            debug_msg.set("find solution!!")
                            break
                        else:
                            self.save()
                            break
                    else:
                        self.reset()
                        self.recall()
                        self.ready()
                        self.remove_basic()
                        self.the_only_candidate()
                        self.two_in_the_group()
                        # print(element[1][8])
                        continue

                if self.done() == 1:
                    debug_msg.set("find solution!")
                    break
                self.test_counter += 1

    # save button for test purpose
    def save(self):
        self.zip_element = copy.deepcopy(self.element)

    def recall(self):
        if len(self.zip_element) != 0:
            for r in range(9):
                for c in range(9):
                    if self.zip_element[r][c]["find"] != 0:
                        self.element_entry[r][c].insert(0, str(self.zip_element[r][c]["find"]))
                    else:
                        for i in range(1, 10):
                            if i not in self.zip_element[r][c]["candidate"]:
                                self.element[r][c]["candidate"].remove(i)


mySudoku = Sudoku_generator()
mySudoku.init(tk)

# Greeting label
greeting_label = tk.Label(text="Welcome to October's Sudoku generator", bg="SkyBlue1", fg="blue")
greeting_label.grid(row=0, column=0, padx=10, columnspan=8)

# reset button
gen_button = tk.Button(text='gen', fg='black', command=mySudoku.gen)
gen_button.grid(row=10, column=10, padx=5, pady=5)

"""# set button
ready_button = tk.Button(text='ready', fg='black', command=mySudoku.ready)
ready_button.grid(row=11, column=10, padx=5, pady=5)

# run button
run_button = tk.Button(text='run', fg='black', command=mySudoku.run)
run_button.grid(row=11, column=11, padx=5, pady=5)

# save button for test purpose only
save_button = tk.Button(text='save', fg='black', command=mySudoku.save)
save_button.grid(row=12, column=10, padx=5, pady=5)

# recall button for test purpose only
call_button = tk.Button(text='recall', fg='black', command=mySudoku.recall)
call_button.grid(row=12, column=11, padx=5, pady=5)"""

# debug message
debug_msg = tk.StringVar()
debug_label = tk.Message(window, textvariable=debug_msg, bg="SkyBlue1", width=400)

debug_msg.set("")
debug_label.grid(row=10, column=0, columnspan=9)

window.mainloop()