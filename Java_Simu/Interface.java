import javax.swing.*;
import java.awt.*;

/**
 * Interface graphique Swing pour le simulateur de robot.
 */
public class Interface {

    /**
     * Affiche la fenêtre principale et lance la simulation.
     * @param logic Instance du simulateur de robot
     */
    public static void show(RobotSimu logic) {
        JFrame frame = new JFrame("Simulateur Robot");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // simu interface globale
        SimulationPanel panel = new SimulationPanel(logic);
        panel.setPreferredSize(new Dimension(600, 600));

        // texte pour l'état et les dépôts
        JLabel statusLabel = new JLabel("État : " + logic.getStatut());
        JLabel depotLabel = new JLabel("Zone 4/5 : 0 cube(s) | Zone 8/9 : 0 cube(s)");

        // Bouton pour charger et lancer la simulation
        JButton loadAndRun = new JButton("Charger & Lancer");

        // Timer toutes les 1,5 secondes
        Timer timer = new Timer(1500, e -> {
            if (logic.aEtapeSuivante()) {
                logic.executerEtape();
                panel.repaint();
                statusLabel.setText("État : " + logic.getStatut());
                depotLabel.setText("Zone 4/5 : " + logic.getNbCubesZoneA() + " cube(s) | Zone 8/9 : " + logic.getNbCubesZoneB() + " cube(s)");
            } else {
                statusLabel.setText("État : Terminé");
                ((Timer)e.getSource()).stop();
            }
        });
        timer.setInitialDelay(0);

        loadAndRun.addActionListener(e -> {
            logic.chargerMissions();
            JOptionPane.showMessageDialog(frame, logic.getMissions().size() + " mission(s) chargée(s)");
            statusLabel.setText("État : " + logic.getStatut());
            depotLabel.setText("Zone 4/5 : " + logic.getNbCubesZoneA() + " cube(s) | Zone 8/9 : " + logic.getNbCubesZoneB() + " cube(s)");
            timer.start();
        });

        // Montage UI
        JPanel controls = new JPanel();
        controls.add(loadAndRun);
        controls.add(statusLabel);
        controls.add(depotLabel);

        frame.add(controls, BorderLayout.NORTH);
        frame.add(panel, BorderLayout.CENTER);
        frame.pack();
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);
    }

    /**
     * Panel interne pour dessiner le cercle, les bases et le robot.
     */
    private static class SimulationPanel extends JPanel {
        private final RobotSimu logic;

        /**
         * Constructeur du panel de simulation.
         * @param logic Instance du simulateur de robot
         */
        SimulationPanel(RobotSimu logic) { this.logic = logic; }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            Graphics2D g2 = (Graphics2D) g;
            g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

            int cx = getWidth()/2, cy = getHeight()/2, r = 120;

            // Cercle
            g2.setColor(new Color(230,230,230));
            g2.setStroke(new BasicStroke(2));
            g2.drawOval(cx-r, cy-r, r*2, r*2);

            // Bases et numéros
            for (int i = 1; i <= RobotSimu.NB_POSITIONS; i++) {
                double ang = 2*Math.PI*(i-1)/RobotSimu.NB_POSITIONS - Math.PI/2;
                int bx = cx + (int)(r*Math.cos(ang));
                int by = cy + (int)(r*Math.sin(ang));
                g2.setColor(logic.getBaseColor(i));
                g2.fillOval(bx-24, by-24, 48, 48);

                // Numéros en blanc pour zones de dépôt et départ, sinon noir
                if (i == 1 || i == 4 || i == 5 || i == 8 || i == 9) {
                    g2.setColor(Color.WHITE);
                } else {
                    g2.setColor(Color.BLACK);
                }
                String lbl = String.valueOf(i);
                FontMetrics fm = g2.getFontMetrics();
                g2.drawString(lbl, bx - fm.stringWidth(lbl)/2, by + fm.getAscent()/2 - 4);
            }

            // Robot
            int pos = logic.getPosition();
            double angR = 2*Math.PI*(pos-1)/RobotSimu.NB_POSITIONS - Math.PI/2;
            int rx = cx + (int)(r*Math.cos(angR)) - 12;
            int ry = cy + (int)(r*Math.sin(angR)) - 12;
            g2.setColor(Color.RED);
            g2.fillOval(rx, ry, 24, 24);

            // Lettre R sur le robot
            g2.setColor(Color.WHITE);
            g2.setFont(g2.getFont().deriveFont(Font.BOLD, 16f));
            FontMetrics fmR = g2.getFontMetrics();
            String robotLabel = "R";
            int labelX = rx + 12 - fmR.stringWidth(robotLabel)/2;
            int labelY = ry + 12 + fmR.getAscent()/2 - 4;
            g2.drawString(robotLabel, labelX, labelY);

            // Pince
            if (logic.isPinceActive()) {
                g2.setColor(new Color(255,100,100,128));
                g2.fillOval(rx-4, ry-4, 32, 32);
            }
        }
    }
}
