#!/bin/bash

# Script para configurar variáveis de ambiente do SciNewsAI

set -e

echo "🚀 Configurando SciNewsAI..."
echo ""

# Backend setup
echo "📦 Configurando Backend..."
if [ ! -f "web/backend/.env" ]; then
    if [ -f "web/backend/.env.example" ]; then
        cp web/backend/.env.example web/backend/.env
        echo "✅ Arquivo web/backend/.env criado"
    else
        echo "⚠️  web/backend/.env.example não encontrado"
    fi
else
    echo "✅ web/backend/.env já existe"
fi

# Frontend setup
echo ""
echo "🎨 Configurando Frontend..."
if [ ! -f "web/frontend/.env" ]; then
    if [ -f "web/frontend/.env.example" ]; then
        cp web/frontend/.env.example web/frontend/.env
        echo "✅ Arquivo web/frontend/.env criado"
    else
        echo "⚠️  web/frontend/.env.example não encontrado"
    fi
else
    echo "✅ web/frontend/.env já existe"
fi

echo ""
echo "✨ Configuração concluída!"
echo ""
echo "📝 Próximos passos:"
echo "1. Revise os arquivos .env criados em:"
echo "   - web/backend/.env"
echo "   - web/frontend/.env"
echo ""
echo "2. Ajuste as variáveis conforme necessário"
echo ""
echo "3. Inicie o projeto com:"
echo "   docker-compose up -d"
echo ""
echo "📚 Para mais informações, veja ENV_SETUP.md"
