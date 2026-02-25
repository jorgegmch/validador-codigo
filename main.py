import os, json
from core.flow import Flow, Node
from evaluator.runner import SafeRunner
from llm.gemini_client import GeminiClient

class LoaderNode(Node):
    def exec(self, state):
        prob_name = state.get("prob_name")
        with open(f"problems/{prob_name}/problem.json") as f: state.set("p_data", json.load(f))
        with open(f"problems/{prob_name}/tests.json") as f: state.set("t_data", json.load(f))
        with open(state.get("sol_path")) as f: state.set("u_code", f.read())
        return "ExecNode"

class ExecNode(Node):
    def exec(self, state):
        runner = SafeRunner()
        p, tests, sol = state.get("p_data"), state.get("t_data")["tests"], state.get("sol_path")
        all_passed = True
        results = []
        for t in tests:
            ok, res, err = runner.run(sol, p["entrypoint"], t["input"])
            passed = ok and res == t["expected"]
            if not passed: all_passed = False
            results.append({"in": t["input"], "out": res if ok else err, "pass": passed})
        state.set("all_passed", all_passed)
        state.set("results", results)
        return "LLMNode"

class LLMNode(Node):
    def exec(self, state):
        print("--- Consultando IA ---")
        client = GeminiClient()
        feedback = client.evaluate_code(state.get("u_code"), state.get("p_data")["description"], state.get("all_passed"))
        print(f"\n🚀 RESULTADOS:\nTests Pasados: {state.get('all_passed')}\nScore: {feedback.get('Score')}/100")
        print(f"Feedback: {feedback.get('Correctness')}")
        return None

if __name__ == "__main__":
    # Asegurar que existan los archivos __init__.py
    for d in ["core", "llm", "evaluator", "nodes"]:
        if os.path.exists(d): open(f"{d}/__init__.py", "a").close()

    flow = Flow("Validator")
    flow.add_node(LoaderNode("LoaderNode"), is_start=True)
    flow.add_node(ExecNode("ExecNode"))
    flow.add_node(LLMNode("LLMNode"))
    
    flow.state.set("prob_name", "two_sum")
    flow.state.set("sol_path", "problems/two_sum/solution.py")
    flow.run()