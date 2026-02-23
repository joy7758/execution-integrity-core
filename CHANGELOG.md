# Changelog

## 0.1.2
- `export` 支持可选 `filename`，未传时自动生成 `execution_log.<timestamp>.json`，默认避免覆盖历史导出。
- 新增 `scripts/selfcheck.sh`，一条命令完成示例运行、导出验证和基础测试。
- 新增 `tests/test_export_verify.py`，覆盖导出验证 PASS 与篡改后 FAIL 的最小流程。

## 0.1.1
- 导出格式升级为带封套结构，新增 `spec`、`version`、`exported_at`、`hash_alg`、`chain` 顶层字段。
- 新增独立验证器 `verify_export.py`，第三方仅凭导出 JSON 即可核验链完整性。

## 0.1.0
- 提供最小哈希链模型：记录执行事件、导出 JSON、链式完整性校验。
