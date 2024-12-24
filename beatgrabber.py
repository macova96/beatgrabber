import yt_dlp
import os
import sys
from tqdm import tqdm


def get_options(quality="best", format="bestaudio"):
    """
    funcion para definir la calidad y el formato
    """
    ydl_opts = {
        "format": format,
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "noplaylist": True,
        "progress_hooks": [download_progress],
    }
    return yt_dlp


def download_progress(d):
    """
    funcion para manejar el progreso de descarga
    """
    if d["status"] == "downloading":
        pbar.update(d["downloaded_bytes"] - pbar.n)


def download(url, quality="best", format="bestaudio"):
    opciones = get_options(quality, format)

    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    with yt_dlp.YoutubeDL(opciones) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        total_size = info_dict.get("filesize")
        if total_size:
            global pbar
            pbar = tqdm(total=total_size, unit="B", unit_scale=True, desc="downloading")

        ydl.download([url])


# Función para manejar la URL ingresada por el usuario
def get_url():
    url = input("Paste a video URL: ")
    return url


if __name__ == "__main__":
    # Obtener URL y llamar a la función de descarga
    url = get_url()
    download(url)
