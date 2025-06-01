from database import db_query as dq

def save_proof(from_user, to_user, file_id, proof_type):
    dq("INSERT INTO proofs (from_user, to_user, proof_file, proof_type, submitted_at) VALUES (?,?,?,?,datetime('now'))",
       (from_user, to_user, file_id, proof_type), commit=True)