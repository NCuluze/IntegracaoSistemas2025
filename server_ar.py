import sys
import os

# adicionar a pasta "generated" ao PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), "generated"))

import random
import grpc
from concurrent import futures

import voter_pb2
import voter_pb2_grpc


VALID_CREDS = [
    "CRED-ABC-123",
    "CRED-DEF-456",
    "CRED-GHI-789"
]

class VoterRegistrationService(voter_pb2_grpc.VoterRegistrationServiceServicer):

    def IssueVotingCredential(self, request, context):
        if random.random() < 0.7:
            return voter_pb2.VoterResponse(
                is_eligible=True,
                voting_credential=random.choice(VALID_CREDS)
            )
        else:
            return voter_pb2.VoterResponse(
                is_eligible=False,
                voting_credential="INVALID-" + hex(random.randint(0, 9999))
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    voter_pb2_grpc.add_VoterRegistrationServiceServicer_to_server(
        VoterRegistrationService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("AR ativa em localhost:50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
