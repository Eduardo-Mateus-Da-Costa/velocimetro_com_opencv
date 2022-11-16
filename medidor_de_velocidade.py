import cv2
import time
import medidor_de_distancia as md

tempo_inicial = 0
distancia_inicial = 0
tempo_corrido = 0
distancia_corrida = 0

lista_de_distancias = []
lista_de_velocidades = []

video = cv2.VideoCapture("video_teste.mp4")


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


while True:
    ret, frame = video.read()

    if ret:
        largura_do_objeto_no_frame = md.procura_objeto(frame)
        if largura_do_objeto_no_frame != 0:
            distancia = md.calcula_distancia(md.foco_referencia, largura_do_objeto_no_frame)
            lista_de_distancias.append(distancia)
            distancia_media = calcula_media(lista_de_distancias, 2)

            distancia_em_metros = distancia / 100

            if distancia_inicial != 0:
                distancia_corrida = distancia_inicial - distancia_em_metros

                if distancia_corrida < 0:
                    distancia_corrida = distancia_corrida * -1

                tempo_corrido = time.time() - tempo_inicial

                velocidade = calcula_velocidade(distancia_corrida, tempo_corrido)
                lista_de_velocidades.append(velocidade)
                media_velocidade = calcula_media(lista_de_velocidades, 2)
                if media_velocidade < 0:
                    media_velocidade = media_velocidade * -1

                cv2.putText(
                    frame, f"Velocidade: {round(media_velocidade, 2)} m/s", (50, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    md.vermelho, 2)

            distancia_inicial = distancia_em_metros
            tempo_inicial = time.time()

            cv2.putText(
                frame, f"Distancia = {round(distancia_em_metros, 2)} m", (50, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, md.verde, 2)
        cv2.imshow("Video", frame)
    else:
        break
    if cv2.waitKey(1) == ord("q"):
        break
video.release()
cv2.destroyAllWindows()
