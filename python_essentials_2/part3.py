class StudentPerformance:
    def __init__(self,performance_list):
        self.performance = performance_list

    def score_difference(self):
        try:
            if len(performance_list) < 2 :
                raise ValueError("No scores available to calculate difference")

            result = performance_list[0]-performance_list[-1]
            print("Difference between last and first score is: ",result)

        except ValueError as e:
            print(e)

n = int(input("enter the numbers of scores to be entered :"))
performance_list = []

for i in range(n):
    enter_performance = int(input("enter the scores:"))
    performance_list.append(enter_performance)

student = StudentPerformance(performance_list)
student.score_difference()