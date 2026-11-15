# 🏨 Onfly — Consolidador de Reservas de Hotel

CLI desenvolvido em Python para ler reservas de hotel, aplicar as regras de faturamento e gerar um relatório JSON consolidado em reais.

O projeto foi recebido como um desafio técnico com defeitos intencionais em regras de câmbio, cálculo de noites, status faturáveis e ordenação. Depois da investigação e das correções, o relatório passou a seguir o contrato proposto e a suíte final ficou com **11 testes aprovados**.

---

## 📂 Estrutura do projeto

```text
📦 onfly-desafio
├── 📁 data
│   ├── 📄 exemplo-validacao.csv
│   ├── 📄 reservas_hoteis.csv
│   └── 📄 taxas_cambio.csv
├── 📁 entrega
│   ├── 📘 README-ENTREGA.md
│   └── 📁 uso-de-ia
│       ├── 📄 declaracao.md
│       ├── 📄 sessao-01.jsonl
│       ├── 📄 sessao-01.md
│       ├── 📄 sessao-02.jsonl
│       └── 📄 sessao-02.md
├── 📁 output
│   └── 📄 .gitkeep
├── 📁 src
│   └── 📁 onfly_report
│       ├── 📁 repositories
│       ├── 📁 services
│       ├── 📄 cli.py
│       ├── 📄 models.py
│       └── 📄 __main__.py
├── 📁 tests
│   ├── 📄 helpers.py
│   ├── 📄 test_currency.py
│   ├── 📄 test_nights.py
│   ├── 📄 test_regression_report.py
│   ├── 📄 test_status_rules.py
│   └── 📄 test_top_hotels.py
├── ⚙️ pyproject.toml
├── 📄 requirements.txt
├── 📄 requirements-dev.txt
└── 📘 README.md
```

## 🛠 O que usei?

- **Python 3.11** para o CLI e as regras de negócio.
- **Biblioteca padrão do Python** para CSV, JSON, datas, argumentos e logs.
- **pytest 8.3.4** para os testes automatizados.
- **Ruff 0.8.4** para análise estática e padronização.

O projeto não precisa de dependências externas em runtime. As dependências de desenvolvimento ficam em `requirements-dev.txt`.

## 📋 Antes de começar

Tenha instalado em sua máquina:

- **[Python 3.11 ou superior](https://www.python.org/downloads/)**
- **Git**, caso queira clonar o repositório

## 🏃‍♂️ Bora rodar!

### 1. Clone o repositório

```bash
git clone https://github.com/PedroMaiaAlves/onfly-desafio.git
cd onfly-desafio
```

### 2. Crie e ative o ambiente virtual

Linux ou macOS:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instale as dependências de desenvolvimento

```bash
pip install -r requirements-dev.txt
```

### 4. Gere o relatório completo

Linux ou macOS:

```bash
PYTHONPATH=src python -m onfly_report \
  --input data/reservas_hoteis.csv \
  --rates data/taxas_cambio.csv \
  --output output/report.json \
  --top 5
```

Windows PowerShell:

```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe -m onfly_report `
  --input data\reservas_hoteis.csv `
  --rates data\taxas_cambio.csv `
  --output output\report.json `
  --top 5
```

O diretório de saída é criado automaticamente. Ao final, o relatório estará em:

```text
output/report.json
```

Resumo esperado para o arquivo completo:

```text
Reservas: 200 | Confirmadas: 153 | Noites: 909 | Total BRL: 249543.79
```

## ⚙️ Argumentos do CLI

| Argumento | Obrigatório | Padrão | Descrição |
|---|---:|---|---|
| `--input` | Sim | — | Caminho do CSV de reservas. |
| `--rates` | Sim | — | Caminho do CSV de taxas de câmbio. |
| `--output` | Não | `output/report.json` | Arquivo JSON que será gerado. |
| `--top` | Não | `5` | Quantidade de hotéis no ranking; deve ser maior ou igual a 1. |

Códigos de saída:

- `0`: execução concluída com sucesso;
- `2`: argumento ou entrada inválida;
- `1`: erro inesperado.

## 🔄 Como o consolidador funciona?

O processamento segue este fluxo:

```text
Ler os CSVs
    ↓
Converter os campos para os tipos corretos
    ↓
Contar as reservas por status
    ↓
Filtrar somente as reservas CONFIRMED
    ↓
Calcular noites e converter os valores para BRL
    ↓
Agrupar por mês e por hotel
    ↓
Gerar o relatório JSON
```

O relatório contém:

- resumo geral das reservas;
- contagens por status;
- total de noites de quarto;
- total e diária média em BRL;
- consolidação pelo mês do check-in;
- ranking dos hotéis de maior valor.

## 📌 Principais regras de negócio

### Status

- Apenas `CONFIRMED` é faturável.
- `CANCELLED` e `NO_SHOW` entram nas contagens, mas não participam das noites, valores, meses ou ranking.
- Qualquer outro status também fica fora das agregações faturáveis.

### Noites

```text
room_nights = (checkout_date - checkin_date).days * rooms
```

A diferença é não inclusiva. Por exemplo, check-in em 10/01 e check-out em 13/01 resultam em três noites por quarto.

### Câmbio

```text
amount_brl = amount * rate_to_brl
```

Os valores usam `Decimal` durante todo o cálculo. O arredondamento para duas casas, com `ROUND_HALF_UP`, acontece somente na serialização.

### Ordenação

- `by_month`: mês em ordem crescente;
- `top_hotels`: total em BRL decrescente;
- em caso de empate: `hotel_id` crescente.

## 📄 Formato do relatório

Exemplo simplificado:

```json
{
  "report_version": "1.0",
  "generated_at": "2026-11-15T10:00:00-03:00",
  "summary": {
    "total_reservations": 200,
    "confirmed_reservations": 153,
    "cancelled_reservations": 22,
    "no_show_reservations": 25,
    "total_room_nights": 909,
    "total_amount_brl": "249543.79",
    "average_nightly_rate_brl": "274.53"
  },
  "by_month": [],
  "top_hotels": []
}
```

Os campos monetários são strings com exatamente duas casas decimais e sem separador de milhar.

## 🧪 Testes e validação

Execute a suíte completa com:

```bash
pytest -q
```

No Windows, também é possível usar diretamente o ambiente virtual:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Resultado final:

```text
11 passed
```

Os testes cobrem:

- conversão de BRL e USD;
- precisão decimal e arredondamento;
- valor monetário zero;
- virada de mês e datas iguais;
- check-out anterior ao check-in;
- regras de `CONFIRMED`, `CANCELLED`, `NO_SHOW` e `PENDING`;
- relatório de regressão completo;
- ranking decrescente e desempate por `hotel_id`.

### Validando com a amostra oficial

```bash
PYTHONPATH=src python -m onfly_report \
  --input data/exemplo-validacao.csv \
  --rates data/taxas_cambio.csv \
  --output output/exemplo.json
```

Resultado esperado:

```text
Reservas: 12 | Confirmadas: 9 | Noites: 28 | Total BRL: 7566.00
```

## 🧩 Defeitos corrigidos

- operação de câmbio invertida;
- perda de precisão monetária;
- status não faturáveis incluídos nos totais;
- cálculo incorreto na virada de mês;
- ranking de hotéis em ordem incorreta;
- desempate incorreto para hotéis de mesmo valor.

O processo de investigação, as causas e as validações estão detalhados em [`entrega/README-ENTREGA.md`](entrega/README-ENTREGA.md).

## 🤖 Uso de inteligência artificial

O uso de IA foi declarado conforme solicitado no desafio:

- [`entrega/uso-de-ia/declaracao.md`](entrega/uso-de-ia/declaracao.md)
- [`entrega/uso-de-ia/sessao-01.md`](entrega/uso-de-ia/sessao-01.md)
- [`entrega/uso-de-ia/sessao-02.md`](entrega/uso-de-ia/sessao-02.md)
- exportações nativas em JSONL na mesma pasta

## 🤔 Problemas que podem aparecer

### `No module named onfly_report`

Confirme que `src` está no `PYTHONPATH`:

Linux ou macOS:

```bash
export PYTHONPATH=src
```

Windows PowerShell:

```powershell
$env:PYTHONPATH = "src"
```

### O comando copiado do Bash não funciona no PowerShell

No Bash, a continuação de linha usa `\`. No PowerShell, use a crase `` ` `` ou execute o comando em uma única linha.

### O relatório não apareceu

Confira o caminho informado em `--output`. Se o argumento não for enviado, o padrão é `output/report.json`.

### `--top` retorna erro

O valor precisa ser um inteiro maior ou igual a `1`.

## 📚 Documentação complementar

- [Relatório completo da entrega](entrega/README-ENTREGA.md)
- [Declaração de uso de IA](entrega/uso-de-ia/declaracao.md)
- [Configuração do projeto](pyproject.toml)

---

## Obrigado! 🚀

Projeto desenvolvido como parte do desafio técnico da Onfly.
