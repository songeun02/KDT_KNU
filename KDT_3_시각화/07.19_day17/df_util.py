# Series / DataFrame에서 사용되는 사용자 정의 함수들

# 데이터 확인
# - 기본정보

# df.info()
# print(f'[index] : {df.index}')
# print(f'[columns] : {df.columns}')

# df2.info()
# print(f'[index] : {df2.index}')
# print(f'[columns] : {df2.columns}')


# doc string : 함수에 대한 설명 적어야 함

# ------------------------------------------------------------------

# 함수 기능 : DF의 기본정보와 속성 확인 기능
# 함수 이름 : checkDataFrame
# 매개변수 : DataFrame 인스턴스 변수명, DataFrame 인스턴스 이름
# 리턴값 / 반환값 : 없음

def checkDataFrame(object, name): # 또는 df_instance 적어도 됨
  print(f'\n [{name}]')
  object.info()
  print(f'[index] : {object.index}')
  print(f'[columns] : {object.columns}')
  print(f'[ndim] : {object.ndim}')

