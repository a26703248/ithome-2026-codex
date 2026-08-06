package com.ithome.day07.imports;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.UUID;

public class WorkspaceImportClient {
    private final HttpClient client;

    public WorkspaceImportClient(HttpClient client) {
        this.client = client;
    }

    public ApiResponse find(URI baseUri, UUID jobId)
            throws IOException, InterruptedException {
        URI endpoint = baseUri.resolve("/imports/" + jobId);
        HttpRequest request = HttpRequest.newBuilder(endpoint)
                .GET()
                .build();
        HttpResponse<String> response = client.send(
                request,
                HttpResponse.BodyHandlers.ofString());
        return new ApiResponse(response.statusCode(), response.body());
    }

    public record ApiResponse(int statusCode, String body) {
    }
}
