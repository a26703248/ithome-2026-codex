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

    // Test seam added only to make the check-then-act ordering reproducible.
    DailyImportGate(Set<String> runningWorkspaces) {
        this.runningWorkspaces = Objects.requireNonNull(runningWorkspaces);
    }

    public boolean tryStart(String workspaceId) {
        if (workspaceId.isBlank()) {
            throw new IllegalArgumentException("workspaceId must not be blank");
        }
        String key = workspaceId.strip().toLowerCase(Locale.ROOT);
        if (runningWorkspaces.contains(key)) {
            return false;
        }
        runningWorkspaces.add(key);
        return true;
    }

    public void finish(String workspaceId) {
        runningWorkspaces.remove(workspaceId);
    }
}
