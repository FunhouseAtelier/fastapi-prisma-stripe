#!/bin/bash
source .venv/bin/activate

if [ -z "$1" ]; then
  echo "❌ Migration name required. Usage: ./migrate.sh <name>"
  exit 1
fi

echo "📦 Running Prisma migration: $1"
prisma migrate dev --name "$1"