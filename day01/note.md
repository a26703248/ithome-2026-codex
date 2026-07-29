# Day 1：一句「登入怪怪的」，為什麼還不能算是一張可處理的 Issue？

通常使用者回報問題時都只會依照當下看到畫面或是感受去描述問題，但往往這樣的回報缺乏大量關鍵資訊，那我們要如何從這樣混亂的回覆中得到有用的資訊呢?
以下將會透過人工先行定義來拆解這步驟，從中獲得一些關鍵資訊

## 客戶的抱怨

今天突然使用者回報一件事"登入功能怪怪的，有時候會失敗"，這一句對於我們工程師追蹤問題基本上毫無幫助

## 為什麼值得解決
模糊 Issue 會導致：
* 工程師重複詢問。 
* 修錯問題。 
* 無法重現。 
* 優先級判斷錯誤。 
* 處理時間增加。

## 第一步-issue 欄位定義
第一步我們應該先定義好填寫欄位，就像我在街上填寫問卷調查一樣，使用者需要給我們哪一些資訊?哪一些欄位是必填?哪一些選填?

| 欄位名稱                | 說明                | 必填   | 範例                               |
|---------------------|-------------------|------|----------------------------------|
| Title               | 可快速識別問題的標題        | 是    | 使用 Google 登入時偶發 500 錯誤           |
| Summary             | 問題的簡短摘要           | 是    | 部分使用者透過 Google OAuth 登入時失敗       |
| Actual  Result      | 實際發生的結果           | 是    | 頁面顯示系統錯誤                         |
| Expected Result     | 預期結果              | 是    | 使用者應成功登入並進入首頁                    |
| Reproduction Steps  | 重現步驟              | 建議必要 | 開啟登入頁、選擇 Google、完成授權             |
| Environment         | 發生環境              | 建議必要 | Production、Chrome 126、Windows 11 |
| Error Message       | 錯誤訊息或 Stack Trace | 否    | HTTP 500、NullPointerException    |
| Frequency           | 發生頻率              | 否    | 約 10 次中發生 2 次                    |
| Impact              | 影響範圍              | 是    | 使用者無法登入                          |
| Evidence            | 截圖、Log、Request ID | 否    | requestId=abc-123                |
| Missing Information | 目前缺少的資訊           | 是    | 尚未確認使用者帳號與發生時間                   |
| Status Issue        | 狀態                | 是    | Need More Information            |
| Service             | 服務/功能/模組名稱        | 是    | 入口網站                             |

### 重要原則

不要因為資料不足，就自行填入看似合理的內容。
例如原始輸入只有：

```
登入功能怪怪的。
```

就不能擅自寫成：

```
使用者在 Production 使用 Chrome 登入時發生 HTTP 500。
```

因為：

```
Production 未知。
Chrome 未知。
HTTP 500 未知。
使用者類型未知。
```

正確方式是填入：

```
Environment: 未知
Error Message: 未提供
Missing Information:
- 發生環境
- 登入方式
- 錯誤訊息
- 發生時間
- 重現步驟
```

這項規則會成為後續 Prompt Engineering 的重要基礎。

## 第二步-人工判讀

## 結論