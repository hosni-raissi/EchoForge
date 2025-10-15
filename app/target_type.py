#!/usr/bin/env python3

from utils.gemini_llm import call_gemini
import asyncio
from lib.prompts import TARGET_TYPE_PROMPT
from lib.variables import TARGET_TYPES

async def analyse_target(target: str) -> None:
    FULL_PROMPT = f"{TARGET_TYPE_PROMPT}\n\nTARGET:\n{target}"
    target_type = await asyncio.to_thread(call_gemini, FULL_PROMPT)
    print(f"Target: {target}  =>  Type: {target_type}")
    return target_type if target_type in TARGET_TYPES else "other"




