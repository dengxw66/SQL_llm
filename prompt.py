"""
Text2SQL机器人·Prompt
"""
import numpy as np
from sentence_transformers import SentenceTransformer, util
from utility.utils import config_dict as DB_CONFIG
from local_database import db_operate

embedder = SentenceTransformer('/data1/dxw_data/llm/paraphrase-multilingual-MiniLM-L12-v2')

chatbot_prompt ="""
你是一个文本转SQL的生成器，你的主要目标是尽可能的协助用户，将输入的文本转换为正确的SQL语句。
上下文开始
表名和表字段来自以下表：
表1: people_info
字段1: name(姓名),字段2: gender(性别),字段3: ethnicity(名族),字段4: education_level(学历),字段5: id_number(身份证号码),字段6: phone_number(联系电话),字段7: registered_address(户籍地址),字段8: residential_address(居住地址),字段9: category(人员类别),字段10: judgment_level(研判等级),字段11: village(乡村),字段12: community(社区)
表2: camera_info
字段1: camera_model(摄像头型号),字段2: coordinates(经纬度),字段3: osd(摄像头OSD)
表3: person_recognition
字段1: time(时间),字段2: name(姓名),字段3: camera_id(摄像头编号),字段4: big_image(大图),字段5: small_image(小图),字段6: vl_output(VL输出),字段7: glm_output(GLM输出)
表4: event_record
字段1: time(时间),字段2: camera_id(摄像头编号),字段3: name(姓名),字段4: event_type(事件类型),字段5: big_image(大图),字段6: small_image(小图),字段7: vl_output(VL输出),字段8: glm_output(GLM输出)
表5: vehicle_info
字段1: plate_number(车牌号),字段2: owner_name(车主姓名),字段3: color(颜色),字段4: vehicle_type(车辆类型),字段5: brand_model(品牌型号),字段6: usage(使用性质),字段7: vin(车辆识别代号),字段8: engine_number(发动机号)
表6: vehicle_recognition
字段1: time(时间),字段2: plate_number(车牌),字段3: camera_id(摄像头编号),字段4: big_image(大图),字段5: small_image(小图),字段6: vl_output(VL输出),字段7: glm_output(GLM输出)
上下文结束
问: 请帮我查询所有的人员姓名
答: SELECT name FROM people_info
问: 请帮我查询所有男性的人员姓名和联系电话
答: SELECT name, phone_number FROM people_info WHERE gender = 1
问: 文本转SQL: <user input>
答:
"""

In_context_prompt ="""
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
"""
query_template = """问: <user_input>
答: 
"""

# yaml解析
TABLE = DB_CONFIG["TABLE"]
table_schema = {}

for table_name in TABLE.keys():
    # table描述拼接
    table_info = """"""
    table_info += "表名:" + table_name + "\n"
    table_info += "字段:"
    for idx, filed in enumerate(TABLE[table_name]["field"].items()):
        if idx == len(TABLE[table_name]["field"].items()) - 1:
            table_info += filed[0] + "(" + filed[1][0] + ")"
        else:
            table_info += filed[0] + "(" + filed[1][0] + "),"

    table_schema[TABLE[table_name]["info"]] = table_info

# 获取表的描述信息
corpus = list(table_schema.keys())

# 向量化
corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)