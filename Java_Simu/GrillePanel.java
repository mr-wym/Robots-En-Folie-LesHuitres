//fait avec chat gpt

import javax.swing.*;
import java.awt.*;

public class GrillePanel extends JPanel {
    private final Robot robot;

    public GrillePanel(Robot robot) {
        this.robot = robot;
        setPreferredSize(new Dimension(400, 400));
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        int r = 120;
        int centerX = getWidth() / 2;
        int centerY = getHeight() / 2;

        for (int i = 0; i < 8; i++) {
            double angle = 2 * Math.PI * i / 8;
            int x = (int) (centerX + r * Math.cos(angle));
            int y = (int) (centerY + r * Math.sin(angle));

            if (i == 0) g.setColor(Color.BLUE);
            else if (i == 3 || i == 6) g.setColor(Color.GREEN);
            else if (robot.estZoneAvecCube(i)) g.setColor(Color.decode("#b0ffb0"));
            else g.setColor(Color.LIGHT_GRAY);

            g.fillOval(x - 15, y - 15, 30, 30);
            g.setColor(Color.BLACK);
            g.drawString("Z" + i, x - 10, y + 5);
        }

        int idx = robot.getPosition().getIndex();
        double angle = 2 * Math.PI * idx / 8;
        int rx = (int) (centerX + r * Math.cos(angle));
        int ry = (int) (centerY + r * Math.sin(angle));

        g.setColor(Color.RED);
        g.fillOval(rx - 10, ry - 10, 20, 20);
    }
}
