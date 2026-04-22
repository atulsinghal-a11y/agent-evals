import json
from datetime import datetime

from utils.loader import load_json
from agent.call_agent import create_thread, run_agent
# from agent.call_agent import call_agent
from evaluators.judge_llm import judge


def run():
    thread_id = create_thread()
    print(f"Using thread: {thread_id}")
    tests = load_json("datasets/skill_prism_tests.json")
    results = []

    for test in tests:
        print(f"Running test: {test['id']}")
        # agent_response = call_agent(test["prompt"])
        agent_response = run_agent(thread_id, test["prompt"])
        evaluation = judge(test, agent_response)

        results.append({
            "id": test["id"],
            "prompt": test["prompt"],
            "agent_response": agent_response,
            "evaluation": evaluation
        })

    filename = f"results/run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved → {filename}")


if __name__ == "__main__":
    run()