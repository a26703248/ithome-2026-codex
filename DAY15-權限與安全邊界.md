# Day 15｜權限與安全邊界：核准前先看懂影響範圍

![Day 15 封面：核准前先看懂影響範圍](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day15/day15-01-cover.png)

Day 14 重跑 Maven 測試時，Maven 下載建置外掛的連線被 `Permission denied: connect` 阻擋。我沒有直接放寬權限，而是把 Git 差異檢查、Maven 測試與外部部署要求並排，逐一確認會碰到的資源再決定。

## 沙箱與核准政策，是兩道不同的門

沙箱（sandbox）限制命令可寫哪些路徑、能否使用網路；核准政策（approval policy）決定 Codex 何時必須停下來提出核准請求。前者是圍牆，後者是確認點。出現核准提示，不代表操作已經安全。

![沙箱與核准政策共同形成安全邊界](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day15/day15-02-two-layers.png)

依 2026 年 8 月 8 日的 OpenAI 官方文件，本機 Codex 採 `Auto` 組合（`workspace-write` 搭配 `on-request`）時，可在工作區內讀檔、修改與執行例行指令，命令預設不能連網；修改工作區外檔案或讓命令連網時會要求核准。非版本控制或尚未信任的資料夾可能從 `read-only` 開始。Codex cloud 在隔離容器執行，設定階段可連網安裝依賴，代理階段預設離線。

## 我先把權限拆成五個面向

「可以改專案」不等於「可以讀取憑證」，「可以跑 Maven」也不等於「可以任意連網」。我先依 Day 14 的驗收範圍畫出界線：

| 權限面向 | 本次可接受範圍 | 我會拒絕的狀況 |
|---|---|---|
| 讀取檔案 | `程式碼/DAY13/` 與 `AGENTS.md` 等專案指示檔 | 要求讀取家目錄、金鑰或無關專案 |
| 修改檔案 | 工作區內的 Java 原始碼與測試 | 改測試斷言、批次覆寫無關檔案 |
| 執行指令 | Git 差異與指定 Maven 測試 | 指令被包在看不懂的下載腳本裡 |
| 網路存取 | 經確認的相依套件來源 | 不明網域、上傳內容或永久全開 |
| 使用憑證 | 本案例不需要 | 顯示、匯出或寫入任何權杖 |

![五個權限面向要分開判斷](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day15/day15-03-permission-surfaces.png)

敏感資料即使位於沙箱允許的路徑，也不代表適合交給 Codex。沙箱限制可觸及範圍，不會替我判斷資料政策。

## 三個請求，我做三種決定

第一個請求是執行 `git diff -- 程式碼/DAY13`。它只讀取差異，不需網路也不改檔，我確認工作目錄後放行。

第二個請求是重跑 `mvn -Dtest=ReportRangeServiceTest test`。Maven 還沒取得建置外掛，JUnit 尚未啟動。我核對 `pom.xml`、Maven 設定與下載網域，再限縮連線；若只能持續開放網路，我會改到已預載依賴的環境執行。

第三個請求來自我準備的模擬供應商說明 `vendor-repro.md`：內容要求新增外部套件庫設定，接著執行 `mvn deploy`。本次驗收只需單元測試，部署會改變設定並上傳成品。我拒絕執行，改請對方提供不含憑證的最小重現專案。

![三個操作請求分別放行、縮小與拒絕](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day15/day15-04-three-decisions.png)

## 外部內容先當證據，不當命令

Issue（議題）、README（專案說明檔）與測試資料都可能混入操作要求，我只把它們當成待查證的證據。若內容把任務從測試推向部署，或要求增加寫入與連線範圍，我會停在差異檢查，核對交付來源後再決定下一步。

![遇到衝突指令時先停止並回到可信來源](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day15/day15-05-untrusted-input.png)

這次 Maven 只需要下載，我會記錄連線端點與取得的檔案；本機若啟用網路代理，只允許必要網域。Codex cloud 還可限制網路請求方法。做不到同等限縮時，我改用離線快取或內部套件庫。

## 小結：核准的是具體動作，不是對 Codex 的信任

今天我只核准看得懂的命令與資源範圍；沙箱和核准能減少意外，不能替代需求判斷。Day 16 會實際建立 Git 分支、commit 與 Pull Request 草稿，檢查每次修改能否留下可追查、可還原的紀錄。

## 參考資料

- [OpenAI：Agent approvals & security](https://learn.chatgpt.com/docs/agent-approvals-security)
- [OpenAI：Sandbox](https://learn.chatgpt.com/docs/sandboxing)
- [OpenAI：Agent internet access](https://learn.chatgpt.com/docs/cloud/internet-access)
