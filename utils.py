
import re
import torch
from sentence_transformers import util
from prompt import embedder, corpus_embeddings, table_schema, corpus, In_context_prompt


# 检索问句答案可能存在表结构
def retrieval_related_table(input_prompt, input, history=None, top_k=3, is_moss=False, In_context_prompt=""):
    # 计算输入问题的嵌入向量
    query_embedding = embedder.encode(input, convert_to_tensor=True) 
    # 计算与6张表的表名的相似度
    cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0] 
    # 取前top_k个表名
    top_results = torch.topk(cos_scores, k=top_k) 

    table_nums = 0 
    for score, idx in zip(top_results[0], top_results[1]):
        # 阈值过滤
        if score > 0.45:
            table_nums += 1
            input_prompt += table_schema[corpus[idx]]
        input_prompt += "上下文结束\n"

    # In-Context Learning
    if is_moss:
        In_context_prompt = In_context_prompt.replace("问: ", ": ").replace("答:", "<eoh>")
    
    if table_nums >= 2 and not history:
        input_prompt += In_context_prompt
    
    return input_prompt

def obtain_sql(response):
    response = re.split("```|\n\n", response)
    for text in response:
        if "SELECT" in text:
            response = text
            break
    else:
        response = response[0]
    response = response.replace("\n", " ").replace("``", "").replace("`", "").strip()
    response = re.sub(' +',' ', response)
    return response


def execute_sql(response, chatbot, dboperate):
    print(f"Debug: Response in execute_sql: {response}")  # 打印 response
    print(f"Debug: Chatbot before SQL execution: {chatbot}")  # 打印 chatbot 列表状态

    if "SELECT" in response:
        try:
            sql_status = "sql语句执行成功,结果如下:"
            sql_result = dboperate.query_data(response)
            sql_result = str(sql_result)
        except Exception as e:
            sql_status = "sql语句执行失败"
            sql_result = str(e)
        
        # 确保 chatbot 列表不为空
        if not chatbot:
            chatbot.append(("", ""))
        
        print(f"Debug: Chatbot before updating: {chatbot}")  # 打印 chatbot 列表状态

        chatbot[-1] = (chatbot[-1][0], 
                       chatbot[-1][1] + "\n\n" + "====================" + "\n\n" + sql_status + "\n\n" + sql_result)
        
        print(f"Debug: Chatbot after updating: {chatbot}")  # 打印更新后的 chatbot 列表状态

    return chatbot