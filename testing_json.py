import json

'''
json_file = [
    'id' : num,
    text_1 : "
        awdawd [daw]  awddaw [dwa] dwadawd awdawd.
    ",
    text_2 : "
        awdwdawd [daw]  awdzxcdaw [dwzxca] dwazxcdawd awzxcdawd.
    ",
    text_3 : "
        awdwdawd/awdzxcdaw/dwazxcdawd/awzxcdawd.
    ",
    text_4 : "
        awdwdawd/awdzxcdaw/dwazxcdawd/awzxcdawd.
    ",
    text_5 : "
         assasa awdwdawd/awdzxcdaw/<dwazxcdawd>/awzxcdawd.
         assasa awdwdawd/<awdzxcdaw>/dwazxcdawd/awzxcdawd.
         assasa awdwdawd/awdzxcdaw/<dwazxcdawd>/awzxcdawd.
         assasa awdwdawd/awdzxcdaw/<dwazxcdawd>/awzxcdawd.
    ",
    text_6 : "
        [asd - wda],
        [fqw - dqw],
        [ger - dqwiju]
    ",
    text_7 : "
        [asd - wda{image}],
        [fqw - dqw{image}],
        [ger - iju{image}]

    ",
    text_8 : "
        "asdasd1" : "asdasd/asdasd/asdasd/asdasd",
        "asdasd2" : "asdasd/asdasd/asdasd/asdasd",
        "asdasd3" : "asdasd/asdasd/asdasd/asdasd",
        "asdasd4" : "asdasd/asdasd/asdasd/asdasd",
    ",
    text_9 : "
        "[asdasd asdasdwda asdawdasd asdasd]/[daw aw da wd wad]",
        "asdasd asdasdwda asdawdasd asdasd",
        "[asdasd asdasdwda asdawdasd asdasd]/[daw aw da wd wad]",
    ", 
]
'''

json_file = {
    'id' : 1,
    "text" : "awdawd [daw]  awddaw [dwa] dwadawd awdawd.",
}

json_file_answer = {
    'id' : 1,
    "text" : "awdawd [daw/daw]  awddaw [daw/dwa] dwadawd awdawd.",
}

json_file_2 = {
    'id' : 2,
    "text" : "awdwdawd [daw]  awdzxcdaw [dwzxca] dwazxcdawd awzxcdawd."
}

json_file_3 = {
    'id':3,
    "text" : "awdwdawd/awdzxcdaw/dwazxcdawd/awzxcdawd."
}

json_file_answer_3 = {
    'id':3,
    "text" : "awdzxcdaw/awdwdawd/dwazxcdawd/awzxcdawd.|awdwdawd/awdzxcdaw/dwazxcdawd/awzxcdawd."
}

json_file_4 = {
    'id':4,
    "text" : "awdwdawd/awdzxcdaw/dwazxcdawd/awzxcdawd."
}
json_file_5 = {
    'id':5,
    "text" : 'assasa awdwdawd/awdzxcdaw/<dwazxcdawd>/awzxcdawd. | assasa awdwdawd/<awdzxcdaw>/dwazxcdawd/awzxcdawd. | assasa awdwdawd/awdzxcdaw/<dwazxcdawd>/awzxcdawd. | assasa awdwdawd/awdzxcdaw/<dwazxcdawd>/awzxcdawd.'   
}
json_file_answer_5 = {
    'id':5,
    "text" : 'assasa awdwdawd/awdzxcdaw/dwazxcdawd/[<awzxcdawd>]. | assasa awdwdawd/<awdzxcdaw>/[dwazxcdawd]/awzxcdawd. | assasa awdwdawd/awdzxcdaw/[<dwazxcdawd>]/awzxcdawd. | assasa awdwdawd/awdzxcdaw/[<dwazxcdawd>]/awzxcdawd.'   
}

json_file_6 = {
    'id':6,
    "text" : "[asd - wda],[fqw - dqw],[ger - dqwiju]"
}
json_file_6_answer = {
    'id':6,
    "text" : "[asd - wda]/[asd - wda],[ger - dqw]/[fqw - dqw],[fqw - dqwiju]/[ger - dqwiju]"
}

json_file_7 = {
    'id':7,
    "text" : "[asd - wda{image}],[fqw - dqw{image}],[ger - iju{image}]"
}
json_file_7_answer = {
    'id':7,
    "text" : "[wda{image}]/[wda{image}],[dqw{image}]/[dqw{image}],[dqw{image}]/[iju{image}]"
}

json_file_8 = {
    'id':8,
    "text" : {
        "asdasd1 : asdasd/asdasd/asdasd/asdasd , asdasd2 : asdasd/asdasd/asdasd/asdasd , asdasd3 : asdasd/asdasd/asdasd/asdasd",
    }
}
json_file_8_answer = {
    'id':8,
    "text" : {
        "asdasd1" : "asdasd/asdasd/asdasd/asdasd|asdasd/asdasd/asdasd/asdasd",
        "asdasd2" : "asdasd/asdasd/asdasd/asdasd|asdasd/asdasd/asdasd/asdasd",
        "asdasd3" : "asdasdwad/asdasd/asdasd/asdasd|asdasd/asdasd/asdasd/asdasd",
    }
}
json_file_9 = {
    'id':9,
    "text" : {
        "[1 2 3 4]/[1 1 2 3]",
        "q w e r",
        "[a s a a]/[f d d x c]",
    }
}
json_file_9_answer = {
    'id':9,
    "text" : "aw asdasdwda asdawdasd asdasd/aw asdasdwda asdawdasd asdasd,asdasd asdasdwda asdawdasd asdasd,asdasd asdasdwda asdawdasd asdasd/daw aw da wd wad"
    
}


json_string = json.dumps(json_file_9_answer)

print(type(json_string) , json_string)

decoded = json.loads(json_string)

print(type(decoded) , decoded)

if(decoded.get('id')==1):
    words = decoded.get('text').split()
    count = 0
    count_of = 0
    for item in words:
        if(item[0]=='[' and item[-1]==']'):
            item = item.replace('[','')
            item = item.replace(']','')
            checking = item.split('/')
            count_of+=1
            if(checking[0] == checking[1]):
                count+=1
            print(checking)
    print("correct answers:", count,"from",count_of)
        
if(decoded.get('id')==2):
    print('2')


if(decoded.get('id')==3):
    words = decoded.get('text').split("|")
    count = 0
    count_of = 0
    if(words[0]==words[1]):
        print('correct')
    else:
        print('inccorrect. correct answer is',words[1])


if(decoded.get('id')==5):
    words = decoded.get('text').replace('.','').split("|")
    count = 0
    count_of = 0
    for item in words:
        count_of+=1
        checking = item.split()
        for item2 in checking[1].split('/'):
            if(item2[0]=='[' and item2[-1]==']'):
                if(item2[1]=='<' and item2[-2]=='>'):
                    count += 1
    print('correct answers:',count,'from',count_of)

if(decoded.get('id')==6):
    words = decoded.get('text').split(",")
    count = 0
    count_of = 0
    for item in words:
        count_of+=1
        item = item.split('/')
        if(item[0]==item[1]):
            count+=1
    print("correct answers:",count,"from",count_of)

if(decoded.get('id')==7):
    words = decoded.get('text').split(",")
    count = 0
    count_of = 0
    for item in words:
        count_of+=1
        item = item.split('/')
        if(item[0]==item[1]):
            count+=1
    print("correct answers:",count,"from",count_of)


if(decoded.get('id')==8):
    words = decoded.get('text')
    correct = True
    for key,value in words.items():
        checking = value.split('|')
        if(checking[0]!=checking[1]):
            correct = False
    print(correct)
            
        
if(decoded.get('id')==9):
    words = decoded.get('text').split(',')
    correct = 0
    count_of = 0
    # print(words)
    for item in words:
        checking = item.split('/')
        # print(checking)
        count_of+=1
        if(len(checking)>1):
            if(checking[0]!=checking[1]):
                correct +=1
        else:
            correct+=1
    print("correct sentenses:",correct,"from",count_of)
            
        







