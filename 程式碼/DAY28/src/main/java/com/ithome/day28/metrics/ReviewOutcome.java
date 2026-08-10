package com.ithome.day28.metrics;

/**
 * 複核人員針對一份 AI 草稿記錄的最終處置。
 * 對應需求書第四節「複核與修改介面」要求記錄的「採用、修改或否決」。
 */
public enum ReviewOutcome {
    /** 複核人員直接採用，僅有小幅或無修改。 */
    ACCEPTED,
    /** 複核人員要求大幅修改後才能定稿。 */
    MAJOR_REVISION,
    /** 複核人員否決，草稿未進入定稿流程。 */
    REJECTED
}
