import csv
file_path = '/Users/liji/Desktop/231126BigData_DongBoShi/data/assignment_wosparse/qje2014_2023.txt'
import csv
import re

# 初始化所有表格的列和数据存储
tables = {
    'table1': {'columns': ['UT', 'PY', 'SO', 'SN', 'DI', 'IS', 'VL'], 'data': []},
    'table2': {'columns': ['UT', 'AB'], 'data': []},
    'table3': {'columns': ['UT', 'TI'], 'data': []},
    'table4': {'columns': ['UT', 'UT_author', 'full_name', 'family_name', 'given_name', 'author_order'],
               'data': []},
    'table5': {'columns': ['UT', 'full_name', 'author_order', 'affiliation'], 'data': []},
    'table6': {'columns': ['UT', 'CR'], 'data': []}
}

# 对于table 4：分割作者姓名，提取作者顺序
def split_author_names(ut, author_str):
    authors = author_str.split('; ')
    if ut is None or author_str is None:
        return []  # 返回一个空列表以防止空数据
    return [{
        'UT_author': ut + '_' + author.strip(),   # 复合主键
        'UT': ut,
        'full_name': author.strip(),
        'family_name': author.split(', ')[0],
        'given_name': ' '.join(author.split(', ')[1:]),
        'author_order': i + 1
    }
    for i, author in enumerate(authors) if author]

# 对于table 5：提取作者单位
def split_af(ut, author_str, affiliation_str):
    authors = split_author_names(ut, author_str)
    author_affiliations_data = {}

    affiliations = affiliation_str.split('; ')
    for aff in affiliations:
        author_names = re.findall(r'\[(.*?)\]', aff)
        affiliation_cleaned = re.sub(r'\[.*?\]', '', aff).strip()

        if author_names:
            author_names = author_names[0].split('; ')
            for author_name in author_names:
                author_name = author_name.strip()
                # 将单位信息聚合到对应的作者名下
                if author_name in author_affiliations_data:
                    author_affiliations_data[author_name].add(affiliation_cleaned)
                else:
                    author_affiliations_data[author_name] = {affiliation_cleaned}
        else:
            # 如果单位是共享的，则为所有作者添加这个单位
            for author in authors:
                if author['full_name'] in author_affiliations_data:
                    author_affiliations_data[author['full_name']].add(affiliation_cleaned)
                else:
                    author_affiliations_data[author['full_name']] = {affiliation_cleaned}

    # 生成最终的作者与单位信息列表
    final_data = []
    for author in authors:
        final_data.append({
            'UT': ut,
            'full_name': author['full_name'],
            'author_order': author['author_order'],
            'affiliation': '; '.join(author_affiliations_data.get(author['full_name'], []))
        })

    return final_data

# 读取文件并提取数据
with open(file_path, 'r') as file:
    reader = csv.DictReader(file, delimiter='\t')
    for row in reader:
        for name, table in tables.items():
            if name == 'table4':
                table['data'].extend(split_author_names(row['UT'], row['AF']))
            elif name == 'table5':
                table['data'].extend(split_af(row['UT'], row['AF'], row['C1']))
            else:
                entry = {col: row.get(col, '') for col in table['columns']}
                table['data'].append(entry)

# 写入CSV文件
def write_csv(file_name, table):
    with open(file_name, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=table['columns'])
        writer.writeheader()
        writer.writerows(table['data'])

# 写入所有表格到CSV文件
for name, table in tables.items():
    write_csv(f'{name}.csv', table)
