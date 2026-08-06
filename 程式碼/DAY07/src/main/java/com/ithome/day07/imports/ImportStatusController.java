package com.ithome.day07.imports;

import java.util.Optional;
import java.util.UUID;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/imports")
public class ImportStatusController {
    private final ImportJobs importJobs;

    public ImportStatusController(ImportJobs importJobs) {
        this.importJobs = importJobs;
    }

    @GetMapping("/{jobId}")
    public ResponseEntity<?> find(@PathVariable UUID jobId) {
        Optional<ImportJobView> job = importJobs.find(jobId);
        if (job.isPresent()) {
            return ResponseEntity.ok(job.get());
        }
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
                .body(new ApiError("IMPORT_NOT_AVAILABLE", "import job is not available"));
    }
}

enum ImportStatus {
    PENDING,
    RUNNING,
    SUCCEEDED,
    FAILED
}

record ImportJobView(UUID jobId, ImportStatus status) {
}

record ApiError(String code, String message) {
}

interface ImportJobs {
    Optional<ImportJobView> find(UUID jobId);
}
