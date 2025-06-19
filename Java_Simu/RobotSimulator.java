import java.awt.Color;
import java.util.*;

/**
 * Logique du simulateur : position sur 10 bases en cercle,
 * gestion des missions, activation de la pince, télémétrie.
 */
public class RobotSimulator {
    /** Nombre de positions sur le cercle. */
    public static final int NUM_POS = 10;

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

    /**
     * Constructeur du simulateur.
     * @param api Client API pour les requêtes réseau
     * @param robotId Identifiant du robot
     */
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

    /** Exécute une étape : déplacement ou activation de la pince. */
    public void startNextStep() {
        if (!hasNextStep()) {
            // Plus d'étapes : on notifie la fin de cette mission
            missionService.summary();
            return;
        }

        int target = missions.get(currentMissionIndex).get(stepIndex);
        if (position != target) {
            int dir = shortestDirection(position, target);
            position = (position + dir - 1 + NUM_POS) % NUM_POS + 1;
            sendTelemetry("MOVE");
        } else {
            pinceActive = !pinceActive;
            sendTelemetry("PICK");
            stepIndex++;
            // Si on vient de finir la dernière étape :
            if (!hasNextStep()) {
                missionService.summary();
            }
        }
    }

    /** Retourne la position actuelle du robot. */
    public int getPosition()             { return position; }
    /** Retourne l’état de la pince. */
    public boolean isPinceActive()       { return pinceActive; }
    /** Retourne la liste des missions. */
    public List<List<Integer>> getMissions() { return missions; }
    /** Retourne la couleur d’une base. */
    public Color getBaseColor(int i)     { return baseColors.getOrDefault(i, Color.LIGHT_GRAY); }

    /**
     * Calcule la direction la plus courte entre deux positions.
     * @param from Position de départ
     * @param to Position d’arrivée
     * @return 1 pour sens horaire, -1 pour antihoraire
     */
    private int shortestDirection(int from, int to) {
        int f = from - 1, t = to - 1;
        int cw = (t - f + NUM_POS) % NUM_POS;
        int ccw = (f - t + NUM_POS) % NUM_POS;
        return cw <= ccw ? 1 : -1;
    }

    /**
     * Envoie la télémétrie à l’API.
     * @param status Statut du robot ("MOVE" ou "PICK")
     */
    private void sendTelemetry(String status) {
        Telemetry t = new Telemetry(1, robotId, status, pinceActive, 1.0, 0.0);
        try {
            String resp = api.post("/telemetry", t.toJson());
            System.out.println("Telemetry → " + resp);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
