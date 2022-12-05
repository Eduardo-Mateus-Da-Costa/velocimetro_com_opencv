from typing import Optional
import cv2
import time
import numpy as np

imagem_de_referencia = cv2.imread("imagem_de_referencia3.jpg")

distancia_de_referencia = 8000

verde = (0, 255, 0)
vermelho = (0, 0, 255)
branco = (255, 255, 255)

tempo_inicial = 0
distancia_inicial = 0

lista_de_distancias = []
lista_de_velocidades = []


def calcula_velocidade(distancia, tempo):
    velocidade = distancia / tempo
    return velocidade


def calcula_media(lista, tamanho):
    itens = len(lista) - tamanho
    if itens < 0:
        itens = len(lista)
    itens_selecionados = lista[itens:]
    if len(itens_selecionados) == 0:
        return 0
    media = sum(itens_selecionados) / len(itens_selecionados)
    return media


def procura_linha_vertical(imagem, cor, posicao: Optional[int] = 1, lado_esquerdo: Optional[bool] = False):
    contador = 0
    mesma_linha = False
    valor_x = None
    centro_altura = int(imagem.shape[0] / 2)
    margen_de_erro_de_cor = 10
    for x in range(imagem.shape[1]):
        (b, g, r) = imagem[centro_altura, x]
        if abs(b - cor[0]) < margen_de_erro_de_cor and abs(g - cor[1]) < margen_de_erro_de_cor and abs(r - cor[2]) < margen_de_erro_de_cor:
            if not mesma_linha:
                contador += 1
                if contador == posicao and lado_esquerdo:
                    valor_x = x
                    return valor_x
            mesma_linha = True
            valor_x = x
        else:
            mesma_linha = False
            if contador == posicao and valor_x:
                return valor_x
    raise ValueError("Não foi possível encontrar a linha")


def procura_quadrado(image, color):
    try:
        hsv_color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
        valor = hsv_color[0][0][0]
        limite_inferior = np.array([valor - 20 if (valor - 20) > 0 else 0, 100, 100])
        limite_superior = np.array([valor + 20 if (valor + 20) <= 255 else 255, 255, 255])
        img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mascara = cv2.inRange(img_hsv, limite_inferior, limite_superior)
        contornos, _ = cv2.findContours(mascara, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contornos[0][0][0][0]
    except Exception as e:
        raise ValueError("Não foi possível encontrar o quadrado")


if __name__ == "__main__":
    video = cv2.VideoCapture("video_teste7.mp4")
    posicao_da_primeira_linha = procura_linha_vertical(imagem_de_referencia, vermelho)
    posicao_da_segunda_linha = procura_linha_vertical(imagem_de_referencia, vermelho, 2, True)
    while True:
        ret, frame = video.read()
        if ret:
            posicao_do_objeto = procura_quadrado(frame, np.uint8([[[255, 0, 0]]]))
            if posicao_da_primeira_linha < posicao_do_objeto < posicao_da_segunda_linha:
                distancia = (posicao_do_objeto - posicao_da_primeira_linha)
                lista_de_distancias.append(distancia)
                distancia_media = calcula_media(lista_de_distancias, 2)
                if distancia_inicial != 0:
                    distancia_corrida = distancia - distancia_inicial

                    if distancia_corrida < 0:
                        distancia_corrida * -1

                    tempo_corrido = time.time() - tempo_inicial

                    velocidade = calcula_velocidade(distancia_corrida, tempo_corrido)
                    lista_de_velocidades.append(velocidade)
                    velocidade_media = calcula_media(lista_de_velocidades, 2)
                    if velocidade_media < 0:
                        velocidade_media = velocidade_media * -1

                    cv2.putText(frame, f"Velocidade: {velocidade_media:.2f} m/s", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, verde, 2)
                    print(f"Velocidade: {velocidade_media:.2f} m/s")
                distancia_inicial = distancia
                tempo_inicial = time.time()
                cv2.putText(
                    frame, f"Distancia percorrida = {round(distancia, 2)} m", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    verde, 2)
            cv2.imshow("Video", frame)
        else:
            break
        if cv2.waitKey(1) == ord("q"):
            break
video.release()
cv2.destroyAllWindows()
