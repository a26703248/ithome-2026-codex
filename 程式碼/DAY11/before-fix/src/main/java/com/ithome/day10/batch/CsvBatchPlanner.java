package com.ithome.day10.batch;

public class CsvBatchPlanner {
    public int countBatches(int rowCount, int batchSize) {
        if (rowCount < 0) {
            throw new IllegalArgumentException("rowCount must be non-negative");
        }
        if (batchSize <= 0) {
            throw new IllegalArgumentException("batchSize must be positive");
        }

        return rowCount / batchSize + 1;
    }
}
