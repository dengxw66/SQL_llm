# GLMSQL
基于ChatGLM-6B,实现nl2sql，直连数据库并返回查询结果
目前仅支持MYSQL语法,后续支持多数据库语法查询

## 🎬 开始
```
pip install -r requirements.txt
```

```
# 新建文件夹
mkdir DB
mkdir logs
```

```
# 修改基础数据和prompt
config.yaml
prompt.py
utils.py
```

```
# 生成本地数据库+插入数据
local_database.ipynb
```

```
# 基于GLM生成SQL
main_gui.ipynb(GUI界面版)
main_direct.ipynb(直接输出版)
```

```
# 添加日志文件：
data/daily.txt
# 基于GLM使用RAG替换关键词检索
main_RAG.ipynb
```



## 🔍 查询示例
```
问: 请帮我查询所有的人员姓名
答: SELECT name FROM people_info;
问: 请帮我查询所有男性的人员姓名和联系电话
答: SELECT name, phone_number FROM people_info WHERE gender = 1;
问: 请帮我查询学历为大学及以上的人员姓名
答: SELECT name FROM people_info WHERE education_level >= 6;
问: 请帮我查询居住地址在北京市的所有人员姓名和身份证号码
答: SELECT name, id_number FROM people_info WHERE residential_address LIKE '%北京市%';
问: 请帮我查询所有识别记录的时间和姓名
答: SELECT time, name FROM person_recognition;
问: 请帮我查询摄像头编号为 cam001 拍摄到的所有人员姓名
答: SELECT name FROM person_recognition WHERE camera_id = 'cam001';
问: 请帮我查询识别时间在2023年1月1日之后的所有人员姓名
答: SELECT name FROM person_recognition WHERE time > '2023-01-01 00:00:00';
问: 请帮我查询张三在识别中的大图和小图
答: SELECT big_image, small_image FROM person_recognition WHERE name = '张三';
```

## 致谢/参考：
- [ChatSQL](https://github.com/cubenlp/ChatSQL) 作为baseline进行修改
