public class Position {
    private int x;
    private int y;
    private String typeZone; // optionnel : "cube", "dépot", etc.

    public int getIndex() {
    // On retourne juste x pour simplifier si tu n’as pas d'ID de zone
    return this.x;
}

    public Position(int x, int y) {
        this.x = x;
        this.y = y;
        this.typeZone = "inconnue";
    }

    public Position(int x, int y, String typeZone) {
        this.x = x;
        this.y = y;
        this.typeZone = typeZone;
    }

    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }

    public String getTypeZone() {
        return typeZone;
    }

    public void setTypeZone(String typeZone) {
        this.typeZone = typeZone;
    }

    @Override
    public String toString() {
        return "(" + x + ", " + y + ") [" + typeZone + "]";
    }
}
