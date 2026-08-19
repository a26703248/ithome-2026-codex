# Day 16｜Codex 與 Git 工作流整合：把修改整理成可審查的交付

![Day 16 封面：把修改整理成可審查的交付](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day16/day16-01-cover.png)

Day 15 劃出可核准範圍後，Day 13 的日期修正仍停在工作目錄。測試通過，不代表團隊看得出修改目的或原有內容。這次我用分支、程式差異（diff）、提交紀錄（commit）與拉取請求（Pull Request，PR）草稿，把結果整理成可審查的交付。

## Git 是證據鏈，不是完成按鈕

我把 Git 當成證據鏈：分支隔離任務，diff 顯示修改，commit 保存意圖，PR 承載問題、證據與風險。它們是檢查點，不會取代測試或人工合併決定。

| Git 節點 | 應留下的證據 | 我會檢查什麼 |
|---|---|---|
| 分支 | 可對應議題的名稱與起點 | 是否從正確基底建立 |
| 索引與工作目錄 | 已暫存（staged）、未暫存與未追蹤清單 | 是否混入他人修改 |
| commit | 單一意圖、檔案範圍與訊息 | 是否只包含本任務 |
| PR | 問題、做法、測試、風險與未完成事項 | 審查者能否重現判斷 |

![Git 證據鏈：從任務分支到 PR 草稿](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day16/day16-02-evidence-chain.png)

依 OpenAI 官方文件，桌面 App 的審查窗格（review pane）可能同時包含 Codex 的修改與原有的未提交修改，所以我先用 `git status` 對照。要看未提交內容或基底分支差異，再從桌面 App、命令列介面（Command-Line Interface，CLI）或整合開發環境（Integrated Development Environment，IDE）擴充啟動 `/review`；結束後重看狀態，避免把審查誤認成修正。

## 從確認起點走到一個 commit

我進入 `程式碼/DAY13/`，確認狀態後建立任務分支。未提交修改會留在新分支，不會因切換分支自動改變歸屬：

```text
git status --short
git branch --show-current
git switch -c codex/day13-same-day-range
mvn clean test
git diff --check
git diff --stat
```

我檢查完整 diff：主程式只修正日期條件，測試只新增同日起訖回傳 1 的案例。本案例沒有保存 `/review` 結果，因此不列為完成證據，只示範人工確認後的暫存步驟：

```text
git add -- src/main/java/com/ithome/day13/report/ReportRangeService.java
git add -- src/test/java/com/ithome/day13/report/ReportRangeServiceTest.java
git diff --cached --check
git diff --cached
git commit -m "fix: accept same-day report ranges"
```

![提交前只審查並暫存本任務的兩個檔案](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day16/day16-03-scoped-diff.png)

commit 訊息描述行為，不寫「Codex 修好了」。提交後我用 `git show --stat --oneline HEAD` 與 `git status --short` 核對檔案規模和剩餘變更；`README.md` 仍在，證明它沒有被混入。

## 工作目錄不乾淨，就先辨識擁有者

若 `git status --short` 顯示 `README.md` 已修改，我先看 diff。與任務無關就保留，只暫存日期修正的兩個檔案；若同一個 Java 檔已有不明修改，我就停下來確認，不擅自 reset、restore 或 stash。

![既有修改與本任務變更分流，不混進同一個 commit](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day16/day16-04-dirty-worktree.png)

自動提交前仍要人工看已暫存的 diff；路徑選錯，可能夾帶無關檔案或不該進版控的祕密。

## PR 草稿要讓審查者不用猜

我先寫 PR 說明，尚未推送分支，也沒有在 GitHub 建立 Draft PR。草稿列出問題、修改、測試、風險與未完成事項：`mvn clean test` 共 5 項通過，但網頁、資料庫與單日報表輸出尚未驗證。完整內容見 [DAY16 PR 草稿](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E7%A8%8B%E5%BC%8F%E7%A2%BC/DAY16/pr-draft.md)。

每項驗收條件都要對到命令、結果或待辦；環境若阻擋測試，就寫「未執行」與原因，不把預期包裝成證據。

![PR 草稿把問題、修改、驗證與風險放在同一頁](https://raw.githubusercontent.com/a26703248/ithome-2026-codex/main/%E5%9C%96%E6%AA%94/Day16/day16-05-pr-draft.png)

改用 Codex cloud 時，我先為已連接 GitHub 的專案設定雲端環境，讓任務與本機分開。結束後仍要核對摘要與 diff，符合範圍才建立 PR。推送、建 PR 與合併都是外部動作；未取得授權，我只準備 commit 或 PR 文字。

## 小結：交付完成，要能重建判斷過程

今天我用分支隔離範圍，以 diff、測試、commit 與 PR 草稿留下證據。修改可追溯，才有資格談自動化。Day 17 會先用一個故事，帶出接手老舊「日報服務」系統時的第一印象，可以讓我們知道當面對古人遺留下來的天書時該如何處理。

## 參考資料

- [OpenAI：Code review](https://learn.chatgpt.com/docs/code-review)
- [OpenAI：Codex cloud](https://learn.chatgpt.com/docs/cloud)
- [OpenAI：Review GitHub pull requests with Codex](https://learn.chatgpt.com/docs/third-party/github)
