# Day 11｜安裝與設定 Codex：先讓一個入口通過驗收

![Day 11 封面：先選入口，再完成最小驗收](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day11/day11-01-cover.png)

Day 10 我用差異、命令與測試紀錄判斷 Codex 是否完成任務。今天往前補一題：要從哪個入口開始？我的環境是 Windows 11、Java 17、Maven 3.8.1，專案沿用 Day 10。這次不裝齊所有介面，只要求一條「登入、開啟專案、讀懂結構」的流程通過驗收。

## CLI、IDE 擴充功能與 Codex cloud，差在工作發生的位置

命令列介面（Command-Line Interface，CLI）使用本機終端機；整合開發環境（Integrated Development Environment，IDE）擴充功能會帶入開啟的檔案與選取範圍；Codex cloud 則在隔離的雲端環境執行。三者不是功能排行榜，而是三種工作距離。

| 選擇條件 | CLI | IDE 擴充功能 | Codex cloud |
|---|---|---|---|
| 我會在何時使用 | 習慣在終端機連續操作 | 需要緊貼目前程式與選取範圍 | 想把本機留給其他工作 |
| 專案位置 | 本機工作目錄 | IDE 開啟的本機專案 | 已授權的 GitHub 儲存庫 |
| 命令執行位置 | 本機沙箱 | 本機沙箱，可依介面交辦較長任務 | 隔離的雲端環境 |
| 驗收方式 | 命令、退出碼、差異與測試 | 編輯器旁的摘要、差異與後續對話 | 工作紀錄、摘要、差異與拉取請求 |
| 先確認的限制 | 作業系統、路徑與權限 | IDE 支援、擴充功能與團隊政策 | GitHub 權限、相依工具、變數與密鑰 |

![三種 Codex 入口的工作位置與驗收證據](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day11/day11-02-entry-choice.png)

這次我不碰編輯器整合，也不新增 GitHub 授權，先把 Windows 本機的啟動問題單獨留下。日後真的更換入口，我才會依當時使用的開發工具與團隊政策設定；發布當日也要重查官方支援範圍。

## 我的安裝檢查沒有一次過關

我原本想先驗證 CLI，因此在專案根目錄執行四個低風險檢查：

```powershell
java -version
mvn -version
Get-Command codex -All
codex --version
```

Java 與 Maven 都回報版本，但 Maven 輸出前也有一行 `Access is denied`。PowerShell 能解析到桌面 App 內附的 `codex.exe`，`codex --version` 卻無法啟動。找得到同名檔案，不代表 CLI 能用。我沒有重裝 Node.js 或改系統路徑，只標記 CLI 尚未通過，再回官方 Windows 安裝說明核對來源。

![從官方來源、版本檢查到登入與專案的四個關卡](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day11/day11-03-install-checkpoint.png)

我改用 Day 03 已安裝、已登入的 Codex 桌面 App，開啟同一個工作區。通過驗收的是桌面 App，不是 CLI；若只接受 CLI，就該停到 `codex --version` 正常回報。安裝完成不能只看套件清單，還要確認入口、帳號、專案與權限。

## 第一個任務先讀，不急著讓 Codex 改碼

我先用 Day 10 專案做冒煙測試，也就是確認最基本的讀取流程。實際提示詞是：

```text
先不要變更工作區。請從 pom.xml 與 src 目錄判斷這個專案需要哪個
Java 版本、如何啟動測試；每個結論都附上檔案路徑。
證據不足就停止並列出缺口。
```

Codex 從 `pom.xml` 找到 Java 17 與 JUnit 5.13.4，測試位於 `src/test/java`，可用 `mvn test` 執行。限定 `程式碼/DAY10` 的 `git status --short` 與 `git diff` 都沒有輸出，表示範圍內沒有變更。「不要變更」只是提示詞；要加上技術限制，我會使用唯讀（`read-only`）權限模式。它預設阻擋寫入，命令也需要核准，所以還要確認核准政策。

![第一個讀取型任務的提示、檢查與證據](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day11/day11-04-readonly-validation.png)

## 排錯時，一次只確認一層

我依序檢查執行檔、登入、專案、沙箱、工具與網路。`Access is denied` 先歸在啟動或權限層，單憑訊息不能定位根因。JUnit 已執行且出現 Day 10 那類斷言失敗，才進入程式與測試行為層；探索或組態錯誤另分一類。

![Codex 最小設定的分層排錯順序](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day11/day11-05-troubleshooting.png)

## 小結：先證明入口可用

我不以「安裝過」作為完成條件，而是要求入口、帳號、專案、權限與讀取任務都留下證據。這次桌面 App 通過，CLI 沒有；結果不漂亮，但邊界很清楚。Day 12 會把 `AGENTS.md` 與目錄慣例放進專案，讓 Codex 讀得懂團隊的工作規則。

## 參考資料

- [OpenAI：Codex CLI](https://learn.chatgpt.com/docs/codex/cli)
- [OpenAI：Codex IDE extension](https://learn.chatgpt.com/docs/codex/ide)
- [OpenAI：Codex cloud](https://learn.chatgpt.com/docs/cloud)
- [OpenAI：ChatGPT desktop app](https://learn.chatgpt.com/docs/app)
- [OpenAI：Sandbox](https://learn.chatgpt.com/docs/sandboxing)
- [Apache Maven：Maven in 5 Minutes](https://maven.apache.org/guides/getting-started/maven-in-five-minutes.html)
- [JUnit 5.13.4 User Guide](https://docs.junit.org/5.13.4/user-guide/index.html)
