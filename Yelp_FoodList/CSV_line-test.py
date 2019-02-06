import csv

# encoding parameter elims unicode print
with open('test.csv', encoding='utf-8-sig') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter =',')

    # header var declaration so it can start read from 2nd row
    header = next(csv_reader)
    line_count = 0
    new_list = []
    for row in csv_reader:
        new_list.append(row[0])
        line_count += 1
        print(row)
    print(new_list, "\n")

