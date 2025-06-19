import org.json.JSONObject;

/**
 * Trame de télémétrie envoyée à l'API.
 */
public class Telemetry {
    /** Ligne ou position du robot. */
    private final int ligne;
    /** Identifiant du robot. */
    private final String robotId;
    /** Statut du déplacement. */
    private final String statusDeplacement;
    /** Statut de la pince. */
    private final boolean statusPince;
    /** Vitesse du robot. */
    private final double vitesse;
    /** Distance mesurée par ultrasons. */
    private final double distanceUltrasons;

    /**
     * Constructeur.
     */
    public Telemetry(int ligne,
                     String robotId,
                     String statusDeplacement,
                     boolean statusPince,
                     double vitesse,
                     double distanceUltrasons) {
        this.ligne = ligne;
        this.robotId = robotId;
        this.statusDeplacement = statusDeplacement;
        this.statusPince = statusPince;
        this.vitesse = vitesse;
        this.distanceUltrasons = distanceUltrasons;
    }

    /**
     * Sérialise en JSON.
     */
    public String toJson() {
        JSONObject j = new JSONObject();
        j.put("ligne", ligne);
        j.put("robot_id", robotId);
        j.put("status_deplacement", statusDeplacement);
        j.put("status_pince", statusPince);
        j.put("vitesse", vitesse);
        j.put("distance_ultrasons", distanceUltrasons);
        return j.toString();
    }
}
