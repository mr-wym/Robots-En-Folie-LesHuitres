fetch("/api/valeurs")
    .then(response => response.json())
    .then(data => {
        if (data.rows.length > 0) {
            const latest = data.rows[data.rows.length - 1];
            document.getElementById("line_value").textContent = "Non disponible";
            document.getElementById("distance_value").textContent = latest.distance;
            document.getElementById("speed_value").textContent = latest.speed;
            document.getElementById("gripper_value").textContent = latest.pincevalue ? "Fermée" : "Ouverte";
        }
    })
    .catch(error => {
        console.error("Erreur de récupération :", error);
    });
    fetch("/api/commandes")
        .then(response => response.json())
        .then(data => {
            const commandeList = document.getElementById("commandesList");
            commandeList.innerHTML = ""; 
            if (data.rows.length > 0) {
                data.rows.forEach(commande => {
                    const listItem = document.createElement("li");
                    listItem.textContent = `ID: ${commande.id}, Commande: ${commande.commande || "Aucune commande disponible"}, Date/Heure: ${commande.datetime || "Non disponible"}`;
                    commandeList.appendChild(listItem);
                });
            } else {
                commandeList.textContent = "Aucune commande trouvée";
            }
        })
        .catch(error => {
            console.error("Erreur de récupération :", error);
        });

fetch("/api/robots")
    .then(response => response.json())
    .then(data => {
        const robotsList = document.getElementById("robotsList");
        robotsList.innerHTML = "";
        if (data.rows.length > 0) {
            // const sortedRobots = data.rows.sort((a, b) => a.id - b.id);
            data.rows.forEach(robot => {
                const listItem = document.createElement("li");
                listItem.textContent = robot.macadress || "Adresse MAC non disponible";
                robotsList.appendChild(listItem);
            });
        } else {
            robotsList.textContent = "Aucun robot trouvé";
        }
    })
    .catch(error => {
        console.error("Erreur de récupération :", error);
    });