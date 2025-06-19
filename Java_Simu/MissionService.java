import org.json.JSONArray;
import org.json.JSONObject;
import java.util.*;

/**
 * Récupération des missions via l’API et notification de fin de mission.
 */
public class MissionService {
    private final ApiClient api;
    private final String robotId;

    public MissionService(ApiClient api, String robotId) {
        this.api = api;
        this.robotId = robotId;
    }

    /**
     * Renvoie une liste de missions ;
     * chaque mission est une liste de positions (1..10).
     */
    public List<List<Integer>> fetch() {
        try {
            String body = api.get("/instructions?robot_id=" + robotId);
            JSONObject json = new JSONObject(body);
            Object blocks = json.get("blocks");
            JSONArray arr = blocks instanceof String
                ? new JSONArray((String) blocks)
                : (JSONArray) blocks;

            List<List<Integer>> missions = new ArrayList<>();
            if (arr.length() > 0 && arr.get(0) instanceof Number) {
                // un simple tableau de nombres → une seule mission
                List<Integer> path = new ArrayList<>();
                for (int i = 0; i < arr.length(); i++) {
                    path.add(arr.getInt(i));
                }
                missions.add(path);
            } else {
                // chaque sous-tableau devient une mission
                for (int i = 0; i < arr.length(); i++) {
                    JSONArray sub = arr.getJSONArray(i);
                    List<Integer> path = new ArrayList<>();
                    for (int j = 0; j < sub.length(); j++) {
                        path.add(sub.getInt(j));
                    }
                    missions.add(path);
                }
            }
            return missions;
        } catch (Exception ex) {
            ex.printStackTrace();
            return Collections.emptyList();
        }
    }

    /**
     * Envoie l'ID du robot au serveur pour signaler
     * que la mission vient de se terminer.
     */
    public void summary() {
        try {
            JSONObject payload = new JSONObject()
                .put("robot_id", robotId);
            api.post("/summary", payload.toString());
            System.out.println("➜ Mission terminée, robot_id envoyé : " + robotId);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
}
