package com.ithome.day10.batch;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

class CsvBatchPlannerTest {
    private final CsvBatchPlanner planner = new CsvBatchPlanner();

    @Test
    void returnsZeroForNoRows() {
        assertEquals(0, planner.countBatches(0, 500));
    }

    @Test
    void returnsOneForPartialBatch() {
        assertEquals(1, planner.countBatches(200, 500));
    }

    @Test
    void returnsTwoForExactMultiple() {
        assertEquals(2, planner.countBatches(1000, 500));
    }

    @Test
    void returnsThreeWhenRowsRemain() {
        assertEquals(3, planner.countBatches(1001, 500));
    }

    @Test
    void rejectsNonPositiveBatchSize() {
        assertThrows(IllegalArgumentException.class, () -> planner.countBatches(1000, 0));
    }
}
