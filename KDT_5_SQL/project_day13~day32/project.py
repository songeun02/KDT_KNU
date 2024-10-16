import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import csv
import koreanize_matplotlib


import pymysql.cursors

year = list(range(2014,2024))
print(year)

conn=pymysql.connect(host='localhost', user='root',password='1216',db='fuel',charset='utf8')

cur=conn.cursor(pymysql.cursors.DictCursor)
cur.execute('select * from csi_file')
rows=cur.fetchall()

csi_df=pd.DataFrame(rows)


# # 생활형편전망, 향후경기전망, 소비지출전망
# plt.plot(csi_df['년도'],csi_df.iloc[:,1:4], 'o-',label=csi_df.columns[1:4])
# plt.title('년도별 소비자 동향 지수')
# plt.xlabel('년도')
# plt.ylabel('소비자 동향 지수')
# plt.xticks([2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023])

# plt.grid(True)
# plt.legend(loc='upper right', bbox_to_anchor=(1.32, 1))
# plt.tight_layout()
# plt.show()

# # 소비자 동향 지수 세부사항 
# plt.plot(csi_df['년도'],csi_df.iloc[:,4:-1], 'o-',label=csi_df.columns[4:-1])
# plt.title('년도별 소비자 동향 지수 세부 사항')
# plt.xlabel('년도')
# plt.ylabel('소비자 동향 지수')
# plt.grid(True)
# plt.xticks([2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023])
# plt.legend(loc='upper right', bbox_to_anchor=(1.32, 1))
# plt.tight_layout()
# plt.show()


# conn=pymysql.connect(host='localhost', user='root',password='1216',db='fuel',charset='utf8')

# cur=conn.cursor(pymysql.cursors.DictCursor)
# cur.execute('select * from travel')
# rows=cur.fetchall()

# travel_df=pd.DataFrame(rows)

# # travel 
# plt.plot(travel_df['년도'],travel_df.iloc[:,1], 'o-',label='여행비 지출전망 CSI')
# plt.plot(travel_df['년도'],travel_df.iloc[:,2], 'o-',label='항공기 기름 가격')
# plt.title('년도별 항공기 기름 가격과 여행비 지출전망')
# plt.xlabel('년도')
# plt.ylabel('항공기와 여행')
# plt.xticks([2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023])
# plt.grid(True)
# plt.legend(loc='upper right', bbox_to_anchor=(1.32, 1))
# plt.tight_layout()
# plt.show()

# cur.close()
# conn.close()

# 최종 결론 

conn=pymysql.connect(host='localhost', user='root',password='1216',db='fuel',charset='utf8')

cur=conn.cursor(pymysql.cursors.DictCursor)
cur.execute('select * from total')
rows=cur.fetchall()
total_df=pd.DataFrame(rows)

# # total 
# plt.plot(total_df['년도'],total_df.iloc[:,1:], 'o-',label=['PPI 전체','CPI 전체','CSI 전체','BSI 전체'])
# plt.title('물가상승률 분석')
# plt.xlabel('년도')
# plt.ylabel('물가상승률')
# plt.xticks([2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023])
# plt.grid(True)
# plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1))
# plt.tight_layout()
# plt.show()

# # PPI, CPI
# plt.plot(total_df['년도'],total_df.iloc[:,1:3], 'o-',label=['PPI 전체','CPI 전체'])
# plt.title('물가상승률 분석')
# plt.xlabel('년도')
# plt.ylabel('물가상승률')
# plt.xticks([2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023])
# plt.grid(True)
# plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1))
# plt.tight_layout()
# plt.show()


# CSI, BSI
plt.plot(total_df['년도'],total_df.iloc[:,3:], 'o-',label=['CSI 전체','BSI 전체'])
plt.title('물가상승률 분석')
plt.xlabel('년도')
plt.ylabel('물가상승률')
plt.xticks([2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023])
plt.grid(True)
plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1))
plt.tight_layout()
plt.show()



# # 유류비


# conn=pymysql.connect(host='localhost', user='root',password='1216',db='fuel',charset='utf8')

# cur=conn.cursor(pymysql.cursors.DictCursor)
# cur.execute('select * from fuel_file')
# rows=cur.fetchall()
# fuel_df=pd.DataFrame(rows)

# # total 
# plt.plot(fuel_df['년도'],fuel_df.iloc[:,1:], 'o-',label=fuel_df.columns[1:])
# plt.title('유류비 분석')
# plt.xlabel('년도')
# plt.ylabel('유류비')
# plt.xticks([2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023])
# plt.grid(True)
# plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1))
# plt.tight_layout()
# plt.show()