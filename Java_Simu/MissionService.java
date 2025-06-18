import org.json.JSONArray;
import org.json.JSONObject;
import java.util.*;

/** Récupération des missions via l’API. */
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
            Object rows = json.get("rows");
            JSONArray arr = rows instanceof String
                ? new JSONArray((String) rows)
                : (JSONArray) rows;

            List<List<Integer>> missions = new ArrayList<>();
            // Si tableau plat de nombres → une seule mission
            if (arr.length() > 0 && arr.get(0) instanceof Number) {
                List<Integer> path = new ArrayList<>();
                for (int i = 0; i < arr.length(); i++) {
                    path.add(arr.getInt(i));
                }
                missions.add(path);
            } else {
                // Sinon, chaque sous-tableau devient une mission
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
}
