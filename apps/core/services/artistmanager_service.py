from django.db import connection
from django.contrib.auth import get_user_model

User = get_user_model()


class ArtistManagerService:
    @staticmethod
    def get_users():
        """Fetch all artists."""
        query = 'SELECT * FROM core_artistprofile;'  # Dynamic table name

        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]  # Get column names
            users = [dict(zip(columns, row)) for row in cursor.fetchall()]  # Convert rows to dict
        
        return users  # Return pure data (list of dicts)