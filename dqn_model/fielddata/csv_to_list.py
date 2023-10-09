import csv
import os
import sys

try:
    path=sys.argv[0]
except:
    path=__file__

def input_csv(dir,filename):
    id=os.path.splitext(filename)[0]
    ike=[]
    shiro=[]
    first=[]
    second=[]
    with open(os.path.join(dir,filename), 'r') as file:
        reader = csv.reader(file)
        for i,line in enumerate(reader):
            for j,cell in enumerate(line):
                if cell=='1':
                    ike.append((j,i))
                elif cell=='2':
                    shiro.append((j,i))
                elif cell=='a':
                    first.append((j,i))
                elif cell=='b':
                    second.append((j,i))
    text='''\
elif id == '{}':
    width={}
    height={}
    ike={}
    shiro={}
    first_shokunin={}
    second_shokunin={}
'''.format(id,i+1,j+1,ike,shiro,first,second)

    print(filename)
    return text
                    
                
dir=os.path.dirname(path)

input_files=sorted(os.listdir(dir))
count=0
text=[]
for input_file in input_files:
    if os.path.splitext(input_file)[1]=='.csv':
        text.append(input_csv(dir,input_file))
        count+=1
with open(os.path.join(dir,'output_csv.log'),'w') as output_file:
    output_file.write("#["+",".join(["'"+os.path.splitext(i)[0]+"'" for i in input_files if os.path.splitext(i)[1]=='.csv'])+"]\n"+"\n".join(text))

print("{}個のCSVファイルを読み取り完了".format(count))
print("出力ファイル:{}".format(output_file))