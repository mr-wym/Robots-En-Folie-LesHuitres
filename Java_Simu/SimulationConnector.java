public class SimulationConnector {

    private static final String BASE_URL = "http://localhost:8000";  // Change si le serveur est ailleurs

    public static void enregistrerRobot(String mac, String alias) {
        String json = String.format("""
            {
                "macAddress": "%s",
                "alias": "%s"
            }
        """, mac, alias);
        try {
            String response = ApiClient.sendPost(BASE_URL + "/robotInitialize", json);
            System.out.println("Robot enregistré : " + response);
        } catch (Exception e) {
            System.err.println("Erreur enregistrement robot : " + e.getMessage());
        }
    }

    public static void envoyerCommande(String datetime, String commande, String mac, String alias) {
        String json = String.format("""
            {
                "datetime": "%s",
                "commande": "%s",
                "macAddress": "%s",
                "alias": "%s"
            }
        """, datetime, commande, mac, alias);
        try {
            String response = ApiClient.sendPost(BASE_URL + "/setinstructions", json);
            System.out.println("Commande envoyée : " + response);
        } catch (Exception e) {
            System.err.println("Erreur envoi commande : " + e.getMessage());
        }
    }

    public static void lireCommandes() {
        try {
            String response = ApiClient.sendGet(BASE_URL + "/instructions");
            System.out.println("Commandes reçues : " + response);
        } catch (Exception e) {
            System.err.println("Erreur lecture commandes : " + e.getMessage());
        }
    }

    public static void lireTelemetry() {
        try {
            String response = ApiClient.sendGet(BASE_URL + "/api/telemetry");
            System.out.println("Télémétrie reçue : " + response);
        } catch (Exception e) {
            System.err.println("Erreur lecture télémétrie : " + e.getMessage());
        }
    }
}
