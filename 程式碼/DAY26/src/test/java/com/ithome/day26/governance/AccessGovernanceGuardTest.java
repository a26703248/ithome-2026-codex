package com.ithome.day26.governance;

import org.junit.jupiter.api.Test;

import java.util.List;

import static com.ithome.day26.governance.AccessGovernanceGuard.Classification.INTERNAL;
import static com.ithome.day26.governance.AccessGovernanceGuard.Classification.PUBLIC;
import static com.ithome.day26.governance.AccessGovernanceGuard.Classification.RESTRICTED;
import static com.ithome.day26.governance.AccessGovernanceGuard.Role.COMPLIANCE;
import static com.ithome.day26.governance.AccessGovernanceGuard.Role.ENGINEER;
import static com.ithome.day26.governance.AccessGovernanceGuard.Role.TECH_LEAD;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AccessGovernanceGuardTest {

    @Test
    void engineerCannotUseRealCustomerScansAsTestData() {
        AccessGovernanceGuard guard = new AccessGovernanceGuard();

        assertThrows(SecurityException.class,
                () -> guard.authorize(ENGINEER, RESTRICTED, "補 OCR 前處理測試"));

        assertFalse(guard.auditTrail().get(0).approved());
    }

    @Test
    void complianceCanAccessRestrictedDataWithPurpose() {
        AccessGovernanceGuard guard = new AccessGovernanceGuard();

        guard.authorize(COMPLIANCE, RESTRICTED, "稽核去識別化流程");

        assertTrue(guard.auditTrail().get(0).approved());
    }

    @Test
    void techLeadCanAccessInternalButNotRestricted() {
        AccessGovernanceGuard guard = new AccessGovernanceGuard();

        guard.authorize(TECH_LEAD, INTERNAL, "檢查 ETL 設定");

        assertThrows(SecurityException.class,
                () -> guard.authorize(TECH_LEAD, RESTRICTED, "除錯正式資料"));
    }

    @Test
    void purposeMustNotBeBlankEvenForPublicData() {
        AccessGovernanceGuard guard = new AccessGovernanceGuard();

        assertThrows(IllegalArgumentException.class,
                () -> guard.authorize(ENGINEER, PUBLIC, " "));
    }

    @Test
    void deniedAttemptsStillAppearInAuditTrail() {
        AccessGovernanceGuard guard = new AccessGovernanceGuard();

        try {
            guard.authorize(ENGINEER, RESTRICTED, "貼真實掃描檔測試");
        } catch (SecurityException ignored) {
            // 預期被拒絕，仍要檢查稽核紀錄是否留存
        }

        List<AccessGovernanceGuard.AuditEvent> trail = guard.auditTrail();
        assertEquals(1, trail.size());
        assertEquals(ENGINEER, trail.get(0).requester());
    }
}
