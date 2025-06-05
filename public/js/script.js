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
            data.rows.sort((a, b) => new Date(b.datetime) - new Date(a.datetime));

            data.rows.forEach(commande => {
                const listItem = document.createElement("li");
                listItem.textContent = `${commande.commande || "Aucune commande disponible"}, ${commande.datetime || "Non disponible"}`;
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
                listItem.textContent = robot.macaddress || "Adresse MAC non disponible";
                robotsList.appendChild(listItem);
            });
        } else {
            robotsList.textContent = "Aucun robot trouvé";
        }
    })
    .catch(error => {
        console.error("Erreur de récupération :", error);
    });


document.getElementById('macAddress').addEventListener('input', function (e) {
    let value = e.target.value.toUpperCase().replace(/[^A-F0-9]/g, ''); // Supprime les caractères non-hexadécimaux
    let formatted = '';

    for (let i = 0; i < value.length; i++) {
        if (i > 0 && i % 2 === 0 && i < 12) {
            formatted += ':';
        }
        formatted += value[i];
    }

    e.target.value = formatted;
});

async function initializeRobot(event) {
    event.preventDefault();
    const macAddress = document.getElementById('macAddress').value;

    try {
        const response = await fetch('/api/robotInitialize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ macAddress: macAddress }),
        });

        if (response.ok) {
            alert('Robot initialisé avec succès !');
            document.getElementById('macForm').reset();
            window.location.reload();
        } else if (response.status === 409) {
            const data = await response.json();
            alert(`Erreur : ${data.error}`);
        } else {
            alert('Erreur lors de l\'initialisation du robot.');
        }
    } catch (error) {
        console.error('Erreur:', error);
        alert('Une erreur est survenue.');
    }
}


async function initializeCommande(event) {
    event.preventDefault();
    const commande = document.getElementById('commande').value;
    const datetime = new Date().toISOString();
    
    try {
        const response = await fetch('/api/commandeInitialize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                commande: commande,
                datetime: datetime
            }),
        });

        if (response.ok) {
            alert('Robot initialisé avec succès !');
            document.getElementById('commandeForm').reset();
            window.location.reload();
        } else {
            alert('Erreur lors de l\'initialisation du robot.');
        }
    } catch (error) {
        console.error('Erreur:', error);
        alert('Une erreur est survenue.');
    }
}