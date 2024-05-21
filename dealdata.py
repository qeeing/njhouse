#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

url = "https://www.njhouse.com.cn/data/index"
response = requests.get(url)

if response.status_code == 200:
	soup = BeautifulSoup(response.text, 'html.parser')
	tables = soup.find_all('table')
	if len(tables) > 3:
		secondHandHouse = tables[3] # 获取二手房住宅数据
		
		data_list = []
		yesterday_time = datetime.now() + timedelta(days = -1)
		yesterday = yesterday_time.strftime("%Y-%m-%d")
		
		trs = secondHandHouse.find_all('tr')
		for tr in trs:
			tds = tr.find_all('td')
			if len(tds) == 5:
				data = {
					'日期': yesterday, # 昨日
					'区属': tds[0].text,
					'成交套数': tds[3].text
				}
				data_list.append(data)
else:
	print("获取网络数据出错了")
	
df = pd.DataFrame(data_list)
df.to_excel('南京二手房住宅成交数据.xlsx', index=False)
	
	