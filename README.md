ansible/
├── inventories/
│   └── prod/
│       └── hosts.ini               # Liste des serveurs cibles (IP, utilisateurs SSH)
│
├── group_vars/
│   └── all.yml                     # Variables globales (domaines, mots de passe, clés, etc.)
│
├── roles/                          # Rôles Ansible : un rôle = un service indépendant
│   ├── common/                     # Mise à jour système, firewall, création d’utilisateurs
│   │   └── tasks/
│   │       └── main.yml
│   │
│   ├── docker/                     # Installation et configuration de Docker + Docker Compose
│   │   └── tasks/
│   │       └── main.yml
│   │
│   ├── keycloak/                   # Service d’authentification unique (SSO)
│   │   ├── tasks/
│   │   │   └── main.yml
│   │   ├── templates/
│   │   │   ├── .env.j2
│   │   │   └── keycloak-init.sh.j2 # Script d’initialisation automatique (realm, clients, groupes)
│   │   └── files/
│   │       └── docker-compose.yml
│   │
│   ├── n8n/                        # Automatisation des flux Stripe → Keycloak → Wiki.js
│   │   ├── tasks/
│   │   │   └── main.yml
│   │   ├── templates/
│   │   │   └── .env.j2
│   │   └── files/
│   │       └── docker-compose.yml
│   │
│   ├── portal/                     # 🌐 Portail client (Node.js + Stripe)
│   │   ├── tasks/
│   │   │   └── main.yml
│   │   ├── templates/
│   │   │   └── .env.j2
│   │   ├── files/                  # Code source du portail (Dockerfile, server.js, etc.)
│   │   │   ├── Dockerfile
│   │   │   ├── docker-compose.yml
│   │   │   ├── package.json
│   │   │   ├── server.js
│   │   │   └── views/
│   │   │       └── dashboard.ejs
│   │   └── public/                 # Fichiers statiques HTML/CSS (interface utilisateur)
│   │       ├── index.html
│   │       ├── success.html
│   │       ├── cancel.html
│   │       └── styles.css
│   │
│   ├── postgres/                   # Configuration locale de PostgreSQL (optionnel)
│   │   └── tasks/
│   │       └── main.yml
│   │
│   ├── traefik/                    # Reverse proxy avec certificats TLS automatiques (Let's Encrypt)
│   │   ├── tasks/
│   │   │   └── main.yml
│   │   ├── templates/
│   │   │   └── docker-compose.yml
│   │   └── files/
│   │       └── traefik.yml
│   │
│   ├── wiki/                       # Déploiement des instances Wiki.js (ia, devops, cyber)
│   │   ├── tasks/
│   │   │   └── main.yml
│   │   ├── templates/
│   │   │   └── .env.j2
│   │   └── files/
│   │       └── docker-compose.yml
│   │
│   └── wiki-essaie/                # Rôle de test (pour expérimentations et validations locales)
│       └── tasks/
│           └── main.yml
│
├── provisioner/                    # 🔧 API Node.js qui déclenche Ansible pour créer de nouveaux wikis
│   ├── tasks/
│   │   └── main.yml                # Déploiement du service Provisioner (Docker)
│   ├── files/
│   │   └── docker-compose.yml      # Lancement du service Node.js (API Express)
│   ├── templates/
│   │   └── env.j2                  # Template du fichier .env (PORT, API_KEY, chemins Ansible)
│   └── README.md
│
├── site_wiki.yml                   # Playbook principal – orchestre tous les rôles
└── README.md                       # Documentation globale Ansible
