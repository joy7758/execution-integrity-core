from core import ExecutionIntegrityCore

ei = ExecutionIntegrityCore()

ei.record("search", {"query": "AI regulation"}, {"result": "Found 12 documents"}, ts=1700000000.0)
ei.record("calculate", {"expression": "2+2"}, {"result": 4}, ts=1700000001.0)

print("Verification before tamper:", ei.verify())

exported_files = []
exported_files.append(ei.export(filename="execution_log.json", exported_at=1700000002.0))
exported_files.append(ei.export())

ei.chain[0]["output"] = {"result": "Modified result"}

print("Verification after tamper:", ei.verify())
print("Exported files:", exported_files)
