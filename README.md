# TIP TOE PLUS

**Número da Lista**: 2<br>
**Conteúdo da Disciplina**: Grafos 2<br>

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 18/0124498  |  Kess Jhones Gomes Tavares |
| 18/0098021  |  Antônio Rangel Chaves |

## Sobre 
Neste segundo trabalho da disciplina, vamos expandir o jogo feito no [trabalho de Grafos 1](https://github.com/projeto-de-algoritmos/Grafos1_TipToeGame), fazendo um novo modo de jogo. O novo modo de jogo consiste em fazer o personagem "Jujuba" atravessar o tabulado (que é um grafo conectado e não-direcionado) com o objetivo de chegar a linha de chegada, porém existem obstáculos para impedi-lo. Os obstáculos são:
- Areia (faz o personagem andar mais lentamente)
- Água (faz o personagem andar mais lento que a areia)
- Fogo (faz o personagem andar mais lento que a água)
- Buraco (faz o personagem cair e voltar ao início, e só é visível quando o personagem cai nele)

Ao encontrar esses obstáculos, o nosso código deve fazer o personagem encontrar o caminho que demore menos para alcançar a linha de chegada. Nós utilizamos busca em profundidade para fazer a Jujuba alcançar a linha de chegada desviando dos buracos já descobertos, e o algoritmo de Dijkstra para achar o menor caminho entre os obstáculos do tabulado.


As regras gerais do jogo são:
- A cada partida os obstáculos são gerados em lugares diferentes do tabulado.
- Ao passar por um quadrado, ele muda de cor e permanece nessa cor até o jogador cair em um buraco, para ajudar o jogador a lembrar o caminho percorrido
- Ao cair em um buraco, o jogador volta para o início e o buraco fica marcado até o final da partida.
- O jogo termina quando o jogador chega na linha de chegada.
  
## Vídeo de apresentação
https://youtu.be/YZrguk1O2tU

## Screenshots
![image](https://github.com/projeto-de-algoritmos/Grafos2_Tip_Toe_Plus/assets/57496213/5b61d2fd-5732-4875-addd-154f9f43a6eb)
![image](https://github.com/projeto-de-algoritmos/Grafos2_Tip_Toe_Plus/assets/57496213/42dbfdb5-fa4a-48e4-a4aa-3368b59e22c9)
![image](https://github.com/projeto-de-algoritmos/Grafos2_Tip_Toe_Plus/assets/57496213/c4d6fd1f-903d-44ff-8419-ba225e7e6d0f)


## Instalação 
**Linguagem**: Python3<br>
Necessário instalar o pygame

## Uso 
Para rodar o projeto basta executar ```python3 game.py```

