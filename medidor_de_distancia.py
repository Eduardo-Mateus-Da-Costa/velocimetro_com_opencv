import cv2

# TODAS AS MEDIDAS EM CENTÍMETROS

imagem_de_referencia = cv2.imread("imagem_de_referencia.jpg")
# distancia de referência camera -> objeto
distancia_de_referencia = 50
# tamanho (largura) real do objeto
largura_de_referencia = 17

verde = (0, 255, 0)
vermelho = (0, 0, 255)
branco = (255, 255, 255)

cascade_do_objeto = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


def calcular_foco(distancia, largura_na_imagem_de_referencia):
    foco = (largura_na_imagem_de_referencia * distancia) / largura_de_referencia
    return foco


def calcula_distancia(foco, largura_no_video):
    distancia = (largura_de_referencia * foco) / largura_no_video
    return distancia


def procura_objeto(image):
    largura_do_objeto = 0
    imagem_cinza = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    objetos = cascade_do_objeto.detectMultiScale(imagem_cinza, 1.3, 5)
    for (x, y, h, w) in objetos:
        cv2.rectangle(image, (x, y), (x + w, y + h), branco, 1)
        largura_do_objeto = w

    return largura_do_objeto


largura_da_imagem_de_referencia = procura_objeto(imagem_de_referencia)
foco_referencia = calcular_foco(distancia_de_referencia, largura_da_imagem_de_referencia)

if __name__ == "__main__":
    video = cv2.VideoCapture("video_teste.mp4")
    print(foco_referencia)
    cv2.imshow("ref_image", imagem_de_referencia)
    print(imagem_de_referencia.shape)
    foi = False
    while True:
        ret, frame = video.read()
        if ret:
            largura_do_objeto_no_frame = procura_objeto(frame)
            if largura_do_objeto_no_frame != 0:
                distance = calcula_distancia(foco_referencia, largura_do_objeto_no_frame)
                cv2.putText(
                    frame, f"Distancia = {round(distance, 2)} CM", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (vermelho), 2
                )
                if not foi:
                    print(frame.shape)
                    foi = True
            cv2.imshow("frame", frame)
        else:
            break
        if cv2.waitKey(1) == ord("q"):
            break
    video.release()
    cv2.destroyAllWindows()
