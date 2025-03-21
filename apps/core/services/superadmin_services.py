from django.db import connection
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class SuperAdminServices:
    @staticmethod
    def get_users():
        """Fetch all users using raw SQL."""
        query = "SELECT * FROM core_user WHERE role != 'super_admin';"   # Dynamic table name

        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]  # Get column names
            users = [dict(zip(columns, row)) for row in cursor.fetchall()]  # Convert rows to dict
        
        return users  # Return pure data (list of dicts)

    @staticmethod
    def get_user_by_id(id):
        with connection.cursor() as cursor:
            cursor.execute(
                   "SELECT id, email, role, is_active FROM core_user WHERE id = %s",
                [id]
            )
            row = cursor.fetchone()
            if row:
                return {"id": row[0], "ema  il": row[1], "role": row[2], "is_active": row[3]}
            return None
        
    @staticmethod
    def create_user(email, password, role):
        hashed_password = make_password(password) 
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO core_user (email, password, role, is_active, is_staff, is_superuser, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
                RETURNING id
                """,
                [email, hashed_password, role, True, False, False]  
            )
            
            user_id = cursor.fetchone()[0]

            if(role == "artist_manager"):
                cursor.execute(
                    """
                    INSERT INTO core_managerprofile (user_id, created_at, updated_at)
                    VALUES (%s,  NOW(), NOW())
                    """,
                    [user_id]
                )

            if(role == "artist"):
                cursor.execute(
                    """
                    INSERT INTO core_artistprofile (user_id, created_at, updated_at)
                    VALUES (%s,  NOW(), NOW())
                    """,
                    [user_id]
                )

        return user_id   
    
    @staticmethod
    def delete_user(user_id):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM core_music WHERE artist_id = (SELECT id FROM core_artistprofile WHERE user_id = %s)", [user_id])
            cursor.execute("DELETE FROM core_artistprofile WHERE user_id = %s", [user_id])
            cursor.execute("DELETE FROM core_managerprofile WHERE user_id = %s", [user_id]) 
            cursor.execute("DELETE FROM core_user where id =%s",[user_id])
            return cursor.rowcount
        
    @staticmethod
    def update_user(new_password,new_role,user_id):
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE core_user SET password=%s, role=%s, updated_at = NOW() where id=%s ",[new_password, new_role, user_id]
            )
            cursor.execute(
            "SELECT * FROM core_user WHERE id=%s", [user_id]
            )
        
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "email": row[4],
                    "role": row[5],
                    "updated_at": row[6], 
                }
            return None
        

