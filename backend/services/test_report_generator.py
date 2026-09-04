from backend.schemas.quiz import QuizResult
from backend.schemas.speaking_evaluation import SpeakingEvaluation
from backend.schemas.test_report import TestReport
from backend.schemas.report_analysis import ReportAnalysis
from backend.services.llm_service import get_llm


def generate_mcq_report(
    quiz_result: QuizResult,
    lecture_context: str
) -> TestReport:

    llm = get_llm()

    prompt = f"""
You are an educational assessment assistant.

Analyze the learner's MCQ test performance using ONLY the
provided quiz result and lecture context.

Test type: MCQ

Score: {quiz_result.percentage}%
Correct answers: {quiz_result.correct_answers}
Total questions: {quiz_result.total_questions}

Lecture context:
{lecture_context}

Generate:
1. Strengths — what the learner performed well on.
2. Recommendations — what the learner should revise or improve.

Rules:
- Do not calculate the score.
- Do not change the score.
- Do not invent concepts that are not present in the lecture context.
- Keep each strength concise.
- Keep each recommendation actionable.
- Return only the requested structured fields.

Respond with ONLY a single valid JSON object, no other text, matching
exactly this shape:
{{
  "strengths": ["<string>", "..."],
  "recommendations": ["<string>", "..."]
}}

Both fields are REQUIRED JSON arrays with AT LEAST ONE item each -- never
an empty array, and never a single combined string. If the score is low
and there is little to praise, still include at least one genuine,
modest strength (for example, effort shown, a correctly-grasped basic
concept, or simply attempting the assessment) rather than leaving the
array empty.
"""

    analysis = llm.with_structured_output(
        ReportAnalysis,
        method="json_mode",
    ).invoke(prompt)

    return TestReport(
        test_type="mcq",
        score=quiz_result.percentage,
        strengths=analysis.strengths,
        recommendations=analysis.recommendations
    )


def generate_speaking_report(
    evaluation: SpeakingEvaluation,
    lecture_context: str
) -> TestReport:

    llm = get_llm()

    prompt = f"""
You are an educational assessment assistant.

Analyze the learner's speaking test performance using ONLY the
provided speaking evaluation and lecture context.

Test type: Speaking

Accuracy: {evaluation.accuracy}%
Feedback:
{evaluation.feedback}

Lecture context:
{lecture_context}

Generate:
1. Strengths — what the learner did well.
2. Recommendations — what the learner should improve or practice.

Rules:
- Do not calculate the score.
- Do not change the accuracy.
- Do not invent concepts that are not present in the lecture context.
- Use the provided evaluation feedback.
- Keep each strength concise.
- Keep each recommendation actionable.
- Return only the requested structured fields.

Respond with ONLY a single valid JSON object, no other text, matching
exactly this shape:
{{
  "strengths": ["<string>", "..."],
  "recommendations": ["<string>", "..."]
}}

Both fields are REQUIRED JSON arrays with AT LEAST ONE item each -- never
an empty array, and never a single combined string. If accuracy is low
and there is little to praise, still include at least one genuine,
modest strength (for example, effort shown, a correctly-grasped basic
concept, or simply attempting the assessment) rather than leaving the
array empty.
"""

    analysis = llm.with_structured_output(
        ReportAnalysis,
        method="json_mode",
    ).invoke(prompt)

    return TestReport(
        test_type="speaking",
        score=evaluation.accuracy,
        strengths=analysis.strengths,
        recommendations=analysis.recommendations
    )