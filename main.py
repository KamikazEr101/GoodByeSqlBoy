from fastapi import FastAPI
from router.nl_to_sql import router
from config import settings
from api.nl_to_sql import convert_nl_to_sql
app = FastAPI(
    title="NL to SQL API",
    description="API for converting natural language queries to SQL statements",
    version="1.0.0"
)

app.include_router(router)

async def run_on_console():
    while True:
        nl = input("请输入自然语言的查询语句 (输入exit退出): \n")
        if nl.upper() == 'EXIT': break
        result = await convert_nl_to_sql(nl)
        print('\n\n',"#" * 5, 'result =',result, "#" * 5,'\n\n')

# 整体程序的入口, 开启后, 对  http://localhost:8000/api/v1/nl2sql  发送post请求, 请求体规定为json格式, 属性只有一个 -> "query"(自然语言)
if __name__ == "__main__":
    if settings.CONSOLE_INPUT:
        import asyncio
        asyncio.run(run_on_console())
    else:
        import uvicorn
        uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)



