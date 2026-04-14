import os
from openai import OpenAI
from dotenv import load_dotenv
from utils.loader import load_text

load_dotenv()

client = OpenAI()

JUDGE_PROMPT = load_text("prompts/judge_prompt.txt")

def judge(test_case, agent_response):

    prompt = JUDGE_PROMPT.format(
        prompt=test_case["prompt"],
        expected_intent=test_case["expected_intent"],
        must_contain=test_case["must_contain"],
        agent_response=agent_response
    )

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return res.choices[0].message.content