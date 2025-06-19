# Robots-En-Folie-LesHuitres

## Démarrage du serveur

1. Activez l'environnement virtuel :
    ```bash
    source env/bin/activate
    ```

2. Lancez le serveur :
    ```bash
    uvicorn main:ap --reload --env-file=.env --host 0.0.0.0
    ```

---

## API Endpoints

### Récupérer les instructions

- **GET**  
  ```
  http://10.7.5.42:8000/instructions?robot_id=53d67923-704f-4b97-b6d4-64a0a04ca5de
  ```

### Envoyer la télémétrie

- **POST**  
  ```
  http://10.7.5.42:8000/telemetry
  ```
  **Body :**
  ```json
  {
     "vitesse": 12,
     "distance_ultrasons": 42,
     "status_deplacement": "avance",
     "ligne": true,
     "status_pince": false,
     "robot_id": "53d67923-704f-4b97-b6d4-64a0a04ca5de"
  }
  ```

### Récupérer le résumé

- **POST**  
  ```
  http://10.7.5.42:8000/summary
  ```
  **Body :**
  ```json
  {
     "robot_id": "53d67923-704f-4b97-b6d4-64a0a04ca5de"
  }
  ```