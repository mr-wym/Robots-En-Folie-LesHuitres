public class Robot {
    private Position position;
    private boolean aUnCube;
    private String typeCube;

    public Robot() {
        // Position de départ : zone 0 (modifiable)
        this.position = new Position(0, 0);
        this.aUnCube = false;
        this.typeCube = null;
    }
    public boolean estZoneAvecCube(int zone) {
    // Exemple basique : les cubes sont toujours sur zones 1, 2, 4, 5, 7
    return zone == 1 || zone == 2 || zone == 4 || zone == 5 || zone == 7;
}
    public Position getPosition() {
        return position;
    }

    public void setPosition(Position pos) {
        this.position = pos;
        System.out.println("Déplacement vers la position : " + pos);
    }

    public boolean aUnCube() {
        return aUnCube;
    }

    public void prendreCube() {
        if (!aUnCube) {
            this.aUnCube = true;
            this.typeCube = "CubeStandard";
            System.out.println("Cube pris !");
        } else {
            System.out.println("La pince contient déjà un cube !");
        }
    }

    public void deposerCube() {
        if (aUnCube) {
            System.out.println("Cube déposé !");
            this.aUnCube = false;
            this.typeCube = null;
        } else {
            System.out.println("Aucun cube à déposer !");
        }
    }

    public void executerCommande(String commande) {
        if (commande == null || commande.isEmpty()) {
            System.out.println("Commande vide !");
            return;
        }

        System.out.println("Commande reçue : " + commande);

        commande = commande.toLowerCase();

        // Commandes basiques, à adapter selon logique plus complexe si besoin
        if (commande.contains("aller a zone 1")) setPosition(new Position(1, 1));
        else if (commande.contains("aller a zone 2")) setPosition(new Position(2, 1));
        else if (commande.contains("aller a zone 3")) setPosition(new Position(3, 1));
        else if (commande.contains("aller a zone 4")) setPosition(new Position(4, 1));
        else if (commande.contains("aller a zone 5")) setPosition(new Position(5, 1));
        else if (commande.contains("aller a zone 6")) setPosition(new Position(6, 1));
        else if (commande.contains("aller a zone 7")) setPosition(new Position(7, 1));
        else if (commande.contains("prendre cube")) prendreCube();
        else if (commande.contains("deposer cube")) deposerCube();
        else System.out.println("Commande non reconnue : " + commande);
    }

    @Override
    public String toString() {
        return "Robot{" +
                "position=" + position +
                ", aUnCube=" + aUnCube +
                ", typeCube='" + typeCube + '\'' +
                '}';
    }
}
