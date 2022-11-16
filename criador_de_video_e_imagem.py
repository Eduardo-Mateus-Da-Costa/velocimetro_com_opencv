import cv2
import numpy as np

vermelho = (0, 0, 255)
branco = (255, 255, 255)
azul = (255, 0, 0)

frame = np.zeros((500, 8000, 3), np.uint8)
frame[:] = branco

cv2.line(frame, (100, 0), (100, frame.shape[0]), vermelho, 5)
cv2.line(frame, (frame.shape[1] - 100, 0), (frame.shape[1] - 100, frame.shape[0]), vermelho, 5)


def create_video(velocity_in_pixels: int, name: str, variable: bool):
    width = frame.shape[1]
    height = frame.shape[0]
    centro_y = int(height / 2)
    square_size = 50
    video_writer = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*"mp4v"), 30, (width, height))
    if 0 < velocity_in_pixels < width:
        i = 0
        variacao = 1
        while i < width:
            frame[:] = branco
            cv2.rectangle(frame, (i, centro_y), (i + square_size, centro_y + square_size), azul, -1)
            cv2.line(frame, (100, 0), (100, height), vermelho, 5)
            cv2.line(frame, (width-100, 0), (width-100, height), vermelho, 5)
            video_writer.write(frame)
            if variable:
                i += velocity_in_pixels + variacao * 2
                variacao += 1
            else:
                i += velocity_in_pixels
    video_writer.release()


if __name__ == "__main__":
    # cv2.imwrite("imagem_de_referencia3.jpg", frame)
    # create_video(velocity_in_pixels=5, name="video_teste7.mp4", variable=False)
    pass
