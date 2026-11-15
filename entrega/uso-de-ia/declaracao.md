# Declaração de uso de inteligência artificial

## Ferramenta e modelo

- **Ferramenta:** OpenAI Codex no VS Code.
- **Versão registrada do cliente:** `0.167.0-alpha.4.1`.
- **Modelo utilizado nas duas sessões:** `gpt-5.6-sol`.
- **Repositório de trabalho:** `onfly-desafio`.
- **Data local das sessões:** 14/11/2026.

## Finalidade do uso

O Codex foi utilizado como apoio para preparar o ambiente, investigar falhas, explicar comportamentos do código, criar alguns testes adicionais solicitados pelo candidato, executar validações e organizar a documentação final da entrega.

Foram consultadas duas sessões:

1. **Preparação, investigação e testes:** configuração do Python 3.11 e das dependências, reprodução das falhas, apoio ao diagnóstico, execução do CLI, criação de testes adicionais e validação do projeto.
2. **Revisão e documentação:** auditoria dos requisitos de entrega, conferência do código e dos testes, identificação de pendências e elaboração dos documentos para apresentar o projeto de forma clara e amigável no GitHub.

## O que a IA fez

### Sessão 01

- Leu os requisitos do projeto e identificou as versões necessárias de Python, pytest e Ruff.
- Instalou o Python 3.11.9 em paralelo ao Python já existente, criou o ambiente virtual e instalou as dependências de desenvolvimento.
- Executou verificações de dependências, compilação, lint e testes.
- Explicou como inspecionar os valores recebidos por `calculate_room_nights` e apontou o problema de considerar apenas o dia do mês.
- Adaptou para PowerShell o comando de geração do relatório e validou o JSON produzido.
- Ajudou a investigar o teste de check-out anterior ao check-in e explicou a diferença entre testar uma exceção diretamente e por meio do subprocesso usado por `run_cli`.
- A pedido do candidato, implementou o teste do intervalo de datas inválido usando o fluxo do CLI.
- Sugeriu casos de borda e, após autorização, criou três testes de regressão: precisão decimal, desempate do ranking e exclusão de status diferente de `CONFIRMED`.
- Revisou uma tentativa de instrumentação de logs, explicou os problemas encontrados e, por decisão do candidato, removeu os logs experimentais preservando o logging original do CLI.

### Sessão 02

- Comparou o estado do repositório com todos os requisitos do README do desafio.
- Executou os testes, o lint, a amostra oficial e o processamento do arquivo completo.
- Identificou a divergência entre a fórmula de noites e a expectativa inicialmente usada no teste de estadia no mesmo dia.
- Verificou a ausência inicial dos documentos obrigatórios em `entrega/` e o estado de versionamento/publicação do repositório.
- Criou e depois reorganizou o `README-ENTREGA.md`, distribuindo as informações entre resumo, defeitos, investigação, decisões técnicas, validação e testes adicionais.
- Criou esta documentação de uso de IA a partir dos registros das duas sessões.

## O que o candidato fez

- Leu o enunciado, analisou os resultados esperados e tomou as decisões finais sobre a solução.
- Implementou e revisou as correções funcionais de conversão cambial, cálculo de noites, política de status e ordenação dos hotéis.
- Criou os primeiros casos adicionais de teste para valor zero, estadia no mesmo dia e check-out anterior ao check-in.
- Solicitou e revisou os três testes adicionais criados pelo Codex.
- Decidiu manter os testes exercitando o CLI, mesmo após receber uma alternativa de teste unitário direto.
- Solicitou a reversão de uma implementação da IA com a qual não concordou e realizou manualmente a abordagem escolhida.
- Avaliou a proposta de logs adicionais e decidiu não incluí-los no escopo final.
- Revisou os resultados, escreveu a descrição inicial do processo e validará estes documentos antes da publicação.
- Permaneceu responsável pela versão final do código, dos testes, da documentação e do repositório entregue.

## Forma de revisão

As sugestões da IA não foram aceitas automaticamente. O candidato acompanhou as mudanças, pediu explicações, solicitou reversões quando necessário e escolheu quais alterações fariam parte da solução.

Os registros consolidados das interações estão disponíveis em `sessao-01.md` e `sessao-02.md`.
