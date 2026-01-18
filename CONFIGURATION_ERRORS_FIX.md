# ⚠️ Correction des Erreurs de Configuration

## Erreur 1: `Integration 'imo_relay_device2' not found`

**Cause:** Tu ne peux pas créer des domaines personnalisés comme `imo_relay_device2` ou `imo_relay_device5`.

**Solution:** Utilise l'intégration `imo_relay` avec `"multiple": true` pour créer plusieurs instances.

### Configuration Correcte:

```yaml
# Instance 1 - Automate 1 (Étage)
imo_relay:
  port: "/dev/ttyUSB0"
  baudrate: 38400
  bytesize: 8
  slave_id: 1
  name: "Automate 1 - Étage"
  relays:
    - name: "Chambre Parents"
      address: 0x2C00
    # ... etc

# Instance 2 - Automate 2 (RDC) - OPTIONNEL
imo_relay_rdc:
  port: "/dev/ttyUSB0"
  baudrate: 38400
  bytesize: 8
  slave_id: 2
  name: "Automate 2 - RDC"
  relays:
    - name: "Salon 1"
      address: 0x2C00
    # ... etc

# Instance 3 - Automate 5 (Équipements) - OPTIONNEL
imo_relay_equipements:
  port: "/dev/ttyUSB0"
  baudrate: 38400
  bytesize: 8
  slave_id: 5
  name: "Automate 5 - Équipements"
  relays:
    - name: "Radiateur SDB"
      address: 0x2C06
    # ... etc
```

## Erreur 2: `Requirements for imo_relay not found: ['pymodbus==3.6.0']`

**Cause:** `pymodbus` n'est pas installé.

**Solution 1 - Installation automatique (HACS):**
- HACS installe automatiquement les dépendances en version `>=3.6.0`

**Solution 2 - Installation manuelle:**
```bash
pip install pymodbus>=3.6.0
```

**Solution 3 - Via SSH sur ta Pi:**
```bash
ssh root@192.168.1.xx
pip install --upgrade pymodbus
```

## ✅ Fichiers à Utiliser:

1. **`configuration_minimal.yaml`** - Configuration simple avec 1 seule instance (RECOMMANDÉ pour commencer)
2. **`configuration_complete.yaml`** - Configuration avec tous les relais commentés

## 🚀 Marche à Suivre:

### Étape 1: Redémarrer Home Assistant

Pour installer les dépendances:
- Va dans **Paramètres → Système → Redémarrer**
- HA va installer `pymodbus` automatiquement

### Étape 2: Utiliser `configuration_minimal.yaml`

Remplace le contenu de ton `configuration.yaml` par `configuration_minimal.yaml`

### Étape 3: Redémarrer à nouveau

HA va charger la nouvelle configuration avec 1 seule instance pour le slave_id 1

### Étape 4: Vérifier les Logs

**Développement → Logs** devrait montrer:
```
IMO Relay connected to /dev/ttyUSB0
Successfully loaded integration imo_relay
```

### Étape 5 (Optionnel): Ajouter d'autres instances

Une fois que la première instance fonctionne, tu peux ajouter:

```yaml
# Ajoute APRÈS imo_relay: dans configuration.yaml
imo_relay_rdc:
  port: "/dev/ttyUSB0"
  baudrate: 38400
  bytesize: 8
  slave_id: 2
  name: "Automate 2 - RDC"
  relays:
    - name: "Salon 1"
      address: 0x2C00
      icon: mdi:lightbulb
    # ... ajoute tous les relais du RDC
```

## 📋 Noms des Domaines (unique pour chaque instance):

- `imo_relay` ← Instance 1 (Automate 1)
- `imo_relay_rdc` ← Instance 2 (Automate 2 - RDC)
- `imo_relay_equipements` ← Instance 3 (Automate 5)
- `imo_relay_garage` ← Instance 4 (si besoin)

Chaque domaine crée des entity_id:
- Instance 1: `switch.relay_1`, `switch.relay_2`, etc.
- Instance 2: `switch.relay_rdc_1`, `switch.relay_rdc_2`, etc.

## ✨ Après Redémarrage:

Tu devrais voir 16 nouveaux `switch.relay_*` dans Home Assistant:
- ✅ `switch.relay_1` → Chambre Parents
- ✅ `switch.relay_2` → Dressing
- ✅ etc.

---

**Besoin d'aide?** Consulte les logs pour plus de détails!
