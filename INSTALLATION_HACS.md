# Déployer sur GitHub et HACS

## 📦 Étapes d'installation sur GitHub

### 1. Créer un repository GitHub

```bash
# Initialiser le repo (si pas déjà fait)
cd c:\Users\gabriel\Desktop\caca\haos\ extension\imo_modbus
git init
git add .
git commit -m "Initial commit: IMO Ismart Relay Control"
```

### 2. Créer le repo sur GitHub

1. Va sur https://github.com/new
2. Remplis:
   - **Repository name:** `imo_relay` (ou `imo-ismart-relay`)
   - **Description:** "Home Assistant integration for IMO Ismart SMT-CD-T20 relays via Modbus RTU"
   - **Public:** OUI (obligatoire pour HACS)
   - **Add .gitignore:** Python
   - **License:** MIT

3. Clone et pousse ton code:

```bash
git remote add origin https://github.com/artemis-fowl-fowl/imo_relay.git
git branch -M main
git push -u origin main
```

## 📝 Vérifications avant HACS

Avant de soumettre à HACS, assure-toi que tu as:

✅ **README.md** - Avec instructions claires  
✅ **LICENSE** - MIT ou compatible  
✅ **manifest.json** - Correct et à jour  
✅ **CHANGELOG.md** - Version history  
✅ **hacs.json** - Configuration HACS  
✅ **.gitignore** - Pour éviter les fichiers inutiles  
✅ **Dossier custom_components/imo_relay/** - Bonne structure  

## 🚀 Soumettre à HACS

### Option 1: HACS Default (Automatique)

1. Pousse ton repo sur GitHub en public
2. Va sur https://hacs.xyz/docs/publish/integration
3. Remplis le formulaire avec ton repo
4. Attends que HACS valide (peut prendre quelques jours)

### Option 2: HACS Direct (Rapide)

1. Va sur https://hacs.xyz/
2. Clique **+ Create custom repository**
3. Entre l'URL: `https://github.com/artemis-fowl-fowl/imo_relay`
4. Type: **Integration**
5. Clique **Create**

Les utilisateurs pourront alors l'ajouter via:
- HACS → ⋮ → Dépôts personnalisés → (ton URL)

## 📋 Checklist Finale

- [ ] Repo sur GitHub (PUBLIC)
- [ ] README.md rédigé
- [ ] manifest.json valide
- [ ] LICENSE présent
- [ ] CHANGELOG.md créé
- [ ] hacs.json configuré
- [ ] Structure correcte `custom_components/imo_relay/`
- [ ] Tags de version sur GitHub (v1.0.0, etc.)
- [ ] Soumis à HACS (ou repo personnel activé)

## 🔗 Ressources

- HACS Docs: https://hacs.xyz/
- Integration Manifest: https://developers.home-assistant.io/docs/creating_integration_manifest
- GitHub Help: https://docs.github.com/

---

**Besoin d'aide?** Contacte-moi pour la mise en place! 🚀
