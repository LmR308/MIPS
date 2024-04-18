import requests
from bs4 import BeautifulSoup
import pandas as pd

# 获取网页内容
url = 'http://mipsconverter.com/opcodes.html'  # 替换为你要爬取的网页地址
response = requests.get(url)
html_content = response.text

# 使用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 找到表格并解析数据
table = soup.find('table')
table_rows = table.find_all('tr')

# 提取表头
headers = [th.text.strip() for th in table_rows[2].find_all('td')]

# 提取表格数据
data = []
for tr in table_rows[1:]:
    row_data = [td.text.strip() for td in tr.find_all('td')]
    data.append(row_data)

# 将数据转换为 DataFrame
df = pd.DataFrame(data, columns=headers)

# 将数据写入 Excel 文件
df.to_excel('table_data.xlsx', index=False)
