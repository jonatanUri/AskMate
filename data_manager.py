import csv


def csv_read_question():
    with open("/home/jonatan/codecool/WEB/SI1/ksfhdjgfh/sample_data/question.csv", "r") as questions:
        reader = csv.DictReader(questions)
        myList = []
        for row in reader:
            myList.append(row)
    return myList
