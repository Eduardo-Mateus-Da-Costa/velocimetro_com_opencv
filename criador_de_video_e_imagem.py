import cv2
import numpy as np

vermelho = (0, 0, 255)
branco = (255, 255, 255)
azul = (255, 0, 0)

frame = np.zeros((500, 8000, 3), np.uint8)
frame[:] = branco

cv2.line(frame, (100, 0), (100, frame.shape[0]), vermelho, 5)
cv2.line(frame, (frame.shape[1] - 100, 0), (frame.shape[1] - 100, frame.shape[0]), vermelho, 5)


def criar_video(velocidade_em_pixels: int, nome: str, velocidade_variavel: bool):
    largura = frame.shape[1]
    altura = frame.shape[0]
    centro_y = int(altura / 2)
    tamanho_do_quadrado = 50
    escritor_de_video = cv2.VideoWriter(nome, cv2.VideoWriter_fourcc(*"mp4v"), 30, (largura, altura))
    if 0 < velocidade_em_pixels < largura:
        i = 0
        variacao = 1
        while i < largura:
            frame[:] = branco
            cv2.rectangle(frame, (i, centro_y), (i + tamanho_do_quadrado, centro_y + tamanho_do_quadrado), azul, -1)
            cv2.line(frame, (100, 0), (100, altura), vermelho, 5)
            cv2.line(frame, (largura-100, 0), (largura-100, altura), vermelho, 5)
            escritor_de_video.write(frame)
            if velocidade_variavel:
                i += velocidade_em_pixels + variacao * 2
                variacao += 1
            else:
                i += velocidade_em_pixels
    escritor_de_video.release()


if __name__ == "__main__":
    # cv2.imwrite("imagem_de_referencia3.jpg", frame)
    # create_video(velocity_in_pixels=5, name="video_teste7.mp4", variable=False)
    pass
