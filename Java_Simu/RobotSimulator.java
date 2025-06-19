import java.awt.Color;
import java.util.*;

/**
 * Logique du simulateur : position sur 10 bases en cercle,
 * gestion des missions, activation de la pince, dépôt automatique dans la base la plus proche,
 * et télémétrie.
 */
public class RobotSimulator {
    /** Nombre de positions sur le cercle. */
    public static final int NUM_POS = 10;
    /** Positions considérées comme bases pour le dépôt. */
    private static final List<Integer> BASE_POSITIONS = Arrays.asList(4, 5, 8, 9);

    private final ApiClient api;
    private final String robotId;
    private final MissionService missionService;

    private List<List<Integer>> missions = Collections.emptyList();
    private int currentMissionIndex = 0, stepIndex = 0;

    private int position = 1;
    private boolean pinceActive = false;

    private final Map<Integer, Color> baseColors = Map.of(
        1, new Color(200,200,255),
        2, Color.YELLOW,
        3, Color.RED,
        4, Color.ORANGE,
        5, new Color(150,75,0),
        6, Color.PINK,
        7, new Color(148,0,211),
        8, Color.CYAN,
        9, Color.DARK_GRAY,
        10, Color.GREEN
    );

    public RobotSimulator(ApiClient api, String robotId) {
        this.api = api;
        this.robotId = robotId;
        this.missionService = new MissionService(api, robotId);
    }

    /** Charge les missions depuis l’API. */
    public void fetchMissions() {
        missions = missionService.fetch();
        currentMissionIndex = 0;
        stepIndex = 0;
    }

    /** Indique s’il reste des étapes à exécuter. */
    public boolean hasNextStep() {
        if (missions.isEmpty()) return false;
        return stepIndex < missions.get(currentMissionIndex).size();
    }

    /**
     * Exécute une étape : déplacement ou saisie + dépôt automatique.
     */
    public void startNextStep() {
        if (!hasNextStep()) {
            missionService.summary();
            return;
        }

        int target = missions.get(currentMissionIndex).get(stepIndex);
        if (position != target) {
            // Déplacement vers la cible
            int dir = shortestDirection(position, target);
            position = (position + dir - 1 + NUM_POS) % NUM_POS + 1;
            sendTelemetry("MOVE");
        } else {
            // Saisie et dépôt automatique
            if (!pinceActive) {
                // On ferme la pince (on saisit)
                pinceActive = true;
                sendTelemetry("PICK");
                // Calcul de la base la plus proche
                int depositBase = findNearestBase(position);
                // On se déplace vers cette base
                while (position != depositBase) {
                    int dir = shortestDirection(position, depositBase);
                    position = (position + dir - 1 + NUM_POS) % NUM_POS + 1;
                    sendTelemetry("MOVE");
                }
                // On ouvre la pince (on dépose)
                pinceActive = false;
                sendTelemetry("DROP");
            }
            // Passage à l'étape suivante
            stepIndex++;
            if (!hasNextStep()) {
                missionService.summary();
            }
        }
    }

    /** Calcule la direction la plus courte entre deux positions. */
    private int shortestDirection(int from, int to) {
        int f = from - 1, t = to - 1;
        int cw = (t - f + NUM_POS) % NUM_POS;
        int ccw = (f - t + NUM_POS) % NUM_POS;
        return cw <= ccw ? 1 : -1;
    }

    /** Trouve la base la plus proche de la position donnée. */
    private int findNearestBase(int pos) {
        int best = BASE_POSITIONS.get(0);
        int minDist = Math.abs(pos - best);
        for (int base : BASE_POSITIONS) {
            int dist = Math.abs(pos - base);
            if (dist < minDist) {
                minDist = dist;
                best = base;
            }
        }
        return best;
    }

    /** Envoie la télémétrie à l’API. */
    private void sendTelemetry(String status) {
        Telemetry t = new Telemetry(1, robotId, status, pinceActive, 1.0, 0.0);
        try {
            String resp = api.post("/telemetry", t.toJson());
            System.out.println("Telemetry → " + resp);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // Getters
    public int getPosition()          { return position; }
    public boolean isPinceActive()    { return pinceActive; }
    public List<List<Integer>> getMissions() { return missions; }
    public Color getBaseColor(int i)  { return baseColors.getOrDefault(i, Color.LIGHT_GRAY); }
}