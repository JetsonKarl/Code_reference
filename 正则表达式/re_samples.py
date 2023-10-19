import re

pattern = 'abc'
match = re.search(pattern,'sdaoiabcoad')

print("找到匹配的内容:", match)

if match:
    print("找到匹配的内容:", match.group())
    print("匹配的位置:", match.span())
else:
    print("未找到匹配的内容")