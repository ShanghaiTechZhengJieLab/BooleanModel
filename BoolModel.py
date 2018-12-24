max_loop=10
count_symbol=['&','!','(',')','-','|']
symbol={}
symbol_name=[]
signal={}
signal_name=[]
rules=[]
def count_value(string):
    # print(string)
    if string[0] != '(':
        value=int(string[0])
        index=0
    else:
        end_pos=string.find(')')
        value=count_value(string[1:end_pos])
        index=end_pos+1
    while True:
        end_pos=0
        if index>=len(string)-1:break
        if string[index] in count_symbol:
            if string[index]=='&' or string[index]=='!' or string[index]=='|' or string[index]=='-':
                if string[index+1]=='(':
                    end_pos=string[index+1:].find(')')
                    next_value=count_value(string[index+2:end_pos+index+1])
                else:next_value=int(string[index+1])
                # print(value,next_value,string[index])
                if string[index]=='&':
                    value*=next_value
                elif string[index]=='!':
                    if next_value==0:next_value=1
                    else:next_value=0
                    value*=next_value
                elif string[index]=='|':
                    if value==0 and next_value==0:
                        value=0
                    else:value=1
                elif string[index]=='-':
                    if value==next_value:value=0
                    else:value=1
        index += end_pos + 1
    return value

with open('./data/rules.txt',encoding='utf-8') as f:
    for i,line in enumerate(f.readlines()):
        line=line.split('\n')[0].split(' ')
        if len(line)==4 and line[2]!='':
            symbol[line[0]]={}
            symbol_name.append(line[0])
            symbol[line[0]]['value']=int(line[2])
            symbol[line[0]]['is_observed']=1
            if line[3]=='I':
                symbol[line[0]]['is_observed']=0
                # symbol[line[0]]['value']=0
            symbol[line[0]]['rule']=line[1].replace('&!','!')
        else:
            signal[line[0]]=int(line[1])
            signal_name.append(line[0])

symbol_name.sort(key=lambda i:len(i),reverse=True)
signal_name.sort(key=lambda i:len(i),reverse=True)
print(symbol_name)
print(symbol)
print(signal)
print(symbol_name)

loop_dic={}

for _ in range(max_loop):
    old_string=''
    for key in symbol.keys():
        tmp_string=symbol[key]['rule']
        for key_name in symbol_name:
            tmp_string=tmp_string.replace(key_name,str(symbol[key_name]['value']))
        for key_name in signal_name:
            tmp_string=tmp_string.replace(key_name,str(signal[key_name]))
        symbol[key]['func']=tmp_string
        old_string+=str(symbol[key]['value'])
    tmp_symbol=symbol
    value_string=''
    key_string=''
    all_string=''
    all_key={}
    value_dic={}
    for key in symbol.keys():
        tmp_symbol[key]['value']=count_value(symbol[key]['func'])
        if symbol[key]['is_observed']==1:
            value_string+=str(tmp_symbol[key]['value'])
            value_dic[key]=str(tmp_symbol[key]['value'])
        all_string+=str(tmp_symbol[key]['value'])
        all_key[key]=str(tmp_symbol[key]['value'])
    # print(symbol)

    print(value_string)
    print(value_dic)
    print(all_string)
    print(all_key)
    if old_string not in loop_dic:
        loop_dic[old_string]={}
    if all_string not in loop_dic[old_string]:
        loop_dic[old_string][all_string]=0
    elif loop_dic[old_string][all_string]!=1:
        loop_dic[old_string][all_string]+=1
    else:break
    symbol=tmp_symbol


def write_to_file(path):
    def _write_func(string):
        new_string=''
        for i in string:
            new_string+=i+'\t'
        return new_string
    with open(path,'w',encoding='utf-8') as f:
        for id,key in enumerate(loop_dic):
            if id==0:
                f.write(_write_func(key)+'0'+'\n')
            for my_key in loop_dic[key]:
                f.write(_write_func(my_key)+str(loop_dic[key][my_key])+'\n')
    print(loop_dic)
write_to_file('S5-0.txt')
