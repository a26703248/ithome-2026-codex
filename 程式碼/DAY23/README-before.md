# 日報服務

> 這是為 Day 22 文件練習保留的「過時版本」，內容刻意包含無法由縮小專案證明的指令，請勿當成目前操作說明。

## 啟動

```shell
java -jar target/daily-report.jar --config config/prod.yml
```

系統會在每天 08:00 產生 PDF 並寄出；部署時請沿用正式環境設定。
