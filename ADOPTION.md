# Adoption

## 这是什么
Execution Integrity Core 是一个最小执行完整性结构：把每次执行事件串成哈希链，并导出可复现的 JSON，让第三方只拿导出文件也能独立验证是否被篡改。

## 最快体验
```bash
python3 example.py
python3 verify_export.py execution_log.json
bash scripts/selfcheck.sh
```

## 怎么接入你自己的 agent/tool
1. 创建 `ExecutionIntegrityCore` 实例。
2. 每次工具调用后执行 `record(action, input, output, ts=...)`。
3. 任务结束时执行 `export(filename="execution_log.json", exported_at=...)`。
4. 分发 `execution_log.json` 给审计方或协作方。
5. 第三方运行 `verify_export.py execution_log.json` 独立验证。

## 常见问题
### 为什么要 deterministic
因为可复现才能对账；同样输入得到一致导出，第三方才能稳定复核。

### 为什么篡改会失败
每条记录都包含前一条哈希，改动任意字段都会导致当前条目的哈希重算不一致，链校验立即失败。

### 我能不能换 hash 算法
未来可能支持；当前版本先固定 `sha256`，保证实现和验证路径简单一致。
