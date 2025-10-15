
import asyncio
import json
from app.deep_search import deep_search

async def main():
    result = await deep_search("hosni raissi", "person")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(main())