/** Point d'entrée : compose logique + UI. */
public class Main {
    public static void main(String[] args) {
        ApiClient api = new ApiClient("http://10.7.5.42:8000");
        RobotSimulator logic = new RobotSimulator(api, "54d67923-704f-4b97-b6d4-64a0a04ca5de");
        SimulatorUI.show(logic);
    }
}
