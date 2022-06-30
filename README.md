# BCH-31-16

Implementação de um algoritmo de codificação e decodificação BCH.

São enviadas informações de 16 bits em pacotes de 31 bits, o algoritmo é capaz de detectar e corrigir 3 erros.

Para visualizar os processo deve-se mudar os 3 valores do vetor 'changed_bits', todo o processo é mostrado no terminal.

O campo finito é definido de forma genérica, porém alguns polinômios utilizados no código são retirados de tabelas e dificultam a generalização.

O código segue o exemplo disponibilizado por:

WALLACE, H. Error Detection and Correction Using the BCH Code. 2005.


A correção de um numero de erros <3 e detecção de numero de erros >3 pode ser aplicada generalizando a parte do algoritmo de decodificação do preenchimento da tabela conforme o descrito na bibliografia e fica proposta como trabalho futuro.


# REFERÊNCIAS:
LIN, S. and COSTELLO, D. J. Erro Control Coding: Fundamental and Application. Prentice-Hall. ISBN 0-13-283796-X. 1982.​

MENEGHESSO, C. Código Corretores de Erros. TCC (Graduação) - Licenciatura em Matemática, Universidade Federal de São Carlos. São Carlos, 2012.​

SASSIOUI, R.; JABI, M.; SZCZECINSKI, L.; LE, L. B.; BENJILLALI, M.; PELLETIER, B. HARQ and AMC: Friends or Foes?, in IEEE Transactions on Communications, vol. 65, no. 2, pp. 635-650, Feb. 2017.​

SAYOOD, Khalid. Introduction to Data Compression, ISBN 13: 978-0-12-620862-7, ISBN 10: 0-12-620862-X. 2006.​

SILVA, Lucas Sousa. Simulação dos algoritmos de rate matching e HARQ no enlace direto do LTE. 2014.​

