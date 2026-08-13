package com.ithome.day06.normalizer;

import java.time.Instant;
import java.util.List;

public record CrawlerRecord(
        String title,
        String description,
        List<String> tags,
        Instant createTime,
        Instant updateTime) {
}
