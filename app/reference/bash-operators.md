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

| Operator | Meaning                                   |
|----------|-------------------------------------------|
| `-e`     | File exists                               |
| `-s`     | File exists and is not empty              |
| `-d`     | File exists and is a directory            |
| `-f`     | File exists and is a regular file         |
| `-v`     | Variable is set and been assigned a value |
| `-z`     | String is zero                            |
| `-n`     | String is non-zero                        |

[Reference (Bash Man Page)](https://linux.die.net/man/1/bash#:~:text=precedence%20rules%20above.-,Conditional%20Expressions,-Conditional%20expressions%20are)
