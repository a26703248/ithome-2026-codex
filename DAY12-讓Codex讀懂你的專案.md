# Day 12｜讓 Codex 讀懂你的專案：把默契寫成可執行規則

![Day 12 封面：讓 Codex 先讀懂專案規則](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day12/day12-01-cover.png)

Day 11 的批次任務明確指定要讀 `pom.xml`、查看 `src`、附上路徑，證據不足就停止；每次重寫這些要求卻很容易漏掉。回頭看 Day 11 的 Java 專案，`pom.xml` 能告訴 Codex 使用 Java 17，卻不會說「不能為了修軟體缺陷（bug）改測試」或「Maven 下載失敗時不能宣稱測試通過」。規則只留在提示詞或腦中，Codex 就只能猜。

![能讀到檔案，不等於知道團隊規則](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day12/day12-02-hidden-rules.png)

## 我先整理五層上下文

我不會把整份資料塞給 Codex，而是先問：哪些資訊會改變它的動作、驗證或回報？這次整理成五層：

| 層次 | Codex 需要知道什麼 | Day 11 專案的內容 |
|---|---|---|
| 任務目標 | 要解決的行為與不處理的範圍 | 修正批次計數，不做無關重構 |
| 目錄與模組 | 程式、測試與文件在哪裡 | `src/main/java`、`src/test/java`、`docs` |
| 建置與測試 | 可重現的命令與成功條件 | Java 17、Maven、`mvn clean test` |
| 編碼與安全規則 | 禁止事項與何時停下 | 不改測試與 `pom.xml`；新增依賴先確認 |
| 完成與回報 | 交付時要留下的證據 | 變更檔案、命令、結果與未驗證風險 |

![專案上下文的五個層次](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day12/day12-03-context-layers.png)

任務本身仍放在當次提示詞；穩定、會重複使用的專案規則才寫進 `AGENTS.md`。這樣不會把一次性的 bug 描述誤當成長期規範。

## `AGENTS.md` 怎麼被套用？

依 OpenAI 官方文件，Codex 每次執行啟動時建立一次指令鏈；終端機通常每個工作階段載入一次。它先在 Codex home 依序檢查全域的 `AGENTS.override.md` 與 `AGENTS.md`，取第一個非空檔，再從專案根目錄走到目前工作目錄。同一目錄中，override 檔優先；越靠近工作目錄的規則越晚加入，可覆蓋上層要求。

![從專案根目錄到工作目錄的指令鏈](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day12/day12-04-instruction-chain.png)

例如根目錄規定 Java 修改要跑單元測試，`services/reporting/AGENTS.override.md` 再指定模組命令。以該目錄或其子目錄啟動 Codex，例如執行 `codex --cd services/reporting`，兩層規則都會載入；若從根目錄啟動，之後讀到子目錄檔案也不會載入該處規則。同一層若兩種檔案並存，只載入 override 檔。

## 我的最小可用 `AGENTS.md`

我把 Day 11 反覆出現的限制寫成下列版本：

```markdown
# Repository instructions

## Scope
- 本規範適用於此目錄下的所有檔案。

## Project
- 使用 Java 17 與 Maven。
- 正式程式碼位於 src/main/java；測試程式碼位於 src/test/java。

## Change boundaries
- 修 bug 時，除非任務明確允許，否則不要修改測試檔案或 pom.xml。
- 新增相依套件、刪除檔案，或變更公開 API 之前，請先詢問。

## Verification
- 修改 Java 程式碼後，執行 mvn clean test。
- 若指令無法執行，請回報確切的錯誤訊息，不要宣稱測試已通過。

## Completion report
- 列出已變更的檔案、執行過的指令、測試結果，以及尚存的風險。
```

完整的 [Day 12 AGENTS.md](https://github.com/a26703248/ithome-2026-codex/blob/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY12/AGENTS.md) 是下載範本，不會套用到相鄰的 DAY11。第一輪先不複製；第二輪才把它放到 DAY11 的 `pom.xml` 同一層、重新啟動 Codex，再交付相同任務。規則都要能由命令、差異或回報驗證，不放口號、密碼、內部主機與付費文件。

## 加入規則後，我怎麼驗收？

兩輪都要記錄讀檔、假設與測試，再看加入規則後是否改善結果。回覆變短不等於上下文有效。

| 觀察項目 | 我會檢查的證據 |
|---|---|
| 錯誤假設 | 是否仍想修改測試或建置設定 |
| 不必要讀檔 | 是否把搜尋限制在相關模組 |
| 追問內容 | 是否只追問衝突或缺少的決策 |
| 測試選擇 | 是否執行規定命令並辨認環境錯誤 |
| 完成回報 | 是否列出差異、結果與剩餘風險 |

![加入規則後仍要用證據驗收](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day12/day12-05-verification.png)

`AGENTS.md` 是工作指示，不是安全機制。它不能取代唯讀模式、沙箱、核准政策、持續整合（Continuous Integration，CI）或人工審查。規則也要像程式碼一樣維護；指令過長、互相矛盾或已經過期，反而會讓 Codex 選錯依據。

## 小結：把默契留在 Codex 找得到的位置

我留下的不是更多背景，而是會改變動作的規則、可執行的驗證，以及失敗時的停止條件；Day 13 會把這份範本放進實作專案根目錄，再將一張問題單交給 Codex，走完定位、修正、測試與回報。

## 參考資料

- [OpenAI：Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Apache Maven：Maven in 5 Minutes](https://maven.apache.org/guides/getting-started/maven-in-five-minutes.html)
