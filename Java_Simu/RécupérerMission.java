import org.json.JSONArray;
import org.json.JSONObject;
import java.util.*;

/**
 * Service pour récupérer les missions et notifier la fin de mission.
 */
public class RécupérerMission {
    private final ApiClient api;
    private final String robotId;

    public RécupérerMission(ApiClient api, String robotId) {
        this.api = api;
        this.robotId = robotId;
    }

    /**
     * Récupère la liste des missions.
     * Chaque mission est une liste d'entiers.
     */
    public List<List<Integer>> fetch() {
        List<List<Integer>> missions = new ArrayList<>();
        try {
            String body = api.get("/instructions?robot_id=" + robotId);
            JSONObject json = new JSONObject(body);
            JSONArray arr = getBlocksAsArray(json.get("blocks"));

            // Si le premier élément est un nombre, c'est une seule mission
            if (arr.length() > 0 && arr.get(0) instanceof Number) {
                missions.add(jsonArrayToList(arr));
            } else {
                // Sinon, autre nombre est une liste de missions
                for (int i = 0; i < arr.length(); i++) {
                    missions.add(jsonArrayToList(arr.getJSONArray(i)));
                }
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return missions;
    }

    // Convertit un objet blocks en JSONArray
    private JSONArray getBlocksAsArray(Object blocks) {
        if (blocks instanceof String) {
            return new JSONArray((String) blocks);
        }
        return (JSONArray) blocks;
    }

    // Convertit un JSONArray en List<Integer>
    private List<Integer> jsonArrayToList(JSONArray arr) {
        List<Integer> list = new ArrayList<>();
        for (int i = 0; i < arr.length(); i++) {
            list.add(arr.getInt(i));
        }
        return list;
    }

    /**
     * Notifie le serveur que la mission est terminée.
     */
    public void summary() {
        try {
            JSONObject payload = new JSONObject().put("robot_id", robotId);
            api.post("/summary", payload.toString());
            System.out.println("➜ Mission terminée, robot_id envoyé : " + robotId);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
}
