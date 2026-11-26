import os
def get_env():
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    user= os.getenv("DB_USER")
    dbname= os.getenv("DB_NAME")
    password = os.getenv("DB_PASSWORD")
    if not host:
        raise ValueError("DB_HOST REQUIRED")
    if host.strip()=="":
        raise ValueError("DB_HOST NOT BE EMPTY")
    
    if port is None:
        raise ValueError("DB_PORT REQUIRED")
    try:
        port_int = int(port)
    except ValueError:
        raise ValueError(f"DB_PORT: {port} MUST BE INTEGER")
    if port_int < 1 or port_int > 65535:
        raise ValueError("DB_PORT MUST BE EQUAL 1-65535")
    
    if user is None:
        raise ValueError("DB_USER REQUIRED")
    if user.strip()=="":
        raise ValueError("DB_USER NOT BE EMPTY")
    
    if dbname is None:
        raise ValueError("DB_NAME REQUIRED")
    if dbname.strip()=="":
        raise ValueError("DB_NAME NOT BE EMPTY")

    if password is None:
        raise ValueError("DB_PASSWORD REQUIRED")
    if password.strip()== "":
        raise ValueError("DB_PASSWORD NOT BE EMPTY")

    return {"DB_HOST":host,
            "DB_PORT":port_int,
            "DB_USER":user,
            "DB_NAME":dbname,
            "DB_PASSWORD":password}