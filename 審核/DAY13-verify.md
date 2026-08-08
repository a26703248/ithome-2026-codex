# DAY13 發布前驗證

## 已完成的內容檢查

- [x] 正文排除五行圖片後約 916 個中文字與中文標點；包含圖片替代文字約 976 字，落在 900～1,100 字目標內。
- [x] 文章使用繁體中文，開頭承接 Day 12 的 `AGENTS.md`，結尾銜接 Day 14 的工作紀錄、diff 與測試輸出。
- [x] 案例已改為獨立設計的 `ReportRangeService` 同日起訖缺陷，沒有沿用草稿「AI 建議」中的 `CheckoutService` 空折扣碼案例。
- [x] 已說明 JUnit 5、回歸測試、`-Dtest`、`mvn clean test` 與公開方法簽章，讓第一次操作的讀者能跟上。
- [x] 已誠實註明沒有純人工計時對照，不宣稱節省分鐘數。
- [x] 五張圖片皆為 1600×900（16:9），圖片文字已目視檢查。
- [x] 五張圖片均使用 `raw.githubusercontent.com` 網址，且每張圖片獨立成行。
- [x] OpenAI Prompting、Codex CLI、JUnit 5.13.4 與 Maven Surefire 官方參考頁均已於 2026-08-08 開啟核對。

## 程式與測試證據

- [x] `before-fix/` 執行 `mvn clean test`：Tests run 4、Failures 0、Errors 0、Skipped 0，BUILD SUCCESS。
- [x] `reproduction/` 執行 `mvn -Dtest=ReportRangeServiceTest test`：Tests run 5、Failures 0、Errors 1、Skipped 0，BUILD FAILURE。
- [x] 重現例外為 `IllegalArgumentException`，訊息為 `endDate must not be before startDate`，堆疊落在 `ReportRangeService.java:14`。
- [x] 最終版本執行 `mvn clean test`：Tests run 5、Failures 0、Errors 0、Skipped 0，BUILD SUCCESS。
- [x] 主程式只將 `!endDate.isAfter(startDate)` 改為 `endDate.isBefore(startDate)`；測試只新增 `sameDayRangeContainsOneDay()`。
- [x] 三份 `pom.xml` 的 SHA-256 均為 `EE2D2AC72498D43329C78A8F3D34F0766C1A4B595C094C73CE2AC607CE7AE660`。
- [x] 未驗證項目已明列為網頁操作、資料庫、端對端報表與實際輸出內容。

## 三角色審查

- [x] 著作權合規：通過。未涉及 ISO／CNS、法律或 OWASP；外部文件只列名稱與連結，沒有直接摘錄；草稿 AI 案例與欄位骨架均已移除。
- [x] 事實正確性：通過。三階段 POM、程式差異、測試數字、例外行號、圖片文字與官方參考資料均已核對。
- [x] 讀者清晰度與規範：通過。流程涵蓋讀檔、假設、重現、修正與重測；字數、標點、標題層級、前後篇銜接及圖片規格均符合要求。

## 發布當日仍需由作者確認

- [ ] 發布前重新開啟 [OpenAI Prompting](https://learn.chatgpt.com/docs/prompting) 與 [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)，確認介面與功能敘述沒有更新。
- [ ] 推送圖檔後逐一開啟文章中的五個 raw 圖片網址，確認公開頁面能載入。
- [ ] 確認第一人稱敘述符合作者願意公開分享的實際操作經驗。
