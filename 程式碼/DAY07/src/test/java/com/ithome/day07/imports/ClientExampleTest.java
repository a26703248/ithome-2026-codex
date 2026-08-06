package com.ithome.day07.imports;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.URI;
import java.net.http.HttpClient;
import java.nio.charset.StandardCharsets;
import java.util.UUID;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;

class ClientExampleTest {
    private static final UUID JOB_ID = UUID.fromString("4df63aac-e40b-4dd7-adb5-05b56a8736c2");
    private static final String RESPONSE = """
            {"jobId":"4df63aac-e40b-4dd7-adb5-05b56a8736c2","status":"RUNNING"}
            """;

    private HttpServer server;
    private URI baseUri;

    @BeforeEach
    void startServer() throws IOException {
        server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        server.createContext("/imports/" + JOB_ID, this::handle);
        server.start();
        baseUri = URI.create("http://127.0.0.1:" + server.getAddress().getPort());
    }

    @AfterEach
    void stopServer() {
        server.stop(0);
    }

    @Test
    void javaHttpClientReadsRunningState() throws Exception {
        WorkspaceImportClient client = new WorkspaceImportClient(HttpClient.newHttpClient());

        var response = client.find(baseUri, JOB_ID);

        assertEquals(200, response.statusCode());
        assertTrue(response.body().contains("\"status\":\"RUNNING\""));
    }

    private void handle(HttpExchange exchange) throws IOException {
        boolean valid = "GET".equals(exchange.getRequestMethod());
        byte[] response = (valid ? RESPONSE : "{\"code\":\"IMPORT_NOT_AVAILABLE\"}")
                .getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().add("Content-Type", "application/json");
        exchange.sendResponseHeaders(valid ? 200 : 404, response.length);
        exchange.getResponseBody().write(response);
        exchange.close();
    }
}
