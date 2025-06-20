import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

/**
 * Client HTTP simple pour requêtes GET/POST JSON.
 */
public class ApiClient {
    private final HttpClient client = HttpClient.newHttpClient();
    private final String baseUrl;

    /**
     * @param baseUrl URL racine des requêtes
     */
    public ApiClient(String baseUrl) {
        this.baseUrl = baseUrl;
    }

    /**
     * Requête GET HTTP.
     * @param path Chemin de la requête
     * @return Réponse du serveur
     * @throws Exception En cas d'erreur HTTP
     */
    public String get(String path) throws Exception {
        return client.send(
            HttpRequest.newBuilder(URI.create(baseUrl + path)).GET().build(),
            HttpResponse.BodyHandlers.ofString()
        ).body();
    }

    /**
     * Requête POST HTTP avec données JSON.
     * @param path Chemin de la requête
     * @param json Données JSON à envoyer
     * @return Réponse du serveur
     * @throws Exception En cas d'erreur HTTP
     */
    public String post(String path, String json) throws Exception {
        return client.send(
            HttpRequest.newBuilder(URI.create(baseUrl + path))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(json))
                .build(),
            HttpResponse.BodyHandlers.ofString()
        ).body();
    }
}
