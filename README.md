Vào [FFmpeg](https://www.gyan.dev/ffmpeg/builds/) để tải ffmpeg

Vào enviroment variable, add cái đường dẫn bin vào system variables -> path

`python manage.py runserver`

trong sql lite có lưu sẵn 1 số cái t đã test
http://127.0.0.1:8000/api/audio/

để upload 1 wav lên để convert thành text
cùng api ở trên, kéo xuống dưới cùng
![API](media\image\post.png)

sau khi post, sẽ có reponse như sau

```
{
    "id": "49df21de-bb6a-4a79-9d76-fac1f9915371",
    "original_filename": "dc4b81ed-c64c-4bc1-bf80-d27b3f724948.wav",
    "audio_file": "http://127.0.0.1:8000/media/audio_files/dc4b81ed-c64c-4bc1-bf80-d27b3f724948_JP60ZjY.wav",
    "transcription": "OK Google turn on the AC",
    "error_message": null,
    "is_processed": true,
    "is_successful": true,
    "created_at": "2025-05-13T07:13:42.121315Z",
    "updated_at": "2025-05-13T07:13:42.987382Z"
}
```

từ id ở trên, gửi và lấy reponse thông qua

http://127.0.0.1:8000/api/audio/ai-process/{id}/

trong đó, id là cái ở trên, khi ấy sẽ nhận được response như sau

```
{
    "response_id": "49df21de-bb6a-4a79-9d76-fac1f9915371",
    "request_text": "OK Google turn on the AC",
    "response_text": "Okay, I can do that.\n\n\"Alright, I'll set a timer to turn on the air conditioning. It will start in approximately five minutes. The AC will be on then.\"",
    "audio_link": "http://127.0.0.1:8000/media/generated_audio%5C77b88d0f-e1e6-4067-bb1a-5d565a3ff1cd.wav",
    "is_successful": true,
    "created_at": "2025-05-13T07:13:42.121315Z"
}
```

trong đó, audio_link là api để tải cái wav về
