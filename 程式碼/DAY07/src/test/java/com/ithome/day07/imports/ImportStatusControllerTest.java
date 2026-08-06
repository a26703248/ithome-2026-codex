package com.ithome.day07.imports;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;

import java.util.Optional;
import java.util.UUID;

import org.junit.jupiter.api.Test;
import org.springframework.http.HttpStatus;

class ImportStatusControllerTest {
    private static final UUID JOB_ID = UUID.fromString("4df63aac-e40b-4dd7-adb5-05b56a8736c2");

    @Test
    void returnsJobWhenAvailable() {
        ImportStatusController controller = new ImportStatusController(
                id -> Optional.of(new ImportJobView(id, ImportStatus.RUNNING)));

        var response = controller.find(JOB_ID);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        ImportJobView body = assertInstanceOf(ImportJobView.class, response.getBody());
        assertEquals(JOB_ID, body.jobId());
        assertEquals(ImportStatus.RUNNING, body.status());
    }

    @Test
    void returnsNotFoundWhenJobIsUnavailable() {
        ImportStatusController controller = new ImportStatusController(id -> Optional.empty());

        var response = controller.find(JOB_ID);

        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        ApiError body = assertInstanceOf(ApiError.class, response.getBody());
        assertEquals("IMPORT_NOT_AVAILABLE", body.code());
    }
}
