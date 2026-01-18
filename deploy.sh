#!/bin/bash
# Script de déploiement pour GitHub et HACS

echo "🚀 Préparation du déploiement..."

# 1. Initialiser git (si nécessaire)
if [ ! -d .git ]; then
    echo "📦 Initialisation du repository git..."
    git init
    git add .
    git commit -m "Initial commit: IMO Ismart Relay Control integration"
else
    echo "✅ Repository git existant"
fi

# 2. Vérifier la structure
echo "🔍 Vérification de la structure..."

REQUIRED_FILES=(
    "README.md"
    "LICENSE"
    "CHANGELOG.md"
    "hacs.json"
    "custom_components/imo_relay/manifest.json"
    "custom_components/imo_relay/__init__.py"
    "custom_components/imo_relay/modbus_client.py"
    "custom_components/imo_relay/switch.py"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file - MANQUANT!"
    fi
done

# 3. Instructions finales
echo ""
echo "=========================================="
echo "📋 PROCHAINES ÉTAPES:"
echo "=========================================="
echo ""
echo "1️⃣  Créer un repo sur GitHub:"
echo "   → https://github.com/new"
echo "   → Name: imo_relay"
echo "   → Public: YES"
echo "   → License: MIT"
echo ""
echo "2️⃣  Pousser le code:"
echo "   git remote add origin https://github.com/VOTRE_USERNAME/imo_relay.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3️⃣  Ajouter des tags (optionnel):"
echo "   git tag -a v1.0.0 -m 'Release 1.0.0'"
echo "   git push origin v1.0.0"
echo ""
echo "4️⃣  Soumettre à HACS:"
echo "   → https://hacs.xyz/docs/publish/integration"
echo "   Ou ajouter en tant que repo personnel via HACS UI"
echo ""
echo "=========================================="
echo "✨ C'est prêt pour le déploiement!"
echo "=========================================="
