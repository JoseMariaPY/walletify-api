

## ExpensesTable

```
| Field         | Tipo   | Ejemplo             |
| ------------- | ------ | ------------------- |
| `PK`          | String | `USER#12345`        |
| `SK`          | String | `EXPENSE#abcd-1234` |
| `amount`      | Number | `50.0`              |
| `category_id` | String | `CATEGORY#food`     |
| `date`        | String | `2025-07-07`        |
| `description` | String | `"Almuerzo"`        |

```

### LSI: LSI_Date

```
PK = USER#12345
SortKey = date

✅ Te permite consultar: "Todos los gastos del usuario ordenados por fecha"
```

### CategoriesTable

```
| Field         | Tipo   | Ejemplo                 |
| ------------- | ------ | ----------------------- |
| `PK`          | String | `USER#12345`            |
| `SK`          | String | `CATEGORY#food`         |
| `name`        | String | `"Comida"`              |
| `description` | String | `"Gastos en alimentos"` |
```

### MovementsTable

```
| Field         | Tipo   | Ejemplo                  |
| ------------- | ------ | ------------------------ |
| `PK`          | String | `USER#12345`             |
| `SK`          | String | `MOVEMENT#gym`           |
| `type`        | String | `"expense"` o `"income"` |
| `amount`      | Number | `25.0`                   |
| `frequency`   | String | `"monthly"`              |
| `start_date`  | String | `"2025-01-01"`           |
| `description` | String | `"Gym membership"`       |
```


