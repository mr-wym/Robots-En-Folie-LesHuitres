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
        1, Color.BLACK,     // zone de départ
        2, Color.YELLOW,
        3, Color.RED,
        4, Color.BLACK,      // zone de dépôt
        5, Color.BLACK,      // zone de dépôt
        6, Color.PINK,
        7, new Color(148,0,211),
        8, Color.BLACK,      // zone de dépôt
        9, Color.BLACK,      // zone de dépôt
        10, Color.GREEN
    );

    private String status = "En attente";

    // Ajoute un enum pour suivre l'étape courante
    private enum StepState { MOVE_TO_CUBE, PICK_CUBE, MOVE_TO_BASE, DROP_CUBE, DONE }
    private StepState stepState = StepState.MOVE_TO_CUBE;
    private int target = -1;
    private int baseTarget = -1;

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
        stepState = StepState.MOVE_TO_CUBE;
    }

    /** Indique s’il reste des étapes à exécuter. */
    public boolean hasNextStep() {
        return !missions.isEmpty() && (stepIndex < missions.get(currentMissionIndex).size() || stepState != StepState.DONE);
    }

    /**
     * Exécute une étape : déplacement ou saisie + dépôt automatique.
     */
    public void startNextStep() {
        if (missions.isEmpty() || currentMissionIndex >= missions.size()) {
            setStatus("En attente");
            return;
        }
        if (stepIndex >= missions.get(currentMissionIndex).size()) {
            missionService.summary();
            setStatus("Terminé");
            stepState = StepState.DONE;
            return;
        }

        if (stepState == StepState.MOVE_TO_CUBE) {
            target = missions.get(currentMissionIndex).get(stepIndex);
            if (position != target) {
                moveTo(target);
            } else {
                stepState = StepState.PICK_CUBE;
                setStatus("À un cube");
            }
        } else if (stepState == StepState.PICK_CUBE) {
            pinceActive = true;
            sendTelemetry("PICK");
            baseTarget = findNearestBase(position);
            stepState = StepState.MOVE_TO_BASE;
        } else if (stepState == StepState.MOVE_TO_BASE) {
            if (position != baseTarget) {
                moveTo(baseTarget);
            } else {
                stepState = StepState.DROP_CUBE;
                setStatus("Dépose un cube");
            }
        } else if (stepState == StepState.DROP_CUBE) {
            pinceActive = false;
            sendTelemetry("DROP");
            stepIndex++;
            if (stepIndex < missions.get(currentMissionIndex).size()) {
                stepState = StepState.MOVE_TO_CUBE;
            } else {
                missionService.summary();
                setStatus("Terminé");
                stepState = StepState.DONE;
            }
        }
    }

    /** Déplace le robot vers la cible. */
    private void moveTo(int target) {
        int dir = shortestDirection(position, target);
        position = (position + dir - 1 + NUM_POS) % NUM_POS + 1;
        sendTelemetry("MOVE");
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
        return BASE_POSITIONS.stream()
            .min(Comparator.comparingInt(base -> Math.abs(pos - base)))
            .orElse(BASE_POSITIONS.get(0));
    }

    /** Envoie la télémétrie à l’API. */
    private void sendTelemetry(String status) {
        switch (status) {
            case "MOVE" -> setStatus("Déplacement");
            case "PICK" -> setStatus("À un cube");
            case "DROP" -> setStatus("Dépose un cube");
            default -> setStatus("En attente");
        }
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

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }
}