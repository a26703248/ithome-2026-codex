package com.ithome.day06.normalizer;

import java.time.Instant;
import java.util.List;

public record WorkspaceDocument(
        String title,
        String content,
        List<String> tags,
        Instant createdAt,
        Instant updatedAt) {
}
