#!/bin/bash
source .venv/bin/activate
echo "⚙️ Generating Prisma client..."
prisma generate
