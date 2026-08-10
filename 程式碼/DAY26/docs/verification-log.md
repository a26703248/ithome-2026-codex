# Day 26 驗證紀錄

草擬日期：2026-08-10

## 環境（待作者本機執行後補齊）

- 建議：Windows 11、OpenJDK 17、Apache Maven 3.8 以上、JUnit Jupiter 5.13.4（比照 Day 24／25 的既有環境）。
- 本次草擬是在沒有 Maven／JDK 編譯工具的沙盒環境中完成，只能以人工方式覆核程式邏輯與測試設計，
  尚未實際執行 `mvn clean test`。這一點與 Day 24／25 已附上真實建置輸出不同，作者發布前必須在本機
  重新執行並貼上實際結果，不可只沿用本文件的預期說明。

## 待執行指令

```shell
cd 程式碼/DAY26
mvn clean test
```

## 測試設計與預期結果（人工覆核，非實際執行輸出）

`AccessGovernanceGuardTest` 共 5 項測試：

1. `engineerCannotUseRealCustomerScansAsTestData`：工程師申請存取限閱等級的客戶掃描檔，預期拋出 `SecurityException`，且稽核紀錄中該筆事件的 `approved` 為 `false`。
2. `complianceCanAccessRestrictedDataWithPurpose`：法遵／資安角色申請存取限閱等級資料且填寫用途，預期核准並記錄。
3. `techLeadCanAccessInternalButNotRestricted`：技術主管可存取內部等級，但申請限閱等級應被拒絕。
4. `purposeMustNotBeBlankEvenForPublicData`：用途欄位空白時，即使是公開等級也要拋出 `IllegalArgumentException`。
5. `deniedAttemptsStillAppearInAuditTrail`：確認被拒絕的請求仍會寫入稽核紀錄，而不是被靜默忽略。

預期結果為 `Tests run: 5, Failures: 0, Errors: 0, Skipped: 0`，但這是依程式邏輯推演的預期值，不是
實際建置輸出；作者需在本機執行後，把真實的 `BUILD SUCCESS` 或失敗訊息貼回本文件。

## 證據邊界

即使本機執行通過，結果也只涵蓋 `AccessGovernanceGuard` 的記憶體內單元測試：角色與分級的核准
判斷、稽核紀錄留存。未驗證真正的檔案系統存取、單一登入、正式稽核儲存、事故通報流程、供應商
條款變更偵測，或跨部門實際核定的資料分級標準。這些項目仍列在
[`governance-inventory.md`](governance-inventory.md) 的待角色確認清單。
