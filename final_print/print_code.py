import re
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image as pilimg

part = ['bumper', 'fender', 'door']
damage_ordered = ['rust', 'scratch', 'strong_scratch', 'concave', 'strong_concave', 'tear', 'crush']
damage = ['crush', 'tear', 'strong_concave', 'rust', 'strong_scratch', 'concave', 'scratch']
# �ֻ��� ���� �̱����� damage ���� ����


#R���� ����� ���� ������ DICTIONARY�� ����dic = dict()
dic['bumper,rust'] = [[10, 15], [15, 20]]
dic['fender,rust'] = [[15, 20], [10, 15], [20, 25]]
dic['door,rust'] = [[15, 20], [20, 25]]

dic['bumper,scratch'] = [[0, 10], [10, 15]]
dic['fender,scratch'] = [[0, 10], [15, 20]]
dic['door,scratch'] = [[15, 20], [20, 25]]

dic['bumper,strong_scratch'] = [[15, 20], [20, 25]]
dic['fender,strong_scratch'] = [[10, 15], [15,20]]
dic['door,strong_scratch'] = [[10, 15], [15,20]]

dic['bumper,concave'] = [[10, 15], [15,20]]
dic['fender,concave'] = [[10, 15], [15,20]]
dic['door,concave'] = [[15, 20], [20, 25]]

dic['bumper,strong_concave'] = [[15, 20], [20, 25]]
dic['fender,strong_concave'] = [[15,15],[20,20]]
dic['door,strong_concave'] = [[10, 15], [15, 20]]

dic['bumper,tear'] = [[10, 15], [15, 20]]
dic['fender,tear'] = [[10,15], [15, 20], [20, 25]]
dic['door,tear'] = [[15, 20], [20, 25]]

dic['bumper,crush'] = [[25, 30], [30, 35]]
dic['fender,crush'] = [[20, 25], [25, 30]]
dic['door,crush'] = [[35, 40], [40, 50]]


def refine_p(f):  # ��ǥ�ؽ�Ʈ ���� �Լ�_part
    res = []
    res2 = []
    res3 = []
    file = f.split(' ')
    file2 = [re.sub(':', '', i) for i in file]
    file2 = [re.sub('\n', '', i) for i in file2]
    file2 = [re.sub('', '', i) for i in file2]
    for i in file2:
        res.append(i.split(','))
    for i in res:
        for j in i:
            if j == '':
                break
            else:
                res2.append(j)
    res2 = res2[5:]
    # print(res2)
    dic = defaultdict(list)
    for idx, i in enumerate(res2):
        if i in part:
            if res2[int(idx) + 2] == 'Bounding':
                for z in res2[idx + 4: idx + 7 + 1]:
                    res3.append(re.sub('[^0-9]', '', z))
                    if len(res3) == 4:
                        dic[i].append(res3)
                        res3 = []
                        # print('p-dic:',dic)
    return dic


def refine_d(f):  # ��ǥ�ؽ�Ʈ ���� �Լ�_damage
    res = []
    res2 = []
    res3 = []
    file = f.split(' ')
    file2 = [re.sub(':', '', i) for i in file]
    file2 = [re.sub('\n', '', i) for i in file2]
    file2 = [re.sub('', '', i) for i in file2]
    for i in file2:
        res.append(i.split(','))
    for i in res:
        for j in i:
            if j == '':
                break
            else:
                res2.append(j)
    res2 = res2[5:]
    # print(res2)
    dic = defaultdict(list)

    for idx, j in enumerate(res2):
        if j in damage:
            if res2[int(idx) + 2] == 'Bounding':
                for zz in res2[idx + 4: idx + 7 + 1]:
                    res3.append(re.sub('[^0-9]', '', zz))
                    if len(res3) == 4:
                        dic[j].append(res3)
                        res3 = []
    # print('d-dic:',dic)
    return dic


def navigate(f, i):  # ��ǥ��� �Լ�
    idxxx = i
    p_data = refine_p(f)
    d_data = refine_d(f)
    car_position = []
    damage_position = []
    param = 0
    result_text = []

    for i in p_data.keys():
        car_position.append(i)
    for i in d_data.keys():
        damage_position.append(i)

    t = 0
    while t < 1:
        if len(car_position) == 0:
             print("**alarm: %d ������ ������ ���������� �����ϴ�" % (idxxx))
            break
        elif len(damage_position) == 0:
            print("**alarm: %d ������ ������ �������� �����ϴ�" % (idxxx))
            break

        for i00 in part:
            try:
                if i00 in car_position:
                    cp = i00
                    # print('cp:',cp)
                for i11 in damage_position:
                    try:
                        if i11 in damage:
                            dp = i11
                            # print('dp:',dp)                    
                        # ��ǥ ��Ī��Ű��  for ��
                        for ii in range(len(p_data[cp])):
                            for j in range(len(d_data[dp])):
                                for z in range(4):
                                    if z == 0:
                                        if int(p_data[cp][ii][z]) < int(d_data[dp][j][z]) < int(
                                                p_data[cp][ii][z + 2]):  # left
                                            param += 1
                                    if z == 1:
                                        if int(p_data[cp][ii][z]) < int(d_data[dp][j][z]) < int(
                                                p_data[cp][ii][z + 2]):  # top
                                            param += 1
                                    if z == 2:
                                        if int(p_data[cp][ii][z - 2]) < int(d_data[dp][j][z]) < int(
                                                p_data[cp][ii][z]):  # right
                                            param += 1
                                    if z == 3:
                                        if int(p_data[cp][ii][z - 2]) < int(d_data[dp][j][z]) < int(
                                                p_data[cp][ii][z]):  # bottom
                                            param += 1
                                if param >= 3:
                                    result_text.append([idxxx, cp, dp])
                                param = 0
                    except:
                        pass
            except:
                pass
        t += 1
         # �ߺ����� �����ϰ�, �ֻ����� ���
    prt = ''
    result = []
    #print(result_text)
    for j in result_text:
        if prt == j[1]:
            pass
        else:
            for i in damage:
                 if i == j[2]:
                    print("%d ����: %s�� %s�� �����Ǿ����ϴ�." % (j[0], j[1], j[2]))
                    result.append([j[1], j[2]])
                    prt = j[1]
                    break
                else:
                    pass
######################################            

    for p in range(len(result)):
        cnt=0
        for q in damage:
            cnt +=1
            if result[p][1]==q:
                result[p].insert(0,cnt)
                continue
                                 
    #print(result)
    result.sort()
    #print(result)
   
    price = []             #�� ������ ���� ���� [[10,15],[15,20]]
    price_detail = []      #�� ������ ���� ���� -��ճ��� [bumper,��ǰ��ü,12.5,17.5]
    price_total = [0, 0]   #�Ѱ��� �ּ� ,�ִ�

    dic2 = dict()
    dic2['crush'] = '��ǰ��ü'
    dic2['tear'] = '�Ǳݵ���/��ȯ'
    dic2['strong_concave'] = '�Ǳݵ���'
    dic2['concave'] = '��Ʈ/�Ǳݵ���'
    dic2['rust'] = '�Ǳݵ���'
    dic2['strong_scratch'] = '�Ǳݵ���'
    dic2['scratch'] = '����/�κе���'
    
    for i in range(len(result)):
        k = result[i][1] + ',' + result[i][2]

        for j in dic.keys():

            if k == j:
                price.append([p for p in dic[j]])
                
                #print(price)
                p1 = sum(price[0][0]) / len(price[0][0])
                p2 = sum(price[0][1]) / len(price[0][1])

                price_detail.append([result[i][1], dic2[result[i][2]], p1, p2])

                price_total[0] = price_total[0] + p1
                price_total[1] = price_total[1] + p2

                price = []

    # print(price_detail)
    print('\n ���� ���� ����\n===================================================================')
    print('�� ��: �ּ� %d~ �ִ� %d����' % (price_total[0], price_total[1]))
    print( '-------------------------------------------------------------------\n ���γ��� \n-------------------------------------------------------------------')
    for i in price_detail:
        print(i[0] + ' ' + i[1] + '  �ּ�%d����~ �ִ�%d���� \n' % (i[2], i[3]))
    
    return result


def image_show(i):  # plt.show 
    path = 'D:\\Desktop\\txt'.format(i)
    
    f = open(path).read()
    prt1 = navigate(f, i)[0][1]   # repair part  
    prt2 = navigate(f, i)[0][2]   # damage part
    
    fig = plt.figure(figsize=(17, 17))
    
    for j in range(i, i+2):
        try:        
            im_path = 'D:\\Desktop\\{}.jpg'.format(j)
            prt2_path = 'D:\\Desktop\\{}{}{}.jpg'.format(prt1,'_',prt2)            
                
            ax = fig.add_subplot(1, 2, 1)
            ax2 = fig.add_subplot(1, 2, 2)            
            ax.imshow(np.array(pilimg.open(im_path)))
            ax2.imshow(np.array(pilimg.open(prt2_path)))
            ax.title.set_text(i)
            plt.axis("off")
           
        except:
            pass
   
    plt.show()


image_show(1)
