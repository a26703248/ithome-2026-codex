package com.ithome.day06.normalizer;

import java.time.Instant;
import java.util.List;
import java.util.Objects;

public final class DataNormalizer {

    public WorkspaceDocument normalize(CrawlerRecord source) {
        Objects.requireNonNull(source, "source must not be null");
        return createDocument(
                source.title(),
                source.description(),
                source.tags(),
                source.createTime(),
                source.updateTime());
    }

    public WorkspaceDocument normalize(HostedRecord source) {
        Objects.requireNonNull(source, "source must not be null");
        return createDocument(
                source.title(),
                source.description(),
                source.tags(),
                source.createAt(),
                source.updateAt());
    }

    private WorkspaceDocument createDocument(
            String title,
            String description,
            List<String> tags,
            Instant createdAt,
            Instant updatedAt) {
        return new WorkspaceDocument(
                stringOrEmpty(title),
                stringOrEmpty(description),
                tags == null ? List.of() : List.copyOf(tags),
                createdAt == null ? Instant.EPOCH : createdAt,
                updatedAt == null ? Instant.EPOCH : updatedAt);
    }

    private String stringOrEmpty(String value) {
        return value == null ? "" : value;
    }
}
