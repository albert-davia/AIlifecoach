# AI Life Coach - LangGraph Agent

Un agent d'intelligence artificielle pour le coaching de vie, construit avec LangGraph et LangChain.

## 🚀 Configuration Rapide

### 1. Activer l'environnement virtuel
```bash
# Option 1: Utiliser le script d'aide
./activate_env.sh

# Option 2: Activation manuelle
source venv/bin/activate
```

### 2. Vérifier l'installation
```bash
# Tester les imports Python
python -c "import agent; print('✅ Tous les imports réussis!')"

# Vérifier LangGraph CLI
langgraph --help
```

## 🔧 Utilisation de LangGraph CLI

### Serveur de développement
```bash
# Démarrer le serveur de développement
langgraph dev --config langgraph.json --port 8123 --no-browser

# Accéder à l'interface web
open http://localhost:8123/docs
```

### Autres commandes CLI
```bash
# Créer un nouveau projet
langgraph new mon-projet --template new-langgraph-project-python

# Construire une image Docker
langgraph build --config langgraph.json

# Générer un Dockerfile
langgraph dockerfile --config langgraph.json

# Lancer en production
langgraph up --config langgraph.json
```

## 📁 Structure du Projet

```
AIlifecoach/
├── venv/                    # Environnement virtuel Python
├── agent.py                 # Agent principal de coaching de vie
├── requirements.txt         # Dépendances Python
├── langgraph.json          # Configuration LangGraph CLI
├── activate_env.sh         # Script d'activation de l'environnement
└── README.md               # Ce fichier
```

## 🐍 Utilisation Python

### Exécuter l'agent directement
```bash
# S'assurer que l'environnement virtuel est activé
source venv/bin/activate

# Exécuter l'agent
python agent.py
```

### Importer dans Python
```python
import agent

# Accéder au graph compilé
graph = agent.graph

# Utiliser le graph
result = graph.invoke({
    "messages": [],
    "life_coach_state": {...},
    "current_date": "2024-01-01"
})
```

## 🔑 Variables d'environnement

Créer un fichier `.env` à la racine du projet :
```bash
# Clé API OpenAI
OPENAI_API_KEY=votre_cle_api_openai_ici

# Optionnel: Clé API LangGraph (pour la production)
LANGGRAPH_API_KEY=votre_cle_api_langgraph_ici
```

## 🌐 API REST

Une fois le serveur démarré, l'API est disponible sur :
- **Documentation interactive** : http://localhost:8123/docs
- **Spécification OpenAPI** : http://localhost:8123/openapi.json
- **Endpoints principaux** :
  - `/assistants` - Gestion des assistants
  - `/threads` - Gestion des conversations
  - `/runs` - Exécution des tâches

## 🚀 Options de déploiement

### 1. Développement local
```bash
langgraph dev --config langgraph.json
```

### 2. Déploiement Docker
```bash
# Générer Dockerfile
langgraph dockerfile --config langgraph.json

# Construire l'image
langgraph build --config langgraph.json

# Exécuter le conteneur
docker run -p 8123:8123 votre-app-name
```

### 3. Déploiement cloud
LangGraph CLI supporte le déploiement sur diverses plateformes cloud. Consultez la documentation LangGraph pour les instructions spécifiques.

## 🛠️ Dépannage

### Erreurs d'import
Si vous voyez des erreurs d'import :
```bash
# Réinstaller les dépendances
pip install -r requirements.txt

# Ou installer les packages manquants
pip install python-dotenv langgraph-cli[inmem]
```

### Problèmes d'environnement virtuel
```bash
# Recréer l'environnement virtuel
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### LangGraph CLI introuvable
```bash
# Réinstaller LangGraph CLI
pip install --upgrade langgraph-cli[inmem]
```

## 📚 Ressources additionnelles

- [Documentation LangGraph](https://langchain-ai.github.io/langgraph/)
- [Guide LangGraph CLI](https://langchain-ai.github.io/langgraph/how-tos/cli/)
- [Documentation LangChain](https://python.langchain.com/)

## 🎯 Prochaines étapes

1. Configurer votre fichier `.env` avec les clés API
2. Tester l'agent avec `python agent.py`
3. Démarrer le serveur de développement avec `langgraph dev --config langgraph.json`
4. Personnaliser la logique de l'agent dans `agent.py`
5. Déployer en production quand prêt

## ✅ Statut actuel

- ✅ Environnement virtuel configuré
- ✅ LangGraph CLI installé et fonctionnel
- ✅ Serveur de développement opérationnel
- ✅ API REST accessible
- ✅ Documentation interactive disponible