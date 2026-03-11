# ChronikAI — Product Roadmap

## Vision

ChronikAI est un **système de mémoire professionnelle augmentée**.
Son objectif n’est pas de générer des posts, mais de **capturer, structurer et valoriser le travail réel**
afin d’aider les professionnels à construire une carrière visible, cohérente et durable.

Le post LinkedIn n’est qu’un **output parmi d’autres**.

---

## Principes directeurs

- **Local-first & privacy-first**
- **Aucune donnée brute envoyée vers l’extérieur**
- **Le cerveau avant l’interface**
- **La valeur avant la visibilité**
- **Architecture modulaire et extractible**

---

## V1 — Fondations (MVP fonctionnel)

🎯 Objectif : prouver que le travail réel peut être transformé en signal exploitable.

### Capture (Watcher)
- [x] Détection application active
- [x] Capture titre de fenêtre
- [x] Fréquence configurable (60s par défaut)
- [x] Whitelist / blacklist applicative
- [x] Stockage local SQLite
- [x] Fonctionnement en arrière-plan

### Intelligence (Brain)
- [x] Regroupement des événements en sessions
- [x] Détection basique de contexte (dev / doc / comm)
- [x] Extraction de mots-clés
- [x] Résumé journalier orienté apprentissage
- [x] Génération de *Knowledge Units*
- [x] Prompt LinkedIn prédéfini

### Interface (Studio)
- [x] Dashboard journalier
- [x] Vue sessions clés
- [x] Édition manuelle du contenu généré
- [x] Sélecteur de style de post
- [x] Copie vers presse-papier

📦 Livraison : **outil personnel utilisable quotidiennement**

---

## V1.5 — Stabilisation & Qualité

🎯 Objectif : fiabilité, clarté, confiance utilisateur.

- [ ] Refactor des frontières entre modules
- [ ] Logs structurés
- [ ] Gestion des erreurs silencieuse
- [ ] Mode pause / reprise
- [ ] Amélioration des heuristiques de sessions
- [ ] Tests unitaires Brain & Watcher
- [ ] Documentation technique minimale

---

## V2 — Capital professionnel

🎯 Objectif : transformer ChronikAI en **outil de capitalisation de carrière**

### Mémoire long terme
- [ ] Mémoire des thématiques récurrentes
- [ ] Évolution des compétences détectées
- [ ] Historique des apprentissages

### Outputs avancés
- [ ] Bilan hebdomadaire / mensuel
- [ ] Génération de résumé de mission
- [ ] Export Markdown / JSON
- [ ] Intégration Notion / Obsidian

### Intelligence
- [ ] Détection de moments à forte valeur
- [ ] Scoring de signal professionnel
- [ ] Déduplication sémantique

---

## V3 — Coaching de carrière assisté

🎯 Objectif : passer de la mémoire à la **stratégie personnelle**

- [ ] Analyse de trajectoire professionnelle
- [ ] Identification des angles éditoriaux naturels
- [ ] Recommandations de positionnement
- [ ] Suggestions de narration long terme
- [ ] Alertes : sous-exposition / sur-dispersion

---

## V4 — Usage avancé & collaboration

🎯 Objectif : ouvrir ChronikAI au-delà de l’individu

- [ ] Mode équipe (opt-in, non intrusif)
- [ ] Valorisation du travail invisible
- [ ] Version manager / lead
- [ ] API ChronikAI (lecture seule)
- [ ] SDK pour outils tiers

---

## Stratégie de monétisation (indicative)

- Gratuit : Watcher + résumé basique
- Payant individuel :
  - Mémoire long terme
  - Analyses avancées
  - Exports professionnels
- B2B :
  - Coaching carrière
  - Version équipe
  - Support & déploiement

---

## Hors périmètre volontaire

ChronikAI **ne vise pas** :
- la surveillance intrusive
- le tracking de performance managérial
- l’automatisation de publication
- le growth hacking

---

## Succès du produit =

Un utilisateur capable de dire :
> *« ChronikAI m’aide à comprendre et valoriser ce que je construis, pas juste à en parler. »*
