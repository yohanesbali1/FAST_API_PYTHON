from app.database import SessionLocal
from app.models.role import Role, Permission

def seed():
    # import User di sini jika perlu
    from app.models.user import User  

    db = SessionLocal()

    # Permissions
    permission_book = Permission(name="custom_book")
    permission_role_permission = Permission(name="custom_role_permission")
    permission_user = Permission(name="custom_user")

    # Roles
    admin = Role(name="Admin")
    user = Role(name="User")

    # Assign permissions
    admin.permissions = [permission_book, permission_role_permission, permission_user]
    user.permissions = [permission_book]

    # Commit ke DB
    db.add_all([admin, user, permission_book, permission_role_permission, permission_user])
    db.commit()
    db.close()
    print("Seeding done!")

if __name__ == "__main__":
    seed()
