import sys
import os

# adicionar a pasta "generated" ao PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), "generated"))

import grpc
from concurrent import futures

import voting_pb2
import voting_pb2_grpc

# Credenciais válidas
VALID_CREDS = {"CRED-ABC-123", "CRED-DEF-456", "CRED-GHI-789"}
USED_CREDS = set()

# Lista de candidatos
CANDIDATES = [
    (1, "Candidato A"),
    (2, "Candidato B"),
    (3, "Candidato C")
]

# Contagem de votos (em memória)
votes = {1: 0, 2: 0, 3: 0}


class VotingService(voting_pb2_grpc.VotingServiceServicer):

    def GetCandidates(self, request, context):
        return voting_pb2.GetCandidatesResponse(
            candidates=[
                voting_pb2.Candidate(id=i, name=n)
                for i, n in CANDIDATES
            ]
        )

    def Vote(self, request, context):
        if request.voting_credential not in VALID_CREDS:
            return voting_pb2.VoteResponse(
                success=False,
                message="Credencial inválida"
            )

        if request.voting_credential in USED_CREDS:
            return voting_pb2.VoteResponse(
                success=False,
                message="Credencial já usada"
            )

        if request.candidate_id not in votes:
            return voting_pb2.VoteResponse(
                success=False,
                message="Candidato inválido"
            )

        votes[request.candidate_id] += 1
        USED_CREDS.add(request.voting_credential)

        return voting_pb2.VoteResponse(
            success=True,
            message="Voto registado com sucesso"
        )

    def GetResults(self, request, context):
        return voting_pb2.GetResultsResponse(
            results=[
                voting_pb2.CandidateResult(
                    id=i,
                    name=n,
                    votes=votes[i]
                )
                for i, n in CANDIDATES
            ]
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    voting_pb2_grpc.add_VotingServiceServicer_to_server(
        VotingService(), server
    )
    server.add_insecure_port("[::]:50052")
    server.start()
    print("AV ativa em localhost:50052")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
