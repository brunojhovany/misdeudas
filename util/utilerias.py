import uuid
import hashlib


class Utilerias:
    def hashpassword(text_to_hash):
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode()+text_to_hash.encode()).hexdigest(), salt

    def matchHashText(hashedText, salt, providedText):
        # _hashed_text,salt= hashedText.split(':');
        return hashedText == hashlib.sha256(salt.encode()+providedText.encode()).hexdigest()
