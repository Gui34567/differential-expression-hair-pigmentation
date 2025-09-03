# differential-expression-hair-pigmentation
Este projeto analise as expressões de genes em cabelos pegmentado e não pigmentados.
# Análise de Expressão Gênica Diferencial no Embranquecimento do Cabelo

## Objetivo
O projeto buscou identificar genes diferencialmente expressos em folículos capilares **pigmentados** e **não pigmentados**, com o intuito de compreender os mecanismos moleculares associados ao **embranquecimento capilar**.

## Metodologia
- **Dados**: Microarray público (GSE24009 – GEO/NCBI).
- **Pré-processamento**:
  - Seleção das 12 amostras (8 pigmentadas e 4 não pigmentadas).
  - Transformação log2 para normalização da variância.
- **Análise estatística**:
  - Teste t de Student para cada gene (n=23.232).
  - Cálculo de *p-value*, *t-statistic* e *log2 fold change*.
  - Correção por múltiplos testes via **FDR**.
- **Visualizações**:
  - Volcano Plot para genes significativos.
  - PCA para visualização global das amostras.
  - Boxplots por gene.
  - Distribuição de probabilidades via LOOCV.
- **Modelo exploratório**:
  - Regressão logística com 4 genes (2 significativos pelo FDR + 2 maiores *fold change*).
  - Avaliação por **Leave-One-Out Cross Validation (LOOCV)** e **Repeated Stratified K-Fold**.

## Resultados
- Apenas **2 genes (MIR646HG e MS4A6E)** permaneceram significativos após FDR.
- A análise dos **20 genes com menor p-value** destacou funções ligadas a:
  - **Epigenética e diferenciação celular** (SUZ12, SOX6, PAX4).
  - **Estresse oxidativo e apoptose** (KRIT1, GDPD5).
  - **Inflamação e imunidade** (CSF3, SIGLEC6, RABGEF1).
  - **Sinalização e regeneração folicular** (HHAT, FAM83A, TRPV5).
- O modelo logístico mostrou separação parcial dos grupos, sugerindo que **assinaturas multigênicas** podem explicar melhor o fenômeno do que genes isolados.

## Limitações
- Tamanho amostral reduzido (8 pigmentadas e 4 não pigmentadas).
- Apenas 2 genes significativos após FDR.
- Parte das sondas não possui anotação clara (ex.: 3xSSC e H200007402).
- Modelo logístico exploratório, sem validação externa.
- Ausência de variáveis clínicas (idade, estresse, doenças, etc.).

## Conclusão
O estudo sugere que o **embranquecimento capilar** envolve múltiplos processos biológicos: envelhecimento celular, regulação epigenética, estresse oxidativo e inflamação. Embora preliminares, os resultados indicam potenciais alvos para investigação futura e reforçam a natureza multifatorial do fenômeno.
