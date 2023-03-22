import uvicorn
from fastapi import FastAPI
from api.special import SpecialManagement, CopySpecial, RevealSpecial, SpecialDetails
from api.npc import NPCManagement, CopyNPC, RevealNPC, NPCDetails
from api.comment import CommentDetails, CommentManagement, ComponentComments, UserComments

app = FastAPI()
"""
api.add_resource(SpecialManagement, '/special/manage')
api.add_resource(CopySpecial, '/special/copy/<int:special_id>')
api.add_resource(RevealSpecial, '/special/reveal/<int:world_id>/<int:special_id>')
api.add_resource(SpecialDetails, '/special/<int:special_id>')
api.add_resource(NPCManagement, '/npc/manage')
api.add_resource(CopyNPC, '/npc/copy/<int:npc_id>')
api.add_resource(RevealNPC, '/npc/reveal/<int:world_id>/<int:npc_id>')
api.add_resource(NPCDetails, '/npc/<int:npc_id>')
api.add_resource(CommentManagement, '/comment/manage/')
api.add_resource(CommentDetails, '/comment/<int:comment_id>')
api.add_resource(ComponentComments, '/comment/<int:component_table>/<int:comment_id>')
api.add_resource(UserComments, '/user/<int:user_id>/comments/<int:limit>/<int:page>/')

"""


if __name__ == '__main__':
    uvicorn.run("fastapi_code:app")
    