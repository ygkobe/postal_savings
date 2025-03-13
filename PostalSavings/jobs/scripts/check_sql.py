# 普通文本
text = "安子草泥马 "

# 转换为 Unicode 转义序列
unicode_escaped = text.encode('unicode_escape').decode('utf-8')

print(unicode_escaped)
