package com.ithome.day28.metrics;

/**
 * 一筆複核紀錄屬於哪一批對照組。
 * BASELINE：沒有 AI 輔助生成系統時，人工從零撰寫草稿再送複核。
 * AI_ASSISTED：由 AI 輔助生成系統產出草稿後，再送複核。
 */
public enum ReviewCohort {
    BASELINE,
    AI_ASSISTED
}
