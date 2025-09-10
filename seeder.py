from app.database import SessionLocal
from app.models.role import Role, Permission
from app.models.user import User
from app.utils.hash import hash_password   

def seed():
    db = SessionLocal()
    try:
        

        # Permissions
        permission_book = Permission(name="custom_book")
        permission_role_permission = Permission(name="custom_role_permission")
        permission_user = Permission(name="custom_user")

        # Roles
        admin = Role(name="Admin")

        # User
        data_user = User(
            username="admin",
            email="admin@example.com",
            password= hash_password("password")
        )
        # Assign permissions
        admin.permissions = [permission_book, permission_role_permission, permission_user]

        data_user.roles = [admin]

        # Commit ke DB
        db.add_all([admin,data_user,  permission_book, permission_role_permission, permission_user])
        db.commit()
        print("Seeding done!")
    except Exception as e:
        db.rollback()
        print("Seeding failed:", e)
    finally:
        db.close()


if __name__ == "__main__":
    seed()
