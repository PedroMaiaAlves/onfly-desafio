# Entrega do desafio técnico — Consolidador de reservas

## 1. Identificação

- **Candidato:** Pedro Henrique Maia Alves
- **Data da entrega:** 14/11/2026
- **Repositório:** https://github.com/PedroMaiaAlves/onfly-desafio
- **Versão do Python utilizada:** Python 3.11

## 2. Resumo da solução

O trabalho consistiu em investigar e corrigir os defeitos do consolidador de reservas, preservando o comando do CLI e o schema do relatório JSON. A análise partiu das regras de negócio descritas no README e dos testes automatizados, relacionando cada falha ao serviço responsável.

Além das correções necessárias para os testes inicialmente fornecidos, foram criados casos adicionais para valores monetários de borda, precisão decimal, datas inválidas, status não reconhecidos e desempate no ranking de hotéis.

## 3. Defeitos corrigidos

### 3.1. Operação incorreta na conversão de moedas

- **Comportamento observado:** valores em moedas diferentes de BRL produziam totais incorretos no relatório.
- **Causa raiz:** a conversão dividia o valor pela taxa de câmbio, em vez de multiplicá-lo pela taxa para BRL.
- **Correção realizada:** a operação foi alterada para `amount * rate`, seguindo a regra definida no desafio.
- **Como validei:** comparei o valor obtido com o valor esperado no teste de conversão e executei novamente a suíte automatizada.

### 3.2. Perda de precisão em valores monetários

- **Comportamento observado:** valores não inteiros podiam apresentar resultado diferente do arredondamento monetário esperado.
- **Causa raiz:** o uso de `float` no fluxo de conversão introduzia imprecisão antes da serialização do resultado.
- **Correção realizada:** os valores e as taxas passaram a ser calculados com `Decimal`, mantendo o valor exato durante as agregações e aplicando `ROUND_HALF_UP` para duas casas somente na serialização.
- **Como validei:** adicionei um cenário com `0.75 USD`, cuja conversão exata pela taxa `5.42` resulta em `4.065` e deve ser serializada como `4.07`.

### 3.3. Status faturáveis

- **Comportamento observado:** `NO_SHOW` e outros status diferentes de cancelado podiam entrar indevidamente nos valores, nas noites e nas agregações do relatório.
- **Causa raiz:** `is_billable` verificava apenas se o status era diferente de `CANCELLED`, em vez de aceitar exclusivamente `CONFIRMED`.
- **Correção realizada:** a política passou a retornar verdadeiro somente quando o status é exatamente `CONFIRMED`.
- **Como validei:** executei os cenários com `CONFIRMED`, `CANCELLED`, `NO_SHOW` e acrescentei um teste com `PENDING`.

### 3.4. Cálculo de noites em viradas de mês

- **Comportamento observado:** reservas que atravessavam a virada de mês podiam produzir uma quantidade incorreta de noites.
- **Causa raiz:** o cálculo considerava apenas o número do dia do mês, em vez da diferença entre as datas civis completas.
- **Correção realizada:** o total passou a usar `(checkout - checkin).days * rooms`, respeitando a diferença não inclusiva definida no desafio.
- **Como validei:** usei o intervalo de 30/01/2025 a 02/02/2025, que deve resultar em três noites para um quarto.

Também foi adicionada uma validação para impedir que um check-out anterior ao check-in gere uma quantidade negativa de noites.

### 3.5. Ordenação do ranking de hotéis

- **Comportamento observado:** os hotéis de menor valor podiam aparecer antes dos hotéis de maior valor no ranking.
- **Causa raiz:** a agregação era ordenada no sentido oposto ao exigido pelo contrato do relatório.
- **Correção realizada:** os hotéis passaram a ser classificados pelo total em BRL em ordem decrescente, preservando o `hotel_id` em ordem crescente como critério de desempate.
- **Como validei:** executei o cenário de valores diferentes e adicionei outro com dois hotéis de mesmo valor e IDs distintos.

## 4. Investigação e abordagem

Primeiro, li o README para levantar as regras de status, cálculo de noites, câmbio, precisão monetária e ordenação. Em seguida, executei `pytest -q` para reproduzir as falhas e comparei, em cada caso, o resultado obtido com o resultado esperado.

Depois, associei cada teste ao serviço responsável e percorri o fluxo de processamento do CLI: leitura do CSV, conversão de tipos, contagem dos status, filtro de reservas confirmadas e agregação. As correções foram feitas de forma isolada e cada alteração foi validada executando novamente os testes relacionados.

Durante a investigação, os novos casos de teste revelaram situações que não estavam totalmente cobertas pelos cenários iniciais, como precisão decimal, valor zero, status `PENDING`, datas iguais, intervalo de datas inválido e empate entre hotéis. Por fim, executei o CLI de ponta a ponta com a amostra de validação e com o arquivo completo.

## 5. Decisões técnicas

- **Dinheiro:** utilização de `Decimal` durante todo o cálculo, soma dos valores exatos e arredondamento `ROUND_HALF_UP` somente na serialização para duas casas decimais.
- **Datas:** utilização de objetos `date` e da diferença entre as datas completas, sem incluir o dia do check-out.
- **Status:** somente `CONFIRMED` participa das noites, valores, agregação mensal e ranking de hotéis; os demais status continuam sendo contabilizados no total de reservas e nas contagens específicas previstas.
- **Ordenação:** `by_month` permanece em ordem cronológica; `top_hotels` usa total em BRL decrescente e `hotel_id` crescente no empate.
- **Compatibilidade:** o comando, os argumentos do CLI, os códigos de saída e o schema do JSON foram preservados.
- **Validação defensiva:** um check-out anterior ao check-in é rejeitado para evitar a produção de noites negativas.

## 6. Como validar

### 6.1. Preparação do ambiente

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

No Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

### 6.2. Testes automatizados

```bash
pytest -q
```

**Estado encontrado durante a revisão da entrega:**

```text
11 passed in 2.35s
```

### 6.3. Amostra de validação

```bash
PYTHONPATH=src python -m onfly_report \
  --input data/exemplo-validacao.csv \
  --rates data/taxas_cambio.csv \
  --output output/exemplo.json
```

**Resumo produzido pelo CLI:**

```text
Reservas: 12 | Confirmadas: 9 | Noites: 28 | Total BRL: 7566.00
```

Os totais, a agregação mensal e os cinco primeiros hotéis coincidiram com a amostra apresentada no README principal.

### 6.4. Arquivo completo

```bash
PYTHONPATH=src python -m onfly_report \
  --input data/reservas_hoteis.csv \
  --rates data/taxas_cambio.csv \
  --output output/report.json \
  --top 5
```

**Resumo produzido pelo CLI:**

```text
Reservas: 200 | Confirmadas: 153 | Noites: 909 | Total BRL: 249543.79
```

## 7. Implementações adicionais e novos testes

Além das correções dos defeitos inicialmente identificados, foram criados seis testes para ampliar a cobertura das regras e dos casos de borda.

### 7.1. Câmbio e precisão monetária

- `test_currency_conversion_to_brl_with_amount_equals_zero`: verifica que uma reserva de valor zero não interfere no total convertido.
- `test_currency_conversion_preserves_decimal_precision`: verifica a precisão com `Decimal` e o arredondamento half-up somente na serialização.

### 7.2. Casos de borda no cálculo de noites

- `test_nights_same_day`: cobre check-in e check-out na mesma data; pela fórmula não inclusiva, o resultado esperado é `0` noites.
- `test_checkout_before_checkin`: confirma que um check-out anterior ao check-in é rejeitado.


### 7.3. Status não reconhecido

- `test_only_confirmed_status_is_billable`: utiliza uma reserva `PENDING` para confirmar que somente `CONFIRMED` entra nas agregações faturáveis.

### 7.4. Critério de desempate no ranking

- `test_top_hotels_breaks_amount_ties_by_hotel_id_ascending`: cria hotéis com o mesmo total e verifica o desempate pelo `hotel_id` crescente.

Esses testes executam o CLI de ponta a ponta e validam o relatório JSON produzido, mantendo o comando e o schema definidos no desafio.

## 8. Uso de inteligência artificial

Foi utilizada assistência de IA durante o desenvolvimento. A IA auxiliou na revisão dos requisitos, na auditoria do estado do repositório e na organização desta documentação. A implementação das correções, a criação dos casos de teste e a decisão sobre as alterações permaneceram sob responsabilidade do candidato.

- **Ferramenta/modelo:** Codex —
- **Artefatos obrigatórios:** exportação das sessões utilizadas e `entrega/uso-de-ia/declaracao.md`.