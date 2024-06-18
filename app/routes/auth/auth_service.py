from app.common.auth.auth_handler import sign_jwt
from app.common.db_connectors.mysql import MysqlConn
from app.dto.auth import SignUpDto, LoginDto
import bcrypt

conn = MysqlConn()

def signupService(req: SignUpDto):
    try:
        query = "insert into users(firstname, lastname, email, password, roles_id, nickname) values (%s, %s, %s, %s, %s, %s)"
        hashedPass = bcrypt.hashpw(req.password.encode('ASCII'), bcrypt.gensalt())
        data = (req.firstname, req.lastname, req.email, hashedPass, req.roles_id, req.nickname)
        rowId = conn.insert(query, data)
        return rowId
    except Exception as error:
        raise Exception(error)

def loginService(req: LoginDto):
    try:
        query = "select * from users where email = %s"
        data = (req.email,)
        user = conn.fetch(query, data)
        user = user[0]
        isSamePassword = False
        if (user != None):
            isSamePassword = bcrypt.checkpw(req.password.encode('ASCII'), user['password'].encode('ASCII'))
        if isSamePassword:
            return sign_jwt(req.email)
        raise Exception()
    except Exception as error:
            raise Exception(error)
