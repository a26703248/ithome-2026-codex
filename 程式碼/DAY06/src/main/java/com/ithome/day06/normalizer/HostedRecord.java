package com.ithome.day06.normalizer;

import java.time.Instant;
import java.util.List;

public record HostedRecord(
        String title,
        String description,
        List<String> tags,
        Instant createAt,
        Instant updateAt) {
}
