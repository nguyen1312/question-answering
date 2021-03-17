import json
import csv, sys
from ast import literal_eval
from datetime import date

def modifyDict(inputDict):
    listt = zip(inputDict.keys(), inputDict.values()) 
    listt = list(listt)[:-1]
    return dict(listt) 

def make_data_list(filename, phase):
    noOfLine = 0
    totalSample = []
    totalSamplev1 = []
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        id = 0
        try:
            for row in reader:
                if noOfLine > 0:
                    if phase == "train":
                        questions = literal_eval(row[0])
                        answers = literal_eval(row[1])
                        for i in range(len(questions)):
                            id += 1
                            obj = {}
                            
                            objv1 = {}
                            objv1['question'] = modifyDict(questions[i])['input_text']
                            objv1['answer'] = modifyDict(answers[i])['span_text']

                            obj["id"] = id
                            obj["question"] = modifyDict(questions[i])
                            obj["answer"] = [modifyDict(answers[i])]
                            totalSample.append(obj) 
                            totalSamplev1.append(objv1)
                    elif phase == "test":
                        questions = literal_eval(row[0])
                        answers = literal_eval(row[1])
                        additional_answers = literal_eval(row[2])
                        keysOfCol3 = list(additional_answers.keys())
                        for i in range(len(questions)):
                            id += 1
                            obj = {}
                            obj["id"] = id
                            obj["question"] =  modifyDict(questions[i])
                            obj["answer"] = [modifyDict(answers[i])]
                            for key in keysOfCol3:
                                obj["answer"].append(modifyDict(additional_answers[key][i]))
                            totalSample.append(obj) 
                    else:
                        return None
                noOfLine += 1
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
    
    return totalSample, len(totalSample), id, totalSamplev1

def writeToJson(lst, filename):
    with open(filename, 'w') as fout:
        json.dump(lst , fout)

if __name__=="__main__":
    trainSet, lenTrainSet, lastIdTrain, v1 = make_data_list("train.csv", "train")
    testSet, lenTestSet, lastIdTest, _ = make_data_list("test.csv", "test")

    print("Len Train Set: ", lenTrainSet)
    print("Last Train ID: ", lastIdTrain)
    print(v1[:10])
    # print("Len Test Set: ", lenTestSet)
    # print("Last Test ID: ", lastIdTest)
    # print(testSet[10])
    # writeToJson(trainSet, "train.json")
    # writeToJson(testSet, "test.json")

   
    header=['question','answer']     
    try:
        with open('output'+str(date.today())+'.csv',mode='w',encoding='utf8',newline='') as output_to_csv:
            dict_csv_writer = csv.DictWriter(output_to_csv, fieldnames=header,dialect='excel')
            dict_csv_writer.writeheader()
            dict_csv_writer.writerows(v1)
        print('\nData exported to csv succesfully and sample data')
    except IOError as io:
        print('\n',io)