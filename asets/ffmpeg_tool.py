import sys
import os
import traceback

from loguru import logger
import subprocess

def audio_conwert(data,format,inp_format='save.ogg'):
        """
        audio_conwert(data,format)
        
        :param1: binaru music data
        
        :param2: convert format data `mp3`
        
        :return: binaru converts data or error
        """
        try:
            # Определяем путь к ffmpeg
            if sys.platform.startswith('win'):
                ffmpeg=os.path.join(os.getcwd(),'asets' ,'ffmpeg-master-latest-win64-gpl-shared','bin','ffmpeg.exe') # для windows
            else:
                ffmpeg=os.path.join(os.getcwd(),'asets' ,'ffmpeg-master-latest-linuxarm64-lgpl','bin','ffmpeg') # для Linux
            # Сохраняем временный файл
            with open('save.ogg', 'wb') as f:
                f.write(data)
                
            if not os.path.exists(ffmpeg):
                logger.error(f'no file {ffmpeg} please download full asets file')
            # Конвертируем в WAV
            mes=subprocess.run([
                ffmpeg,
                '-v', 'error', # только error
                '-i', inp_format,
                '-ar', '16000',  # частота дискретизации
                '-ac', '1',      # моно-аудио
                '-y',            # перезаписать если файл существует
                f'out.{format}'
            ], check=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # Читаем файл
            if os.path.exists(f'out.{format}'):
                with open(f'out.{format}', 'rb') as f:
                    return f.read()
            else:
                logger.warning(f'no file out.{format}')
                raise EOFError(f'не удалось создать файл out.{format} его чтение не возможно')
            os.remove(f'out.{format}')
        except subprocess.CalledProcessError as e:
            logger.error(f"Ошибка конвертации аудио: {e}")
            return "Ошибка обработки аудио"
        except Exception as e:
            logger.error(f"Ошибка распознавания: {str(e)}\n{traceback.format_exc()}")
            return f"Произошла ошибка: {str(e)} выход ffmpeg>{mes.stdout + mes.stderr}"
        finally: 
            # Удаляем временные файлы
            for f in [inp_format, f'out.{format}']:
                try:
                    if os.path.exists(f):
                        os.remove(f)
                except:
                    pass

def video_to_audio_conwert(data,format):
        """
        audio_conwert(data,format)
        
        :param1: binaru music data
        
        :param2: video (`mp4`) convert to audio file 
        
        :return: binaru converts data or error
        """
        try:
            # Определяем путь к ffmpeg
            if sys.platform.startswith('win'):
                ffmpeg=os.path.join(os.getcwd(),'asets' ,'ffmpeg-master-latest-win64-gpl-shared','bin','ffmpeg.exe') # для windows
            else:
                ffmpeg=os.path.join(os.getcwd(),'asets' ,'ffmpeg-master-latest-linuxarm64-lgpl','bin','ffmpeg') # для Linux
        
            # Сохраняем временный файл
            with open('save.mp4', 'wb') as f:
                f.write(data)
                
            if not os.path.exists(ffmpeg):
                logger.error(f'no file {ffmpeg} please download full asets file')
            codec = {
            "ogg" : "libopus",
            "mp3" : "libmp3lame",
            "wav" : "pcm_s16le",
            "aac" : "aac",
            "flac": "flac",
            "m4a" : "aac",
            "webm": "libopus -b:a 128k",
            "ac3" :  "ac3 -b:a 448k",
            "wma" : "wmapro -ac 6 -q:a 1"
            }
            # Конвертируем в WAV
            mes=subprocess.run([
                ffmpeg,
                '-v', 'error',
                '-i', 'save.mp4',
                '-vn',
                '-acodec', codec[format], # MP3 encoder
                '-q:a', '4',              # Quality (0-9, 2=high)
                '-y',
                f'out.{format}'
            ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # Читаем файл
            if os.path.exists(f'out.{format}'):
                with open(f'out.{format}', 'rb') as f:
                    return f.read()
            else:
                logger.warning(f'no file out.{format}')
                raise EOFError(f'не удалось создать файл out.{format} его чтение не возможно')
            os.remove(f'out.{format}')
        except subprocess.CalledProcessError as e:
            logger.error(f"Ошибка конвертации аудио: {e}")
            return "Ошибка обработки аудио"
        except Exception as e:
            logger.error(f"Ошибка распознавания: {str(e)}\n{traceback.format_exc()}")
            return f"Произошла ошибка: {str(e)} выход ffmpeg>{mes.stdout + mes.stderr}"
        finally:
            del data # очистка данных
            # Удаляем временные файлы
            for f in ['save.mp4', 'out.mp3']:
                try:
                    if os.path.exists(f):
                        os.remove(f)
                except:
                    pass

def video_meta_data(data:bytes):
    """
    video_meta_data(data)
        
    :param1: binaru video data
        
    :return: meta data fila
    """
    try:
        # Определяем путь к ffmpeg
        if sys.platform.startswith('win'):
            ffmpeg=os.path.join(os.getcwd(),'asets' ,'ffmpeg-master-latest-win64-gpl-shared','bin','ffmpeg.exe') # для windows
        else:
            ffmpeg=os.path.join(os.getcwd(),'asets' ,'ffmpeg-master-latest-linuxarm64-lgpl','bin','ffmpeg') # для Linux
        
        # Сохраняем временный файл
        with open('save.mp4', 'wb') as f:
            f.write(data)
                
        if not os.path.exists(ffmpeg):
            logger.error(f'no file {ffmpeg} please download full asets file')

        mes=subprocess.run([
            ffmpeg,
            '-v', 'error',
            '-show_format',
            '-show_streams',
            '-of', 'json',
            '-i', 'pipe:0'
            ],input=bytes(data), check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        os.remove('save.mp4')
        return mes.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        logger.error(f"Ошибка извлечения мета данных: {e}")
        return "error:Ошибка извлечения мета данных"
    except Exception as e:
        logger.error(f"Ошибка распознавания: {str(e)}\n{traceback.format_exc()}")
        if 'mes' in locals():
            return f"error:Произошла ошибка: {str(e)} выход ffmpeg>{mes.stdout + mes.stderr}"
    finally:
        os.remove('save.mp4')