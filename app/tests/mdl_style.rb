all
rule 'MD029', style: :ordered
exclude_rule 'MD013'  # Temporary exclusion.  TODO: remove
exclude_rule 'MD041'  # Notes are displayed with headers added in separately
exclude_rule 'MD002'  # Ibid
exclude_rule 'MD030'  # Rule conflicts with style guide
exclude_rule 'MD010'  # False positive hard tabs visible in code fences
exclude_rule 'MD026'  # False positive on app/notes/20180711-0403.md
exclude_rule 'MD033'  # Allow HTML in notes, needed for things that markdown doesn't support
