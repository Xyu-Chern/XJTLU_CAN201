import re

def find_numbers_and_locations():
    number_list = []
    location_list = []
    user_input = input("Pls input a string: ")

    number_pattern = re.compile(r'\d+\.\d+|\d+')  
    print(number_pattern)  # re.compile(r'\d+\.\d+|\d+') 
    matches = number_pattern.finditer(user_input)
    # matches 是一个由 re.finditer() 返回的迭代器对象。
    # finditer() 方法用于在字符串中查找所有与正则表达式模式匹配的子字符串，并返回一个包含所有匹配项的迭代器。
    # 每一个匹配项都被表示为一个 Match 对象，它包含匹配的具体信息，如匹配的文本内容、位置等。
    # 与 findall() 方法不同，finditer() 不仅返回匹配的文本，还可以提供关于匹配项的更多详细信息，例如开始和结束位置等。

    # 每个 Match 对象表示一个正则表达式的匹配结果，它提供了以下常用方法和属性：
        # group()：返回匹配的子字符串。
        # start()：返回匹配子字符串的开始位置。
        # end()：返回匹配子字符串的结束位置（不包含该位置的字符）。
        # span()：返回匹配子字符串的 (start, end) 元组。

    for match in matches:
        number = float(match.group()) if '.' in match.group() else int(match.group())
        number_list.append(number)

        start = match.start()
        length = len(match.group())
        location_list.append([start, length])

    # 对数字列表进行升序排序
    sorted_indices = sorted(range(len(number_list)), key=lambda i: number_list[i])
    number_list = [number_list[i] for i in sorted_indices]
    location_list = [location_list[i] for i in sorted_indices]

    # 输出结果
    print("number_list =", number_list)
    print("location_list =", location_list)

# 调用函数
find_numbers_and_locations()
