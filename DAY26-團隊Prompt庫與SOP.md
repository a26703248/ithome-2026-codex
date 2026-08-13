# Day 26｜團隊提示詞（Prompt）庫與標準作業程序（Standard Operating Procedure，SOP）

![Day 26 封面：好提示詞要離開聊天紀錄，進入可驗證流程](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day26/day26-01-cover.png)

Day 25 把跨角色交接整理成可驗證紀錄後，我收到一句交辦：「沿用上次最好用的提示詞。」問題是，那一版只在同事的聊天紀錄裡。沒人說得出當時用了哪些來源、逐字沿用怎麼算，也不知道誰核准過。換人只能重試，效果變差也找不到基準。

## 先把提示詞當成工作資產

我不看收藏數量，只檢查每份是否寫清用途、必要輸入、禁止事項、固定輸出、驗收方式與維護人。缺一項，就只是難以重跑的個人技巧。

![個人聊天與團隊資產](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day26/day26-02-chat-to-asset.png)

| 資產欄位 | 本篇案例的決定 |
|---|---|
| 名稱與版本 | `draft-from-sources` 0.1.0 |
| 必要輸入 | 文件目的、允許資料等級、核定分級表、來源與沿用規則 |
| 禁止事項 | 跨客戶資料、真實密碼或權杖、自動核准與發布 |
| 固定輸出 | 草稿標示、來源對照、逐字沿用檢查、待確認事項 |
| 通過方式 | 人工核對來源與敏感資料，另用一致算法重算比例 |
| 維護角色 | 產品經理與品質保證代表共同核准版本 |

Codex 執行工作前會讀取 `AGENTS.md`，適合保存跨任務規則。本篇的[提示詞檔案](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY26/prompt/draft-from-sources.md)可交給 ChatGPT 討論草稿，或讓 Codex 處理專案檔案；產出都走同一套複核。流程穩定後，我會把固定做法寫進技能（skill）的指示檔，另附執行時需要查閱的材料；只有步驟確實需要自動化時，才加入腳本。

![AI 草稿生成提示詞的必要欄位與固定輸出](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day26/day26-03-prompt-contract.png)

## 我把「不確定」寫進提示詞

需求書尚未決定既有內容可逐字沿用多少。我沒有替法遵填一個數字，而是把 `reuse_rule` 設為必要輸入；值仍是「待確認」時，提示詞只能回報缺口，不產生正文。每個可驗證主張還要標出來源識別碼，沒有根據就寫「待確認」，輸出一律標示「草稿｜尚未複核」。

```text
若 reuse_rule 尚未核定，停止生成正文。
每個可驗證主張在句末標示 [source_id]。
不得把輸出稱為定稿、核准文件或正式決策。
```

## 用合成資料做人工走查

我沒有呼叫正式模型，只用不含客戶內容的[四組合成案例](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY26/docs/test-cases.md)人工走查。P-01 檢查主張與來源；P-02 依本案例規則判斷通用術語。P-03 缺少沿用規則就停止。P-04 另附示範分級表；正式分級仍待核定，沒有規則也要停止。

![四組合成案例人工走查正常輸出、引用判斷與停止條件](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day26/day26-04-test-matrix.png)

[走查紀錄](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY26/docs/verification-log.md)顯示四組判斷分支符合預期，不代表模型測試通過。模型自報比例仍可能算錯，正式流程必須重算；模型、來源格式或提示詞一變，也要重跑案例。

## 人工走查後，Prompt 還要接進 SOP

我的 [SOP](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY26/docs/sop.md) 指定申請人準備來源、執行人鎖定版本、複核人檢查來源與敏感資料。任一項失敗就保留原因並否決；提示詞改版後必須重跑案例。

![提示詞接入申請、執行、人工複核與版本維護流程](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day26/day26-05-sop-flow.png)

共用資產也會放大過時規則。我會保留負責人、版本、驗證日期與限制；沒有維護人或基準案例，就不進現行清單。

## 小結：能被否決，才有機會被維護

這次我確認，個人做法補上輸入、拒絕規則、驗收證據與管理責任後，才適合列入團隊清單。下一篇會從組織角度檢查資料分級、存取權限、稽核留痕與合規責任。

## 參考資料

- [OpenAI：Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [OpenAI：Build skills](https://learn.chatgpt.com/docs/build-skills)
- [AI 輔助生成系統需求書](https://github.com/a26703248/ithome-2026-codex/blob/main/%E6%A1%88%E4%BE%8B/AI%E8%BC%94%E5%8A%A9%E7%94%9F%E6%88%90%E7%B3%BB%E7%B5%B1-%E9%9C%80%E6%B1%82%E6%9B%B8.md)
