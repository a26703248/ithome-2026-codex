package com.ithome.day28.metrics;

import java.util.List;
import java.util.Objects;

/**
 * 將一批 {@link ReviewRecord} 彙總成 {@link ReviewMetrics}，作為需求書第七節
 * 「如何量測是否真的縮短撰寫時間，以及草稿被大幅修改或否決的比例」的量測工具。
 * 只做彙總計算，不含資料庫存取或報表輸出。
 */
public final class ReviewMetricsCalculator {

    /**
     * 彙總一批複核紀錄。清單不可為空——空清單代表沒有樣本，不該除以零硬算出
     * 一個看似正常的平均值，寧可讓呼叫端先發現「沒有資料」這個問題。
     *
     * @param records 同一批（例如同一個 cohort）的複核紀錄
     * @throws IllegalArgumentException 若 records 為 null 或空清單
     */
    public ReviewMetrics calculate(List<ReviewRecord> records) {
        Objects.requireNonNull(records, "records 不能為 null");
        if (records.isEmpty()) {
            throw new IllegalArgumentException("records 不能為空清單，沒有樣本無法計算指標");
        }

        int sampleSize = records.size();
        double avgDraftToFinal = records.stream()
                .mapToInt(ReviewRecord::draftToFinalMinutes)
                .average()
                .orElseThrow();
        double avgReview = records.stream()
                .mapToInt(ReviewRecord::reviewMinutes)
                .average()
                .orElseThrow();
        long majorRevisionOrReject = records.stream()
                .filter(r -> r.outcome() == ReviewOutcome.MAJOR_REVISION
                        || r.outcome() == ReviewOutcome.REJECTED)
                .count();
        long completed = records.stream()
                .filter(r -> r.outcome() != ReviewOutcome.REJECTED)
                .count();
        double avgCitationError = records.stream()
                .mapToInt(ReviewRecord::citationErrorCount)
                .average()
                .orElseThrow();

        return new ReviewMetrics(
                sampleSize,
                avgDraftToFinal,
                avgReview,
                (double) majorRevisionOrReject / sampleSize,
                (double) completed / sampleSize,
                avgCitationError
        );
    }
}
