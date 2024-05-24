#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from openpyxl import load_workbook

url = "https://www.njhouse.com.cn/data/index"
response = requests.get(url)

if response.status_code == 200:
	soup = BeautifulSoup(response.text, 'html.parser')
	tables = soup.find_all('table')
	if len(tables) > 3:
		secondHandHouse = tables[3] # 获取二手房住宅数据
		
		data_list = []
		trs = secondHandHouse.find_all('tr')
		for tr in trs:
			tds = tr.find_all('td')
			if len(tds) == 5:
				data = {
					'区属': tds[0].text,
					'成交套数': tds[3].text
				}
				data_list.append(data)
		
		df = pd.DataFrame(data_list)
		
		yesterday_time = datetime.now() + timedelta(days = -1)
		yesterday = yesterday_time.strftime("%Y-%m-%d")
		sheet_name = yesterday # 昨日日期作为sheet表名
		
		excel_path = '南京二手房住宅成交数据.xlsx'
		try:
			# 非首次追加和覆盖sheet内容
			data = load_workbook(excel_path)
			with pd.ExcelWriter(excel_path, mode='a',
			if_sheet_exists='replace') as writer:
				df.to_excel(writer, sheet_name=sheet_name)
		except FileNotFoundError:
			# 首次创建
			df.to_excel(excel_path, sheet_name=sheet_name)
else:
	print("获取网络数据出错了！")
	
	
	