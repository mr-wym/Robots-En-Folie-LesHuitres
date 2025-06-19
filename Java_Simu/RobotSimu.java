import java.awt.Color;
import java.util.*;

public class RobotSimu {
    public static final int NB_POSITIONS = 10;
    private static final List<Integer> BASES_DEPOT = Arrays.asList(4, 5, 8, 9);

    private final ApiClient api;
    private final String idRobot;
    private final RécupérerMission serviceMission;

    private List<List<Integer>> missions = Collections.emptyList();
    private int indexMissionCourante = 0, indexEtape = 0;
    private int position = 1;
    private boolean pinceActive = false;

    // Compteurs de cubes déposés dans chaque zone
    private int nbCubesZoneA = 0; // bases 4/5
    private int nbCubesZoneB = 0; // bases 8/9

    public int getNbCubesZoneA() { return nbCubesZoneA; }
    public int getNbCubesZoneB() { return nbCubesZoneB; }

    private final Map<Integer, Color> couleursBases = Map.of(
        1, Color.BLACK,
        2, Color.YELLOW,
        3, Color.RED,
        4, Color.BLACK,
        5, Color.BLACK,
        6, Color.PINK,
        7, new Color(148,0,211),
        8, Color.BLACK,
        9, Color.BLACK,
        10, Color.GREEN
    );

    private String statut = "En attente";

    // Étapes possibles d'une mission
    private enum Etape { ALLER_CUBE, PRENDRE_CUBE, ALLER_DEPOT, DEPOSER_CUBE, TERMINE }
    private Etape etapeActuelle = Etape.ALLER_CUBE;
    private int cible = -1;
    private int cibleDepot = -1;
    private List<Integer> basesDepotCourantes = Collections.emptyList();

    public RobotSimu(ApiClient api, String idRobot) {
        this.api = api;
        this.idRobot = idRobot;
        this.serviceMission = new RécupérerMission(api, idRobot);
    }

    // Charge les missions et réinitialise l'état
    public void chargerMissions() {
        missions = serviceMission.fetch();
        indexMissionCourante = 0;
        indexEtape = 0;
        etapeActuelle = Etape.ALLER_CUBE;
    }

    // Indique s'il reste des étapes à faire
    public boolean aEtapeSuivante() {
        return !missions.isEmpty() && (indexEtape < missions.get(indexMissionCourante).size() || etapeActuelle != Etape.TERMINE);
    }

    // Exécute l'étape courante de la mission
    public void executerEtape() {
        if (missions.isEmpty() || indexMissionCourante >= missions.size()) {
            setStatut("En attente");
            return;
        }
        if (indexEtape >= missions.get(indexMissionCourante).size()) {
            serviceMission.summary();
            setStatut("Terminé");
            etapeActuelle = Etape.TERMINE;
            return;
        }

        if (etapeActuelle == Etape.ALLER_CUBE) {
            cible = missions.get(indexMissionCourante).get(indexEtape);
            if (position != cible) {
                deplacerVers(cible);
            } else {
                etapeActuelle = Etape.PRENDRE_CUBE;
                setStatut("À un cube");
            }
        } else if (etapeActuelle == Etape.PRENDRE_CUBE) {
            pinceActive = true;
            sendTelemetry("PICK");
            // Pour le jaune, choisir la zone la moins remplie (aléatoire si égalité)
            if (cible == 2) {
                choisirZoneDepotPourJaune();
            } else {
                cibleDepot = trouverBaseDepotProche(position);
                basesDepotCourantes = Arrays.asList(cibleDepot);
            }
            etapeActuelle = Etape.ALLER_DEPOT;
        } else if (etapeActuelle == Etape.ALLER_DEPOT) {
            // Dépose dès qu'il atteint une base de la zone choisie
            if (basesDepotCourantes.contains(position)) {
                etapeActuelle = Etape.DEPOSER_CUBE;
                setStatut("Dépose un cube");
            } else {
                deplacerVers(cibleDepot);
            }
        } else if (etapeActuelle == Etape.DEPOSER_CUBE) {
            pinceActive = false;
            sendTelemetry("DROP");
            // Incrémente le compteur de la zone correspondante
            if (basesDepotCourantes.contains(position)) {
                if (position == 4 || position == 5) nbCubesZoneA++;
                if (position == 8 || position == 9) nbCubesZoneB++;
            }
            indexEtape++;
            if (indexEtape < missions.get(indexMissionCourante).size()) {
                etapeActuelle = Etape.ALLER_CUBE;
            } else {
                serviceMission.summary();
                setStatut("Terminé");
                etapeActuelle = Etape.TERMINE;
            }
        }
    }

    // Déplace le robot d'une position vers la cible (sens le plus court)
    private void deplacerVers(int cible) {
        int dir = directionLaPlusCourte(position, cible);
        position = (position + dir - 1 + NB_POSITIONS) % NB_POSITIONS + 1;
        sendTelemetry("MOVE");
    }

    // Retourne +1 ou -1 selon le sens le plus court sur le cercle
    private int directionLaPlusCourte(int de, int vers) {
        int f = de - 1, t = vers - 1;
        int sensHoraire = (t - f + NB_POSITIONS) % NB_POSITIONS;
        int sensAntiHoraire = (f - t + NB_POSITIONS) % NB_POSITIONS;
        return sensHoraire <= sensAntiHoraire ? 1 : -1;
    }

    // Trouve la base de dépôt la plus proche
    private int trouverBaseDepotProche(int pos) {
        return BASES_DEPOT.stream()
            .min(Comparator.comparingInt(base -> Math.abs(pos - base)))
            .orElse(BASES_DEPOT.get(0));
    }

    // Choisit la zone de dépôt pour le jaune (la moins remplie, ou aléatoire si égalité)
    private void choisirZoneDepotPourJaune() {
        Random rand = new Random();
        if (nbCubesZoneA < nbCubesZoneB) {
            basesDepotCourantes = Arrays.asList(4, 5);
        } else if (nbCubesZoneB < nbCubesZoneA) {
            basesDepotCourantes = Arrays.asList(8, 9);
        } else {
            basesDepotCourantes = rand.nextBoolean() ? Arrays.asList(4, 5) : Arrays.asList(8, 9);
        }
        cibleDepot = basesDepotCourantes.get(rand.nextInt(basesDepotCourantes.size()));
    }

    // Envoie la télémétrie et met à jour le statut
    private void sendTelemetry(String statut) {
        switch (statut) {
            case "MOVE" -> setStatut("Déplacement");
            case "PICK" -> setStatut("À un cube");
            case "DROP" -> setStatut("Dépose un cube");
            default -> setStatut("En attente");
        }
        Telemetry t = new Telemetry(1, idRobot, statut, pinceActive, 1.0, 0.0);
        try {
            String resp = api.post("/telemetry", t.toJson());
            System.out.println("Telemetry → " + resp);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // Getters pour l'interface graphique
    public int getPosition()          { return position; }
    public boolean isPinceActive()    { return pinceActive; }
    public List<List<Integer>> getMissions() { return missions; }
    public Color getBaseColor(int i)  { return couleursBases.getOrDefault(i, Color.LIGHT_GRAY); }
    public String getStatut()         { return statut; }
    public void setStatut(String s)   { statut = s; }
}