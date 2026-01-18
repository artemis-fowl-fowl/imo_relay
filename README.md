# IMO Ismart Relay Control - Integration Home Assistant 🎛️

[![HACS Custom][hacs-badge]][hacs-url]
[![License][license-badge]][license-url]
[![Python 3.11+][python-badge]][python-url]

Intégration Home Assistant pour contrôler les relais des automates **IMO Ismart SMT-CD-T20 3RD** via connexion Modbus RTU RS485.

## 🎯 Fonctionnalités

✅ **Contrôle des 4 relais** via Modbus RTU  
✅ **Lecture/Écriture des bobines Modbus** (coils)  
✅ **Configuration personnalisée** (baudrate, bytesize, slave ID)  
✅ **Intégration native Home Assistant** (Switches)  
✅ **Service personnalisé** pour contrôle avancé  
✅ **Dashboard Lovelace** stylisé inclus  
✅ **Logging détaillé** pour debugging  

## 📋 Pré-requis

- **Home Assistant** 2024.1.0 ou supérieur
- **Python** 3.11 ou supérieur
- **Raspberry Pi 3+** ou autre système Home Assistant
- **Convertisseur USB-RS485** connecté à la Pi
- **IMO Ismart SMT-CD-T20 3RD** avec Modbus RTU configuré

## 🚀 Installation

### Via HACS (Recommandé)

1. Ouvre **HACS** → **Intégrations**
2. Clique sur le menu **⋮** → **Dépôts personnalisés**
3. Colle l'URL: `https://github.com/artemis-fowl-fowl/imo_relay`
4. Catégorie: **Integration**
5. Clique **Créer**
6. Trouve **IMO Ismart Relay Control** → **Télécharger**
7. **Redémarre** Home Assistant

### Installation Manuelle

```bash
# Sur ton système HAOS
cd /config/custom_components/
git clone https://github.com/artemis-fowl-fowl/imo_relay
cd imo_relay
```

Puis redémarre Home Assistant.

## ⚙️ Configuration

Après installation, ajoute dans ton **`configuration.yaml`**:

```yaml
imo_relay:
  port: "/dev/ttyUSB0"      # Port RS485 (vérifier avec: ls /dev/tty*)
  baudrate: 38400           # Vitesse de communication
  bytesize: 8               # Taille des données
  slave_id: 1               # Adresse Modbus de l'automate
  name: "IMO Ismart"        # Nom du dispositif
```

Puis **redémarre Home Assistant** pour activer l'intégration.

### Trouver le port USB sur Raspberry Pi:

```bash
# Via SSH sur la Pi
ls -la /dev/ttyUSB*
dmesg | grep -i usb
```

Typiquement: `/dev/ttyUSB0` ou `/dev/ttyUSB1`

## 🎮 Utilisation

### Via UI Home Assistant

Après installation et redémarrage, tu trouveras les entités:
- `switch.relay_1` → Relay 1
- `switch.relay_2` → Relay 2
- `switch.relay_3` → Relay 3
- `switch.relay_4` → Relay 4

### Via Automation

```yaml
automation:
  - alias: "Allumer Relay 1"
    trigger:
      platform: time
      at: "08:00:00"
    action:
      service: switch.turn_on
      target:
        entity_id: switch.relay_1

  - alias: "Éteindre Relay 1"
    trigger:
      platform: time
      at: "18:00:00"
    action:
      service: switch.turn_off
      target:
        entity_id: switch.relay_1
```

### Via Service Personnalisé

```yaml
service: imo_relay.write_coil
data:
  address: 0x0551      # Adresse Modbus du relais
  state: true          # true = ON, false = OFF
```

## 📊 Adresses Modbus Supportées

| Relais | Adresse | Type |
|--------|---------|------|
| Relay 1 | `0x0551` | Coil (bobine) |
| Relay 2 | `0x0552` | Coil (bobine) |
| Relay 3 | `0x0553` | Coil (bobine) |
| Relay 4 | `0x0554` | Coil (bobine) |

> 💡 Vous pouvez modifier ces adresses dans `const.py` selon votre configuration

## 🎨 Dashboard Lovelace

Un fichier `lovelace_dashboard.yaml` inclus contient un dashboard avec:
- Affichage de l'état des relais en temps réel
- Boutons stylisés (vert = ON, gris = OFF)
- Icônes Material Design Icons

Importe-le dans ta configuration Lovelace!

## 🔧 Troubleshooting

### Erreur: "Failed to connect"

```bash
# 1. Vérifier la connexion USB
ls /dev/ttyUSB*

# 2. Vérifier les permissions
sudo usermod -a -G dialout homeassistant

# 3. Redémarrer le conteneur HA
```

### Erreur: "Modbus exception"

- Vérifier l'adresse slave ID du SMT-CD-T20
- Vérifier les registres Modbus (0x0551, etc.)
- Consulter la doc du fabricant IMO

### Les relais ne répondent pas

```yaml
# Test via service dans Developer Tools:
service: imo_relay.write_coil
data:
  address: 0x0551
  state: true
```

Vérifier les logs: `Configuration → Logs`

## 📝 Fichiers de Configuration Modbus

Pour configurer le SMT-CD-T20:
- Adresse Modbus: `1` (par défaut)
- Fonction: `Modbus RTU`
- Baudrate: `38400` (par défaut)
- Data bits: `8`
- Parity: `None`
- Stop bits: `1`

## 🐛 Debugging

Pour activer les logs détaillés:

```yaml
# Dans configuration.yaml
logger:
  logs:
    custom_components.imo_relay: debug
    pymodbus.client: debug
```

## 📞 Support

- **Issues GitHub**: [Signaler un bug](https://github.com/artemis-fowl-fowl/imo_relay/issues)
- **Discussions**: [Demander de l'aide](https://github.com/artemis-fowl-fowl/imo_relay/discussions)

## 📄 Licence

MIT License - Voir [LICENSE](LICENSE)

## 🙏 Remerciements

- [Home Assistant](https://www.home-assistant.io/)
- [Pymodbus](https://github.com/pymodbus-dev/pymodbus)
- [IMO Ismart](https://www.imo-online.de/)

---

**Version:** 1.0.0  
**Dernière mise à jour:** Janvier 2025  
**Auteur:** Gabriel

[hacs-badge]: https://img.shields.io/badge/HACS-Custom-41BDF5?style=for-the-badge
[hacs-url]: https://github.com/hacs/integration
[license-badge]: https://img.shields.io/badge/License-MIT-blue?style=for-the-badge
[license-url]: https://github.com/artemis-fowl-fowl/imo_relay/blob/main/LICENSE
[python-badge]: https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge
[python-url]: https://www.python.org/
