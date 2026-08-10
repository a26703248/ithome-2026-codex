package com.ithome.day26.governance;

import java.time.Instant;
import java.util.ArrayList;
import java.util.EnumSet;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;

/**
 * 最小化的存取治理檢查：模擬開發團隊自己用 Codex 存取不同分級資料時，
 * 依角色決定是否核准，並且不論核准或拒絕都留下稽核紀錄。
 *
 * 這裡的三個分級（PUBLIC／INTERNAL／RESTRICTED）只是示範順序，
 * 不是需求書已核定的正式資料分級規則；正式分級仍待法遵與資安確認。
 */
public final class AccessGovernanceGuard {

    public enum Classification {
        PUBLIC,
        INTERNAL,
        RESTRICTED
    }

    public enum Role {
        ENGINEER,
        TECH_LEAD,
        COMPLIANCE
    }

    public record AuditEvent(Instant timestamp, Role requester, Classification classification,
                              String purpose, boolean approved) {
        public AuditEvent {
            Objects.requireNonNull(timestamp, "timestamp");
            Objects.requireNonNull(requester, "requester");
            Objects.requireNonNull(classification, "classification");
            purpose = requireText(purpose, "purpose");
        }
    }

    private static final Map<Classification, Set<Role>> ALLOWED_ROLES = Map.of(
            Classification.PUBLIC, EnumSet.of(Role.ENGINEER, Role.TECH_LEAD, Role.COMPLIANCE),
            Classification.INTERNAL, EnumSet.of(Role.TECH_LEAD, Role.COMPLIANCE),
            Classification.RESTRICTED, EnumSet.of(Role.COMPLIANCE)
    );

    private final List<AuditEvent> events = new ArrayList<>();

    /**
     * 檢查是否核准存取；無論核准或拒絕，都會新增一筆稽核紀錄。
     *
     * @throws IllegalArgumentException 使用目的為空白
     * @throws SecurityException        角色不在該分級的允許清單內
     */
    public void authorize(Role requester, Classification classification, String purpose) {
        Objects.requireNonNull(requester, "requester");
        Objects.requireNonNull(classification, "classification");
        String normalizedPurpose = requireText(purpose, "purpose");

        boolean approved = ALLOWED_ROLES.get(classification).contains(requester);
        events.add(new AuditEvent(Instant.now(), requester, classification, normalizedPurpose, approved));

        if (!approved) {
            throw new SecurityException(
                    requester + " 無權存取 " + classification + " 等級資料：" + normalizedPurpose);
        }
    }

    public List<AuditEvent> auditTrail() {
        return List.copyOf(events);
    }

    private static String requireText(String value, String field) {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException(field + " must not be blank");
        }
        return value.strip();
    }
}
