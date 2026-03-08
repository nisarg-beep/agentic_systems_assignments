class StudentMarks:
    def __init__(self,marks_list):
        self.marks = marks_list

    def last_three_avg(self):
        try:
            if len(self.marks) < 3:
                raise ValueError("Not enough marks to calculate average")

            last_three_marks = []
            for a in self.marks[-3:]:
                last_three_marks.append(a)

            res = sum(last_three_marks)/len(last_three_marks)
            print("Average of last 3 marks is: ",res)

        except ValueError as e:
            print(e)


n = int(input("enter the numbers of marks to be entered :"))
marks_list = []

for i in range(n):
    enter_marks = int(input("enter the marks:"))
    marks_list.append(enter_marks)

student = StudentMarks(marks_list)
student.last_three_avg()