## Fast_zero

### Inicializar o servidor na porta 8001, se for o caso
```bash
uvicorn fast_zero.app:app --port 8001
```

## Alembic

### Criar as migrações
```bash
alembic revision --autogenerate -m "exercicio 02 aula 04"
```

### Aplicar as migrações
```bash
alembic upgrade head
```

### Checando a aplicação
```bash
sqlite3 database.db
```

 