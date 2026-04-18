from backend.compiler import SLCCompiler
from backend.lom import _mock_execution_plan

plan = _mock_execution_plan("test", {"emotion": "neutral"})
raw_data = [{"category": "Food", "amount": 10}, {"category": "Food", "amount": 20}, {"category": "Transport", "amount": 15}]

compiler = SLCCompiler()
result = compiler.compile(plan, raw_data)
print("HTML generated successfully. Length:", len(result))
