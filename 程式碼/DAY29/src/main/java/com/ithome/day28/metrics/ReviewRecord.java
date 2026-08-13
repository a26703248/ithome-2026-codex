package com.ithome.day28.metrics;

/**
 * 單一份草稿從生成到複核完成的一筆紀錄，是 {@link ReviewMetricsCalculator}
 * 的輸入資料。欄位對應需求書第七節提出、目前尚待回答的量測問題：
 * 撰寫時間縮短了多少、草稿被大幅修改或否決的比例、引用既有內容出錯的次數。
 */
public final class ReviewRecord {

    private final String draftId;
    private final ReviewCohort cohort;
    private final int draftToFinalMinutes;
    private final int reviewMinutes;
    private final ReviewOutcome outcome;
    private final int citationErrorCount;

    public ReviewRecord(String draftId, ReviewCohort cohort, int draftToFinalMinutes,
                         int reviewMinutes, ReviewOutcome outcome, int citationErrorCount) {
        if (draftToFinalMinutes < 0 || reviewMinutes < 0 || citationErrorCount < 0) {
            throw new IllegalArgumentException("時間與錯誤數不能為負數：" + draftId);
        }
        this.draftId = draftId;
        this.cohort = cohort;
        this.draftToFinalMinutes = draftToFinalMinutes;
        this.reviewMinutes = reviewMinutes;
        this.outcome = outcome;
        this.citationErrorCount = citationErrorCount;
    }

    public String draftId() {
        return draftId;
    }

    public ReviewCohort cohort() {
        return cohort;
    }

    public int draftToFinalMinutes() {
        return draftToFinalMinutes;
    }

    public int reviewMinutes() {
        return reviewMinutes;
    }

    public ReviewOutcome outcome() {
        return outcome;
    }

    public int citationErrorCount() {
        return citationErrorCount;
    }
}
