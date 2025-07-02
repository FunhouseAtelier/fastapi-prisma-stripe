#!/usr/bin/env bash
echo "🧼 Formatting Python and Jinja2 templates..."

# Format Python with isort and yapf
isort app/ scripts/
yapf -r -i app/ scripts/


# Format Jinja2 templates (you already use djlint)
djlint app/templates/ --reformat

echo "✅ Formatting complete."
