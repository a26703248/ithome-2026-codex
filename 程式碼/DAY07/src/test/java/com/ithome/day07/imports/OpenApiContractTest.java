package com.ithome.day07.imports;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Set;

import org.junit.jupiter.api.Test;

import io.swagger.v3.parser.OpenAPIV3Parser;
import io.swagger.v3.parser.core.models.ParseOptions;

class OpenApiContractTest {
    @Test
    void specificationMatchesTheStatusQueryDecisions() throws IOException {
        ParseOptions options = new ParseOptions();
        options.setResolve(true);
        String specification = Files.readString(Path.of("openapi.yaml"));
        var result = new OpenAPIV3Parser().readContents(specification, null, options);

        assertNotNull(result.getOpenAPI(), () -> "OpenAPI was not parsed: " + result.getMessages());
        assertTrue(result.getMessages().isEmpty(), () -> "Parser messages: " + result.getMessages());

        var operation = result.getOpenAPI().getPaths().get("/imports/{jobId}").getGet();
        assertNotNull(operation);
        assertEquals(Set.of("200", "404"), operation.getResponses().keySet());
        assertEquals("uuid", operation.getParameters().get(0).getSchema().getFormat());

        var statusSchema = result.getOpenAPI().getComponents().getSchemas()
                .get("ImportJobView").getProperties().get("status");
        assertEquals(List.of("PENDING", "RUNNING", "SUCCEEDED", "FAILED"), statusSchema.getEnum());
    }
}
