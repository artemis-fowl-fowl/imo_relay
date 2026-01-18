# Changelog

## [1.0.0] - 2025-01-18

### Features
- ✨ Intégration initiale Modbus RTU pour IMO Ismart SMT-CD-T20
- ✨ Support des 4 relais (addresses 0x0551-0x0554)
- ✨ Driver Modbus RTU avec pymodbus 3.6.0+
- ✨ Entités Switch pour Home Assistant
- ✨ Service personnalisé `write_coil` pour contrôle avancé
- ✨ Configuration flexible (baudrate, bytesize, slave ID)
- ✨ Dashboard Lovelace avec boutons stylisés
- ✨ Support complet des logs DEBUG

### Documentation
- 📖 README complet en français
- 📖 Exemples de configuration
- 📖 Guide d'installation HACS
- 📖 Troubleshooting et debugging

### Technical
- ⚙️ Utilisation de pymodbus pour communication Modbus RTU
- ⚙️ Architecture async pour Home Assistant 2024.1.0+
- ⚙️ Gestion complète des erreurs Modbus
- ⚙️ Logging détaillé pour debugging

---

**Status:** Production Ready ✅
