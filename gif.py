from PIL import Image, ImageSequence

def concat_gifs(gif1_path, gif2_path, output_path, loop=0):
    # GIF 파일 열기
    gif1 = Image.open(gif1_path)
    gif2 = Image.open(gif2_path)
    
    # 각 GIF의 모든 프레임을 리스트로 저장 (원본의 palette, duration 정보는 기본적으로 유지되지 않을 수 있으므로 복사)
    frames1 = [frame.copy() for frame in ImageSequence.Iterator(gif1)]
    frames2 = [frame.copy() for frame in ImageSequence.Iterator(gif2)]
    
    # 두 GIF의 프레임을 순차적으로 이어 붙임
    combined_frames = frames1 + frames2
    
    # 각 프레임의 지속시간(duration)을 저장 (없을 경우 100ms 기본값 사용)
    durations = []
    for frame in ImageSequence.Iterator(gif1):
        durations.append(frame.info.get("duration", 100))
    for frame in ImageSequence.Iterator(gif2):
        durations.append(frame.info.get("duration", 100))
    
    # 첫 번째 프레임을 기준으로 나머지 프레임을 추가하면서 저장
    combined_frames[0].save(
        output_path,
        save_all=True,
        append_images=combined_frames[1:],
        loop=loop,
        duration=durations,
        disposal=2
    )

# 사용 예: gif1.gif의 프레임과 gif2.gif의 프레임을 이어 붙여 combined.gif로 저장
concat_gifs("cool.gif", "hot.gif", "combined.gif")