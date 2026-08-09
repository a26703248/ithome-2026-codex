# Day 23 安全與品質縮小案例

這個 Spring Boot 縮小專案示範報表建立端點的輸入驗證、身分與授權分離、日誌最小化，以及套件通知的可達性判讀。它不代表正式日報服務的完整程式或部署設定。

```shell
mvn clean test
mvn dependency:tree "-Dincludes=org.apache.pdfbox:pdfbox"
```

正式環境的 API 閘道、限流、佇列、祕密管理、監控與完整相依清單均未在本專案中提供，需另行確認。
