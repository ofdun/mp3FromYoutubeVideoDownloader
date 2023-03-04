from pytube import YouTube
from typing import LiteralString
import os
import ffmpeg


class NoLinksError(Exception):
    pass


def downloadVideo(url: LiteralString, path: LiteralString = 'videos/') -> LiteralString:
    filename = YouTube(url).title + '.mp4'
    try:
        YouTube(url).streams.filter(progressive=True, file_extension='mp4').get_by_resolution("720p").download(
            output_path=path, filename=filename)
    except:
        YouTube(url).streams.filter(progressive=True, file_extension='mp4').first().download(
            output_path=path, filename=filename)
    return filename


def convertVideoToOGG(path: LiteralString) -> None:
    (
        ffmpeg
        .input(path)
        .audio
        .output(path.replace('mp4', 'ogg'), ** {'ar': '8000', 'acodec': 'libvorbis'})
        .run()
    )


if __name__ == '__main__':
    links = [i.replace('\n', '') for i in open('links.txt')]
    pathToVideos = 'videos/'
    if not links:
        raise NoLinksError("Ссылки добавь в файл сын дерьмеца")
    for video in links:
        name = downloadVideo(video, pathToVideos)
        convertVideoToOGG(pathToVideos + name)
        os.remove(pathToVideos + name)
