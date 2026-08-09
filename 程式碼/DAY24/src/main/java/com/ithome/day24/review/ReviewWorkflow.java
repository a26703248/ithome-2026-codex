package com.ithome.day24.review;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public final class ReviewWorkflow {

    public enum Decision {
        ACCEPTED,
        MODIFIED,
        REJECTED
    }

    public record DraftVersion(int version, String content) {
        public DraftVersion {
            if (version < 1) {
                throw new IllegalArgumentException("version must be positive");
            }
            Objects.requireNonNull(content, "content");
        }
    }

    public record ReviewEvent(Decision decision, String reason, String reviewer) {
        public ReviewEvent {
            Objects.requireNonNull(decision, "decision");
            reason = reason == null ? "" : reason.strip();
            reviewer = requireText(reviewer, "reviewer");
        }
    }

    private final List<DraftVersion> versions = new ArrayList<>();
    private final List<ReviewEvent> events = new ArrayList<>();

    public ReviewWorkflow(String originalDraft) {
        versions.add(new DraftVersion(1, requireText(originalDraft, "originalDraft")));
    }

    public void submit(Decision decision, String revisedContent, String reason, String reviewer) {
        Objects.requireNonNull(decision, "decision");
        String normalizedReason = reason == null ? "" : reason.strip();

        if (normalizedReason.isBlank()) {
            throw new IllegalArgumentException("複核原因不可空白");
        }
        if (decision == Decision.MODIFIED) {
            versions.add(new DraftVersion(versions.size() + 1,
                    requireText(revisedContent, "revisedContent")));
        }

        events.add(new ReviewEvent(decision, normalizedReason, reviewer));
    }

    public List<DraftVersion> versions() {
        return List.copyOf(versions);
    }

    public List<ReviewEvent> events() {
        return List.copyOf(events);
    }

    private static String requireText(String value, String field) {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException(field + " must not be blank");
        }
        return value.strip();
    }
}
