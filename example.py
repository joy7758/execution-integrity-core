from core import ExecutionIntegrityCore

ei = ExecutionIntegrityCore()

ei.record("search", {"query": "AI regulation"}, {"result": "Found 12 documents"})
ei.record("calculate", {"expression": "2+2"}, {"result": 4})

print("Verification before tamper:", ei.verify())

# 篡改第一条记录
ei.chain[0]["output"] = {"result": "Modified result"}

print("Verification after tamper:", ei.verify())

ei.export()
