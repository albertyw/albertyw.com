Bash File Test Operators

bash-operators

1665034644

Usage Example:
```bash
if [[ -e "$file" ]]; then
  echo "pass"
else
  echo "does not pass"
fi
```

| Operator | Meaning                      |
|----------|------------------------------|
| `-e`     | File exists                  |
| `-s`     | File exists and is not empty |
