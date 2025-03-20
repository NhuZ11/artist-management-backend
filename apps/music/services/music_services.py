from django.db import connection
from django.contrib.auth import get_user_model

User = get_user_model()

class MusicManagerService:
    @staticmethod
    def get_musics(artist_id):
        query = "SELECT id, title, artist_id AS artist, album_name, genre, created_at, updated_at FROM core_music WHERE artist_id=%s;"
        print(artist_id)

        with connection.cursor() as cursor:
            cursor.execute(query, [artist_id])  # Pass parameters as a tuple (query, [params])
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            musics = [dict(zip(columns, row)) for row in rows]

        print(musics)
        return musics


    @staticmethod
    def create_music(artist_id, title, album_name=None, genre=None):
        """Insert a new music record and return the ID."""
        query = """
            INSERT INTO core_music (artist_id, title, album_name, genre, created_at, updated_at)
            VALUES (%s, %s, %s, %s, NOW(), NOW())
            RETURNING id;
            """
        with connection.cursor() as cursor:
            cursor.execute(query, (artist_id, title, album_name, genre))
            music_id = cursor.fetchone()[0]  # Fetch the returned ID
            
        return music_id
    
    @staticmethod
    def delete_music(music_id, artist_id):
        """Delete a music record by ID."""

        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM core_music WHERE id = %s AND artist_id = %s;", [music_id, artist_id])
            return cursor.rowcount
        

    @staticmethod
    def update_music(music_id, artist_id, title, album_name=None, genre=None):
        """Update a music record by ID."""
        query = """
            UPDATE core_music
            SET title = %s, album_name = %s, genre = %s, updated_at = NOW()
            WHERE id = %s AND artist_id = %s;
            """
        with connection.cursor() as cursor:
            cursor.execute(query, [title, album_name, genre, music_id, artist_id])
            return cursor.rowcount
        