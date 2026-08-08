package com.ithome.day08.tutor;

import org.springframework.scheduling.annotation.Scheduled;

public final class DailyReportScheduler {

    private final DailyReportImporter importer;

    public DailyReportScheduler(DailyReportImporter importer) {
        this.importer = importer;
    }

    @Scheduled(
            cron = "${daily-import.cron:0 0 9 * * *}",
            zone = "${daily-import.zone:Asia/Taipei}")
    public void importDailyReport() {
        importer.importDailyReport();
    }
}
