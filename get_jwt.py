from jwcrypto import jwk,jwt
import time
import json
import os

#JWTトークンの有効期限（最大30分 エポック秒で指定）
exp = (int(time.time()))+(60 * 30)

token_exp = 3600

with open('./credentials/private-key.json') as f:
    privateKey = json.load(f)

print('privateKey:', privateKey)


header = {"alg": privateKey['alg'],
          "typ": "JWT",
          "kid": privateKey['kid']}

channel_id = os.getenv('CH_ID')
print('channel_id:', channel_id)
payload = { "iss": channel_id, "sub": channel_id, "aud": "https://api.line.me/", "exp": exp, "token_exp": token_exp }

#プライベートキーをJSONからJWKに変換
privateKey = jwk.JWK(**privateKey)

#JWTトークンを作成
Token = jwt.JWT(header=header,claims=payload)

#作成したプライベートキーで署名
Token.make_signed_token(privateKey)

#シリアライズ
JWTtoken = Token.serialize()

#完成
print(JWTtoken)