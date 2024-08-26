from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Prompt import system_prompt
from typing import Optional

# 引入之前定义的类
from model import LLM, VectorStoreIndex, EmbeddingModel

app = FastAPI()

# 实例化模型
embed_model_path = './AI-ModelScope/bge-small-zh-v1___5'
embed_model = EmbeddingModel(embed_model_path)

model_path = './IEITYuan/Yuan2-2B-Mars-hf'
llm = LLM(model_path)

class Query(BaseModel):
    question: str
    document_path: Optional[str] = None

# 使用系统Prompt，不使用RAG
@app.post("/generate_with_prompt/")
def generate_answer_with_prompt(query: Query):
    try:
        input_prompt = f'{system_prompt["content"]}\n以下是需要你评价的文章：{query.question}\最后请记住你的角色{system_prompt["content"]}\n请输出你的评分'
        response = llm.generate(input_prompt, context=[])  # 不使用RAG，直接生成
        return {"answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 使用RAG，不使用系统Prompt
@app.post("/generate_with_rag/")
def generate_answer_with_rag(query: Query):
    try:
        document_path = "./" + query.document_path
        index = VectorStoreIndex(document_path, embed_model)
        
        context = index.query(query.question)
        response = llm.generate(query.question, context)
        return {"answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

