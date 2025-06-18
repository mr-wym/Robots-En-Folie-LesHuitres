import javax.swing.*;
import java.awt.*;

/**
 * Interface graphique Swing pour le simulateur de robot.
 */
public class SimulatorUI {

    /**
     * Affiche la fenêtre principale et lance la simulation.
     * @param logic Instance du simulateur de robot
     */
    public static void show(RobotSimulator logic) {
        JFrame frame = new JFrame("Simulateur Robot");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // Panel de dessin
        SimulationPanel panel = new SimulationPanel(logic);
        panel.setPreferredSize(new Dimension(600, 600));

        // Bouton unique
        JButton loadAndRun = new JButton("Charger & Lancer");

        // Timer toutes les 400 ms
        Timer timer = new Timer(400, e -> {
            if (logic.hasNextStep()) {
                logic.startNextStep();
                panel.repaint();
            } else {
                ((Timer)e.getSource()).stop();
            }
        });
        timer.setInitialDelay(0);

        loadAndRun.addActionListener(e -> {
            logic.fetchMissions();
            JOptionPane.showMessageDialog(
                frame,
                logic.getMissions().size() + " mission(s) chargée(s)"
            );
            timer.start();
        });

        // Montage UI
        JPanel controls = new JPanel();
        controls.add(loadAndRun);

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
        private final RobotSimulator logic;

        /**
         * Constructeur du panel de simulation.
         * @param logic Instance du simulateur de robot
         */
        SimulationPanel(RobotSimulator logic) { this.logic = logic; }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            Graphics2D g2 = (Graphics2D) g;
            g2.setRenderingHint(
                RenderingHints.KEY_ANTIALIASING,
                RenderingHints.VALUE_ANTIALIAS_ON
            );

            int cx = getWidth()/2, cy = getHeight()/2, r = 120;
            // Cercle
            g2.setColor(new Color(230,230,230));
            g2.setStroke(new BasicStroke(2));
            g2.drawOval(cx-r, cy-r, r*2, r*2);

            // Bases
            for (int i = 1; i <= RobotSimulator.NUM_POS; i++) {
                double ang = 2*Math.PI*(i-1)/RobotSimulator.NUM_POS - Math.PI/2;
                int bx = cx + (int)(r*Math.cos(ang));
                int by = cy + (int)(r*Math.sin(ang));
                g2.setColor(logic.getBaseColor(i));
                g2.fillOval(bx-16, by-16, 32, 32);
                g2.setColor(Color.BLACK);
                String lbl = String.valueOf(i);
                FontMetrics fm = g2.getFontMetrics();
                g2.drawString(
                    lbl,
                    bx - fm.stringWidth(lbl)/2,
                    by + fm.getAscent()/2 - 4
                );
            }

            // Robot
            int pos = logic.getPosition();
            double angR = 2*Math.PI*(pos-1)/RobotSimulator.NUM_POS - Math.PI/2;
            int rx = cx + (int)(r*Math.cos(angR)) - 12;
            int ry = cy + (int)(r*Math.sin(angR)) - 12;
            g2.setColor(Color.RED);
            g2.fillOval(rx, ry, 24, 24);

            // Pince
            if (logic.isPinceActive()) {
                g2.setColor(new Color(255,100,100,128));
                g2.fillOval(rx-4, ry-4, 32, 32);
            }
        }
    }
}
