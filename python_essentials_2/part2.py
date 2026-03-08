class StudentScores:
    def __init__(self,scores_list):
        self.scores = scores_list

    def highest_last_two(self):
        try:
            if len(self.scores) < 2:
                raise ValueError("Not enough scores to find highest value")

            last_two_scores = []
            for a in self.scores[-2:]:
                last_two_scores.append(a)

            highest = max(last_two_scores)
            print("Highest score among last two is: ",highest)

        except ValueError as e:
            print(e)

n = int(input("enter the numbers of scores to be entered :"))
scores_list = []

for i in range(n):
    enter_scores = int(input("enter the scores:"))
    scores_list.append(enter_scores)

student = StudentScores(scores_list)
student.highest_last_two()