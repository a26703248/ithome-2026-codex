package com.ithome.day06.normalizer;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Test;

class DataNormalizerTest {

    private final DataNormalizer normalizer = new DataNormalizer();

    @Test
    void normalizesCrawlerRecord() {
        var createdAt = Instant.parse("2026-08-05T01:00:00Z");
        var updatedAt = Instant.parse("2026-08-05T02:00:00Z");
        var source = new CrawlerRecord(
                "Crawler title", "Crawler content", List.of("java"), createdAt, updatedAt);

        var result = normalizer.normalize(source);

        assertEquals(
                new WorkspaceDocument(
                        "Crawler title", "Crawler content", List.of("java"), createdAt, updatedAt),
                result);
    }

    @Test
    void normalizesHostedRecord() {
        var createdAt = Instant.parse("2026-08-05T03:00:00Z");
        var updatedAt = Instant.parse("2026-08-05T04:00:00Z");
        var source = new HostedRecord(
                "Hosted title", "Hosted content", List.of("workspace"), createdAt, updatedAt);

        var result = normalizer.normalize(source);

        assertEquals(
                new WorkspaceDocument(
                        "Hosted title", "Hosted content", List.of("workspace"), createdAt, updatedAt),
                result);
    }

    @Test
    void appliesDemonstrationDefaultsToNullFields() {
        var result = normalizer.normalize(new CrawlerRecord(null, null, null, null, null));

        assertEquals(new WorkspaceDocument("", "", List.of(), Instant.EPOCH, Instant.EPOCH), result);
    }

    @Test
    void copiesTagsBeforeReturningDocument() {
        var sourceTags = new ArrayList<>(List.of("initial"));
        var result = normalizer.normalize(new HostedRecord("title", "content", sourceTags, null, null));

        sourceTags.add("added-later");

        assertEquals(List.of("initial"), result.tags());
        assertThrows(UnsupportedOperationException.class, () -> result.tags().add("blocked"));
    }

    @Test
    void rejectsNullElementInTags() {
        var tags = new ArrayList<String>();
        tags.add("valid");
        tags.add(null);

        var source = new HostedRecord("title", "content", tags, null, null);

        assertThrows(NullPointerException.class, () -> normalizer.normalize(source));
    }

    @Test
    void rejectsNullSource() {
        assertThrows(NullPointerException.class, () -> normalizer.normalize((CrawlerRecord) null));
        assertThrows(NullPointerException.class, () -> normalizer.normalize((HostedRecord) null));
    }
}
