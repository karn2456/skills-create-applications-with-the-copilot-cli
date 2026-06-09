from typing import Optional, Dict
from app.models.research import AgentChatRequest, AgentChatResponse
from app.agents.topic_generator import TopicGeneratorAgent
from app.agents.literature_review import LiteratureReviewAgent
from app.agents.framework_builder import FrameworkBuilderAgent
from app.agents.questionnaire_builder import QuestionnaireBuilderAgent
from app.agents.data_analysis import DataAnalysisAgent
from app.agents.paper_writer import PaperWriterAgent
from app.agents.thesis_supervisor import ThesisSupervisorAgent
from app.agents.sem_expert import SEMExpertAgent
from app.agents.aviation_knowledge import AviationKnowledgeAgent


class AgentOrchestrator:
    def __init__(self):
        self.agents = {
            "topic-generator": TopicGeneratorAgent(),
            "literature-review": LiteratureReviewAgent(),
            "framework-builder": FrameworkBuilderAgent(),
            "questionnaire": QuestionnaireBuilderAgent(),
            "data-analysis": DataAnalysisAgent(),
            "paper-writing": PaperWriterAgent(),
            "thesis-supervisor": ThesisSupervisorAgent(),
            "sem-expert": SEMExpertAgent(),
            "aviation-knowledge": AviationKnowledgeAgent(),
        }

    async def process_message(
        self,
        agent_id: str,
        message: str,
        context: Optional[Dict] = None,
        language: str = "th",
    ) -> AgentChatResponse:
        agent = self.agents.get(agent_id)
        if not agent:
            return AgentChatResponse(
                response=f"Agent '{agent_id}' not found. Available agents: {', '.join(self.agents.keys())}",
                agent_id=agent_id,
                suggestions=[],
                next_steps=[],
            )

        result = await agent.process({"message": message, "language": language}, context)

        return AgentChatResponse(
            response=result.get("response", ""),
            agent_id=agent_id,
            suggestions=result.get("suggestions", []),
            next_steps=result.get("next_steps", []),
            artifacts=result.get("artifacts"),
        )
