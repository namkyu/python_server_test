import httpx

async def fetch_google():

    async with httpx.AsyncClient() as client:
        response = await client.get("https://www.google.com")
        return {"status_code": response.status_code, "content": response.text[:200]}  # 일부 내용만 반환
