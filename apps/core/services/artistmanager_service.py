from django.db import connection
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class ArtistManagerService:
    @staticmethod
    def get_artists():
        """Fetch all artists."""
        query = """
             SELECT core_artistprofile.*, core_user.email 
             FROM core_artistprofile
             INNER JOIN core_user ON core_user.id = core_artistprofile.user_id;
            """

        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]  # Get column names
            users = [dict(zip(columns, row)) for row in cursor.fetchall()]  # Convert rows to dict
        
        return users
    
    @staticmethod
    def create_artist_profile(artist_name, email, password):
        """Insert a new artist profile using a raw SQL query."""
        hashed_password = make_password(password) 

        with connection.cursor() as cursor:
        # Insert into core_user and get the user_id
            cursor.execute(
            """
            INSERT INTO core_user 
            (email, password, role,is_active, is_superuser, is_staff ,created_at, updated_at) 
            VALUES (%s, %s, 'artist',true,false,false, NOW(), NOW())
            RETURNING id;
            """,
            [email, hashed_password]
             )
            user_id = cursor.fetchone()[0]

            cursor.execute(
            """
            INSERT INTO core_artistprofile (user_id, artist_name, created_at, updated_at)
            VALUES (%s, %s,NOW(), NOW());
            """,
            [user_id, artist_name]
            )

        return user_id  
    
    @staticmethod
    def delete_artist(user_id):
        """Delete an artist profile by user_id."""
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM core_artistprofile WHERE user_id = %s;", [user_id])

            cursor.execute("DELETE FROM core_user WHERE id = %s AND role='artist';", [user_id])

            return cursor.rowcount
        
    @staticmethod
    def update_artist(artist_name, dob, gender, address, first_release_year, no_of_albums_released, artist_id):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE core_artistprofile 
                SET artist_name=%s, dob=%s, gender=%s, address=%s, 
                    first_release_year=%s, no_of_albums_released=%s, updated_at=NOW() 
                WHERE id=%s
                """,
                [artist_name, dob, gender, address, first_release_year, no_of_albums_released, artist_id]
            )
            
            # Fetch the updated record
            cursor.execute(
                """
                SELECT core_artistprofile.*, core_user.email 
                FROM core_artistprofile
                INNER JOIN core_user ON core_user.id = core_artistprofile.user_id
                WHERE core_artistprofile.id = %s
                """,
                [artist_id]
            )
            columns = [col[0] for col in cursor.description]  # Get column names
            artist = cursor.fetchone()

        if artist:
            return dict(zip(columns, artist))  # Return a dictionary with the updated artist data
        return None


