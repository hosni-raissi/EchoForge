#!/usr/bin/env python3
#EchoForge
import asyncio
import json
from unittest import result
from app.target_type import analyse_target
from utils.tor_manager import run_tor_manager
from app.deep_search import deep_search
async def main():
    #await analyse_target(test_target)
    #run_tor_manager()
    # Usage
    result = await deep_search("hosni raissi", "person", max_results=100)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(main())