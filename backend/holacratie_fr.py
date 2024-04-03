from autogen import GroupChat, GroupChatManager, UserProxyAgent, ConversableAgent, config_list_from_json

from agent_builder_fr import AgentBuilderFR

config_file_or_env = "OAI_CONFIG_LIST"
llm_config = {"temperature": 0.3}
# config_list = autogen.config_list_from_json(config_file_or_env, filter_dict={"model": ["gpt-4-1106-preview", "gpt-4"]})
config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")


    

def start_task(execution_task: str, agent_list: list):
    group_chat = GroupChat(agents=agent_list, messages=[], max_round=12)
    manager = GroupChatManager(groupchat=group_chat, llm_config={"config_list": config_list, **llm_config})
    agent_list[0].initiate_chat(manager, message=execution_task)

builder = AgentBuilderFR(
    # config_file_or_env=config_file_or_env, builder_model="gpt-4-1106-preview", agent_model="gpt-4-1106-preview"
    config_file_or_env=config_file_or_env
)

building_task = """Générer des agents capable d'organiser un tel système."""

agent_list, agent_configs = builder.build(building_task, llm_config)

start_task(
    execution_task="""Je souhaite créer le système décris dans cette page https://raw.githubusercontent.com/holacracyone/Holacracy-Constitution-4.1-FRENCH/master/Constitution-Holacracy.md""",
    agent_list=agent_list,
)
