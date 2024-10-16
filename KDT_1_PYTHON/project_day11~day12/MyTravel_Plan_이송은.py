import ast
from datetime import datetime, timedelta

def manu():
    print()
    print('---------------My Travel Plan-----------------')
    print('-============================================-')
    print('- 1  내 여행 전체 일정 확인하기              -')
    print('- 2. 여행일정 상세보기 및 편집               -')
    print('- 3. 여행 일정 추가                          -')
    print('- 4. 방문했던 여행지와 날짜 및 방문여부 확인 -')
    print('- 5. 종료                                    -')
    print('-============================================-')
    print('----------------------------------------------')


def manu1():
    print()
    print('---[ ONE. 여행 전체 일정 확인 ]---')
    print('-================================-')
    print('-    1. 년도별 전체 일정 확인    -')
    print('-    2. 월별 일정 확인           -')
    print('-================================-')


def manu2():
    print()
    print('----[ TWO. 여행일정 조회 및 편집 ]---')
    print('-===================================-')
    print('-       1. 여행 년도/월/일 조회     -')
    print('-       2. 여행일정 삭제            -')
    print('-       3. 여행일정 수정            -')
    print('-===================================-')


def manu2_3():
    print()
    print('---[ TWO - 3. 여행일정 수정 ]---')
    print('-==============================-')
    print('-     1. 여행 종료 날짜        -')
    print('-     2. 함께 여행간 사람      -')
    print('-     3. 장소                  -')
    print('-     4. 기록하고 싶은 내용    -')
    print('-===================================-')


def manu3():
    print()
    print('-----[ THREE. 여행 일정 추가 ]----')
    print('-================================-')



def manu4():
    print()
    print('--[ FOUR. 방문한 여행지 정보 및 여부확인]--')
    print('-=========================================-')
    print('-      1. 방문한 여행지와 방문일 확인     -')
    print('-      2. 여행지 방문 여부 확인           -')
    print('-=========================================-')


def print_plan(index, var):
    print()
    while(1):
        line=f.readline()
        if line[:index]==var:
            print(line)
        elif not line: break
    f.close()


def modify_plan(start_date,modify_index,modify_content,slice,index):

    with open(FILENAME, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(FILENAME, 'w', encoding='utf-8') as file:
        for line in lines:
            if line[:slice] == year_month_day_2_2:
                parts = line.strip().split('/')
                parts[index] = modify_content
                line = '/'.join(parts) + '\n'
            file.write(line)


def date_range(start, end):
    start = datetime.strptime(start, "%Y-%m-%d") # 날짜와 시간(datetime)을 문자열로 출력하려면 strftime, 날짜와 시간 형식의 문자열을 datetime으로 변환
    end = datetime.strptime(end, "%Y-%m-%d")
    dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end-start).days+1)] # 두 날짜 차이 계산 
    return dates


def modify_plan_dict(modify_index, modify_content):
    with open(DICTFILENAME, mode='r', encoding='utf-8') as file:
        travel_data = file.readlines()

    for idx, line in enumerate(travel_data):
        if year_month_day_2_2 in line:
            travel_dict = eval(line.strip(','))
            travel_dict[modify_index] = modify_content
            updated_line = ','+str(travel_dict)
            travel_data[idx] = updated_line
            break         
    with open(DICTFILENAME, mode='w', encoding='utf-8') as file:
        file.writelines(travel_data)
           

FILENAME='mytravel.txt'
DICTFILENAME='mytravel_plan.txt'
DATEFILENAME='date.txt'

mytravel_plan=[]

with open(DICTFILENAME, 'r', encoding='utf-8') as file:
    for line in file:
        clean_line = line.strip().strip(",")
        travel_dict = ast.literal_eval(clean_line) # literal_eval : 딕셔너리였던 데이터를 ""감싼 문자열을 dict로 변환
        if type(travel_dict)==tuple:
            mytravel_plan.append(travel_dict[0]) # 튜플로 들어가는 것 따로 처리
        else:
            mytravel_plan.append(travel_dict)


date=[]

with open(DATEFILENAME, 'r', encoding='utf-8') as file1:
    for line1 in file1:
        clean_line1 = line1.strip()
        date_list1 = ast.literal_eval(clean_line1)
        date.append(date_list1)


while(1):

    manu()

    with open(FILENAME, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    sorted_lines = sorted(lines, key=lambda line: line.split('/')[0])

    with open(FILENAME, 'w', encoding='utf-8') as file:
        for line in sorted_lines:
            file.write(line)


    choose_manu=input("원하시는 옵션의 번호를 입력하시오 :")

    if choose_manu=='1':
        manu1()
        f=open(FILENAME, mode='r', encoding='utf-8')

        choose_manu1 = input("여행 전체 일정 확인에서 필요한 옵션의 번호를 입력하시오 : ")
        if choose_manu1=='1':
            year_1_1=input("여행 시작 일정을 확인하고자 하는 년도를 입력해주세요 (ex) 2024)) : ")
            print_plan(4,year_1_1)
        elif choose_manu1=='2':
            year_1_2=input("여행 시작 일정을 확인하고자 하는 년도와 월을 입력해주세요 (ex) 2024-07) : ")
            print_plan(7,year_1_2)

        else:
            print('옵션에 있는 번호만 입력해주세요 ')

    elif choose_manu=='2':
        manu2()
        f=open(FILENAME, mode='r', encoding='utf-8')
        df=open(DICTFILENAME, mode='r', encoding='utf-8')

        choose_manu2=input("여행 일정 조회 및 편집에서 필요한 옵션의 번호를 입력하시오 : ")
        if choose_manu2=='1':
            year_month_day_2_1=input("조회 하고 싶은 여행 시작 년도-월-일을 입력하시오 (ex) 2024-07-10) : ")
            print_plan(10,year_month_day_2_1)
        elif choose_manu2=='2':
            year_month_day_2_2=input("삭제하고자 하는 여행 시작 년도-월-일을 입력하시오 (ex) 2024-07-10) :")

            mytravel_plan[:] = [plan for plan in mytravel_plan if plan['start_date'] != year_month_day_2_2]

            with open(FILENAME, 'r', encoding='utf-8') as file:
                lines = [line for line in file if year_month_day_2_2 not in line]


            with open(FILENAME, 'w', encoding='utf-8') as file:
                for line in lines:
                    file.write(line)

            with open(DICTFILENAME, 'r', encoding='utf-8') as file:
                lines = [line for line in file if year_month_day_2_2 not in line]


            with open(DICTFILENAME, 'w', encoding='utf-8') as file:
                for line in lines:
                    file.write(line)

            with open(DATEFILENAME, 'r', encoding='utf-8') as file:
                lines = [line for line in file if year_month_day_2_2 not in line]


            with open(DATEFILENAME, 'w', encoding='utf-8') as file:
                for line in lines:
                    file.write(line)



        elif choose_manu2=='3':
            year_month_day_2_2=input("수정하고자 하는 여행의 시작 년도-월-일을 입력하시오 (ex) 2024-07-10) :")

            manu2_3()

            choose_manu_2_3=input("선택한 일정에서 수정하고 싶은 사항의 번호를 입력하시오 : ")


            if choose_manu_2_3=='1':
                modify_fin_date=input("수정할 여행 종료 년도-월-일-일을 입력하시오 (ex) 2024-07-10) :")
                modify_plan(year_month_day_2_2,'fin_date',modify_fin_date,10,1)

                with open(DATEFILENAME, 'r', encoding='utf-8') as file:
                    lines = [line for line in file if year_month_day_2_2 not in line]


                ymdfile=open(DATEFILENAME,mode='w',encoding='utf-8')
                for line in lines:
                    ymdfile.write(line)
                print(date_range(year_month_day_2_2,modify_fin_date),file=ymdfile)
                ymdfile.close()

                modify_plan_dict('fin_date',modify_fin_date)

                
            elif choose_manu_2_3=='2':
                modify_with_person=input("수정할 함께 여행간 사람을 입력하시오 : ")
                modify_plan(year_month_day_2_2,'with_persion',modify_with_person,10,2)

            elif choose_manu_2_3=='3':
                modify_place=input("수정할 여행간 여행지를 지역명만 입력하시오 ex)부산, 제주도 : ")
                modify_plan(year_month_day_2_2,'place',modify_place,10,3)

                modify_plan_dict('place',modify_place)


            elif choose_manu_2_3=='4':
                modify_comment=input("수정할 기록하고 싶은 내용을 입력하시오 : ")
                modify_plan(year_month_day_2_2,'comment',modify_comment,10,4)
            else:
                print('옵션에 있는 번호만 입력해주세요 ')

        else:
            print('옵션에 있는 번호만 입력해주세요 ')

    elif choose_manu=='3':
        manu3()
        f=open(FILENAME, mode='a', encoding='utf-8')

        year_month_day_3_start=input("추가하고자 하는 여행 시작 년도/월/일을 입력하시오 (ex) 2024-07-10) :")

        isexist=False
        for day in date:
            if year_month_day_3_start in day:
                print('해당 날짜는 이미 여행중인 날짜 입니다. ')
                isexist=True
                break

        if isexist==False:

            year_month_day_3_fin=input("추가하고자 하는 여행 종료 년도/월/일을 입력하시오 (ex) 2024-07-10) :")
            with_person=input("함께 여행간 사람들을 작성하시오 : ")
            place=input("여행간 장소에 대해 지역명만 입력하시오 ex)부산, 제주도 : ")
            comment=input("기록하고 싶은 내용을 입력하시오 : ")

            print(year_month_day_3_start,year_month_day_3_fin,with_person,place,comment, sep='/',file=f)
            f.close()

            df=open(DICTFILENAME,mode='a',encoding='utf-8')
            print(',',{'start_date':year_month_day_3_start, 'fin_date':year_month_day_3_fin, 'with_person':with_person,'place':place,'comment':comment},sep='',file=df)
            df.close()

            ymdfile=open(DATEFILENAME,mode='a',encoding='utf-8')
            print(date_range(year_month_day_3_start,year_month_day_3_fin),file=ymdfile)
            ymdfile.close()


    elif choose_manu=='4':
        manu4()
        choose_manu4 = input("방문한 여행지 정보 및 여부 확인에서 필요한 옵션의 번호를 입력하시오 : ")
        if choose_manu4=='1':
            for plan in mytravel_plan:
                print(plan['start_date'], plan['fin_date'],plan['place'])
        elif choose_manu4=='2':
            search_place=input("방문 여부를 확인하고 싶은 여행지를 지역명만 입력하시오 ex)부산, 제주도 : ")
            print()

            found=False

            for plan in mytravel_plan:
                if search_place in plan['place']:
                    if not found:
                        print(f'{search_place}은/는 방문했던 장소입니다. ')
                        found=True
                    print(plan['start_date'], plan['fin_date'], plan['place'])

            if not found:
                print(f'{search_place}은/는 방문하지 않았던 장소입니다. ')

        else:
            print('옵션에 있는 번호만 입력해주세요 ')

    elif choose_manu=='5':
        print('My Travel Plan이 종료됩니다.')
        break

    else:
        print('옵션에 있는 번호만 입력해주세요 ')
