import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.net.HttpURLConnection;
import java.net.URL;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import org.json.JSONArray;
import org.json.JSONObject;

public class SimulationUI extends JFrame {
    private final Robot robot;
    private final JTextArea info;
    private final GrillePanel grille;
    private String derniereCommande = null;

    public SimulationUI() {
        setTitle("Simulation du Robot");
        setSize(800, 600);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        robot = new Robot();
        info = new JTextArea(5, 20);
        info.setEditable(false);
        JScrollPane scrollPane = new JScrollPane(info);
        grille = new GrillePanel(robot);

        JButton btnObtenirCommande = new JButton("Obtenir commande");
        JButton btnExecuterCommande = new JButton("Exécuter commande");

        btnObtenirCommande.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                recupererCommandeDepuisServeur();
            }
        });

        btnExecuterCommande.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (derniereCommande != null) {
                    info.append("\nExécution de la commande : " + derniereCommande);
                    robot.executerCommande(derniereCommande);
                    grille.repaint();
                } else {
                    info.append("\nAucune commande à exécuter.");
                }
            }
        });

        JPanel panelBoutons = new JPanel();
        panelBoutons.add(btnObtenirCommande);
        panelBoutons.add(btnExecuterCommande);

        add(grille, BorderLayout.CENTER);
        add(scrollPane, BorderLayout.SOUTH);
        add(panelBoutons, BorderLayout.NORTH);

        setVisible(true);
    }

    private void recupererCommandeDepuisServeur() {
        try {
            URL url = new URL("http://localhost:8000/api/commandes");
            HttpURLConnection con = (HttpURLConnection) url.openConnection();
            con.setRequestMethod("GET");

            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
            String inputLine;
            StringBuilder content = new StringBuilder();

            while ((inputLine = in.readLine()) != null) {
                content.append(inputLine);
            }

            in.close();
            con.disconnect();

            JSONObject obj = new JSONObject(content.toString());
            JSONArray commandes = obj.getJSONArray("rows");

            if (commandes.length() > 0) {
                JSONObject commande = commandes.getJSONObject(0);
                derniereCommande = commande.getString("commande");
                info.setText("Commande reçue : " + derniereCommande);
            } else {
                derniereCommande = null;
                info.setText("Aucune commande disponible.");
            }
        } catch (Exception e) {
            info.setText("Erreur de récupération : " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new SimulationUI());
    }
}
