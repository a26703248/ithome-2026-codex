package com.ithome.day09.review;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.AbstractSet;
import java.util.Iterator;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CyclicBarrier;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;
import org.junit.jupiter.api.Test;

class DailyImportGateTest {

    @Test
    void rejectsNullWorkspaceIdAsInvalidInput() {
        DailyImportGate gate = new DailyImportGate();

        assertThrows(IllegalArgumentException.class, () -> gate.tryStart(null));
    }

    @Test
    void onlyOneConcurrentAttemptStartsTheSameWorkspace()
            throws InterruptedException, ExecutionException, TimeoutException {
        DailyImportGate gate = new DailyImportGate(new BarrierSet());
        ExecutorService executor = Executors.newFixedThreadPool(2);

        try {
            Future<Boolean> first = executor.submit(() -> gate.tryStart("workspace-42"));
            Future<Boolean> second = executor.submit(() -> gate.tryStart("workspace-42"));

            int started = Boolean.compare(first.get(2, TimeUnit.SECONDS), false)
                    + Boolean.compare(second.get(2, TimeUnit.SECONDS), false);
            assertEquals(1, started);
        } finally {
            executor.shutdownNow();
        }
    }

    @Test
    void finishUsesTheSameNormalizedKeyAsTryStart() {
        DailyImportGate gate = new DailyImportGate();

        assertTrue(gate.tryStart(" Workspace-42 "));
        gate.finish(" Workspace-42 ");

        assertTrue(gate.tryStart("workspace-42"));
    }

    @Test
    void aRunningWorkspaceCannotStartTwice() {
        DailyImportGate gate = new DailyImportGate();

        assertTrue(gate.tryStart("workspace-42"));
        assertFalse(gate.tryStart("WORKSPACE-42"));
    }

    private static final class BarrierSet extends AbstractSet<String> {

        private final Set<String> delegate = ConcurrentHashMap.newKeySet();
        private final CyclicBarrier barrier = new CyclicBarrier(2);

        @Override
        public boolean add(String value) {
            awaitBothCalls();
            return delegate.add(value);
        }

        @Override
        public Iterator<String> iterator() {
            return delegate.iterator();
        }

        @Override
        public int size() {
            return delegate.size();
        }

        @Override
        public boolean remove(Object value) {
            return delegate.remove(value);
        }

        private void awaitBothCalls() {
            try {
                barrier.await(2, TimeUnit.SECONDS);
            } catch (Exception exception) {
                throw new IllegalStateException("concurrent calls did not meet", exception);
            }
        }
    }
}
