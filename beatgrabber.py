import yt_dlp
import os
import sys
import re 
from tqdm import tqdm

def is_valid_url(url):
    """
    valida si la url ingresada es un enlace valido de youtube 
    """
    youtube_regex = re.compile(
        r'^(https?://)?www\.)?(youtube\.com|youtu\.?be)/.+$'
    )

    return youtube_regex.match(url)

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
    return ydl_opts


def download_progress(d):
    """
    funcion para mostrar el progreso de descarga
    """
    if d["status"] == "downloading":
        if 'total_bytes' in d:
            total = d['total_bytes']
        elif 'total_bytes_estimate' in d:
            total = d['total_bytes_estimate']
        else:
            total = 0

        if 'pbar' not in globals():
            global pbar
            pbar = tqdm(total=total, unit= "B", unit_scale=True, desc="downloading")

        downloaded = d.get("downloaded_bytes", 0)
        pbar.update(downloaded - pbar.n)
    elif d["status"] == "finished":
        print("\n✅ Download Complete")

def download(url, quality="best", format="bestaudio"):
    """
    Funcion para descargar un video/audio desde una URL, con manejo de errores 
    """
    opciones = get_options(quality, format)

    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            total_size = info_dict.get("filesize", 0)

            if total_size:
                global pbar
                pbar = tqdm(total=total_size, unit="B", unit_scale=True, desc="downloading")

            ydl.download([url])

    except yt_dlp.utils.DownloadError as e:
        print (f"❌ Error en la descarga: {e}")

    except Exception as e:
                print (f"⚠️ Ocurrio un error inesperado: {e}")

    finally:
         if 'pbar' in globals():
              pbar.close()

def get_url_and_format():
    while True:
        url = input("Paste a video URL: ").strip()
        if is_valid_url(url):
            break
        else:
            print("❌invalid URL - Try again")

    while True:
        choice = input("Download option: (audio/video): ").strip().lower()
        if choice in 


if __name__ == "__main__":
    # Obtener URL y llamar a la función de descarga
    url = get_url()
    download(url)
