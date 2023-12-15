# Assignment8_wosparse

assignment_wosparse 路径中的文件qje2014_2023.txt包含了过去十年间发表在QJE杂志上的所有论文，请使用python编程将该数据拆分成若个关联表格。

原始数据中各列表达的含义参考：https://images.webofknowledge.com/WOKRS5132R4.2/help/zh_CN/WOS/hs_wos_fieldtags.html 

1. 第一张表为论文的基本信息，表格的主键为ut论文入藏号，至少包括论文的发表年份、杂志、issn、doi、issue、volume等信息

2. 第二张表为论文的摘要信息，表格的主键为ut论文入藏号，包括入藏号、摘要

3. 第二张表为论文的题目，表格的主键为ut论文入藏号，包括入藏号、标题

4. 第四张表为论文的作者，表格的主键为ut论文入藏号与作者，包括入藏号、作者全名、作者的family name、givenname、作者顺序；

5. 第五张表为论文的作者与单位，表格的主键为ut论文入藏号与作者，包括入藏号、作者全名、作者顺序、单位affiliation地址全文、单位署名顺序；

6. 第六张表位论文的参考文献信息，表格的主键为ut与参考文献条目，包括ut与参考文献两列
