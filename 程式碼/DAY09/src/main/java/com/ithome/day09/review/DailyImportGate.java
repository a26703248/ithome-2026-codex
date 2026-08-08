package com.ithome.day09.review;

import java.util.Locale;
import java.util.Objects;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

public final class DailyImportGate {

    private final Set<String> runningWorkspaces;

    public DailyImportGate() {
        this(ConcurrentHashMap.newKeySet());
    }

    DailyImportGate(Set<String> runningWorkspaces) {
        this.runningWorkspaces = Objects.requireNonNull(runningWorkspaces);
    }

    public boolean tryStart(String workspaceId) {
        return runningWorkspaces.add(normalize(workspaceId));
    }

    public void finish(String workspaceId) {
        runningWorkspaces.remove(normalize(workspaceId));
    }

    private String normalize(String workspaceId) {
        if (workspaceId == null || workspaceId.isBlank()) {
            throw new IllegalArgumentException("workspaceId must not be blank");
        }
        return workspaceId.strip().toLowerCase(Locale.ROOT);
    }
}
