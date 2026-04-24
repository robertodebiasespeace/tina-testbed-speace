"""
Safety Module - Risk Gates & SafeProactive Integration
Composto per la sicurezza e gestione dei rischi.
Versione: 1.0
Data: 23 Aprile 2026
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger("SafetyModule")


class SafetyModule:
    """
    Safety Module - Risk Gates e SafeProactive.

    Responsabilita:
    - Valutazione rischi prima azioni
    - Enforcement vincoli etici
    - Human-in-the-loop per azioni critiche
    - Compliance monitoring
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.name = "safety_module"
        self.version = "1.1"
        self.config = config or {}
        self.bridge = None

        # Risk thresholds
        self.risk_thresholds = {
            "low": 0.3,
            "medium": 0.6,
            "high": 0.8,
            "critical": 0.95,
        }

        # Risk history
        self.risk_assessments: List[Dict] = []
        self.max_assessments = self.config.get("max_assessments", 100)

        # Approved/blocked actions
        self.approved_actions: List[str] = []
        self.blocked_actions: List[str] = []

        # Ethical bounds
        self.ethical_bounds = {
            "no_self_preservation_modification": True,
            "no_autonomous_weapons": True,
            "transparency_required": True,
            "human_oversight_required": True,
            "privacy_by_design": True,
        }

        # Compliance
        self.compliance_frameworks = ["EU_AI_Act", "NIST", "ISO_42001", "TINA"]

        self.last_assessment = datetime.now()
        self.assessment_count = 0
        self.blocked_count = 0

    def set_bridge(self, bridge):
        """Imposta il riferimento al Neural Bridge"""
        self.bridge = bridge

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processo principale Safety Module.

        Args:
            context: Contesto con action da valutare

        Returns:
            Dict con risk_assessment e approval_status
        """
        self.last_assessment = datetime.now()

        try:
            operation = context.get("operation", "assess_risk")

            if operation == "assess_risk":
                result = self._assess_risk(context)
            elif operation == "check_ethics":
                result = self._check_ethical_bounds(context)
            elif operation == "request_approval":
                result = self._request_human_approval(context)
            elif operation == "log_action":
                result = self._log_action(context)
            else:
                result = {"status": "unknown_operation"}

            return {
                "status": "success",
                "result": result,
                "comparto": self.name,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"SafetyModule error: {e}")
            return {"status": "error", "error": str(e), "comparto": self.name}

    def _assess_risk(self, context: Dict) -> Dict[str, Any]:
        """Valuta rischio di un'azione"""
        action = context.get("action", "")
        action_type = context.get("action_type", "unknown")
        parameters = context.get("parameters", {})

        # Calcolo rischio base
        risk_score = self._calculate_risk(action, action_type, parameters)

        # Determina livello
        risk_level = self._get_risk_level(risk_score)

        # Check etici
        ethical_ok = self._check_ethical_compliance(action, parameters)

        # Decisione
        if risk_level in ["critical", "high"] or not ethical_ok:
            self.blocked_actions.append(action)
            self.blocked_count += 1
            approved = False
            approval_needed = True
        else:
            self.approved_actions.append(action)
            approved = True
            approval_needed = risk_level == "medium"

        assessment = {
            "action": action,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "ethical_compliant": ethical_ok,
            "approved": approved,
            "approval_needed": approval_needed,
            "blocking_reason": self._get_blocking_reason(risk_level, ethical_ok) if not approved else None,
        }

        self.risk_assessments.append(assessment)
        self.assessment_count += 1

        if len(self.risk_assessments) > self.max_assessments:
            self.risk_assessments = self.risk_assessments[-self.max_assessments:]

        return assessment

    def _calculate_risk(
        self, action: str, action_type: str, parameters: Dict
    ) -> float:
        """Calcola score di rischio (0-1)"""
        base_risk = 0.3

        # Azioni ad alto rischio
        high_risk_types = ["delete", "modify_system", "network", "external_api"]
        if action_type in high_risk_types:
            base_risk += 0.3

        # Azioni reversibili
        reversible_actions = ["query", "read", "analyze"]
        if action_type in reversible_actions:
            base_risk -= 0.1

        # Parametri rischiosi
        if parameters.get("force", False):
            base_risk += 0.2
        if parameters.get("recursive", False):
            base_risk += 0.15

        return min(1.0, max(0.0, base_risk))

    def _get_risk_level(self, score: float) -> str:
        """Converte score in livello"""
        if score >= self.risk_thresholds["critical"]:
            return "critical"
        elif score >= self.risk_thresholds["high"]:
            return "high"
        elif score >= self.risk_thresholds["medium"]:
            return "medium"
        else:
            return "low"

    def _check_ethical_compliance(self, action: str, parameters: Dict) -> bool:
        """Check compliance con bounds etici"""
        # Check per azioni vietate
        forbidden_patterns = [
            "self_preservation",
            "weapon",
            "harm_human",
            "disable_safety",
        ]

        action_lower = action.lower()
        for pattern in forbidden_patterns:
            if pattern in action_lower:
                return False

        # Check privacy
        if parameters.get("collect_personal_data", False):
            if not self.ethical_bounds.get("privacy_by_design"):
                return False

        return True

    def _get_blocking_reason(
        self, risk_level: str, ethical_ok: bool
    ) -> Optional[str]:
        """Ritorna reason di blocco"""
        if not ethical_ok:
            return "Ethical bounds violation"
        if risk_level == "critical":
            return "Critical risk level"
        if risk_level == "high":
            return "High risk level - requires human approval"
        return None

    def _check_ethical_bounds(self, context: Dict) -> Dict[str, Any]:
        """Verifica tutti i bounds etici"""
        action = context.get("action", "")

        violations = []
        for bound, enabled in self.ethical_bounds.items():
            if enabled and bound.replace("_", " ") in action.lower():
                violations.append(bound)

        return {
            "action": action,
            "bounds_violated": violations,
            "compliant": len(violations) == 0,
            "active_bounds": sum(self.ethical_bounds.values()),
        }

    def _request_human_approval(self, context: Dict) -> Dict[str, Any]:
        """Richiede approvazione umana"""
        action = context.get("action", "")
        risk_level = context.get("risk_level", "medium")

        return {
            "action": action,
            "risk_level": risk_level,
            "approval_requested": True,
            "approval_status": "pending",
            "request_timestamp": datetime.now().isoformat(),
            "required_for": ["high", "critical", "regulatory"],
        }

    def _log_action(self, context: Dict) -> Dict[str, Any]:
        """Log di un'azione"""
        action = context.get("action", "")
        approved = context.get("approved", None)

        log_entry = {
            "action": action,
            "timestamp": datetime.now().isoformat(),
            "approved": approved,
        }

        return log_entry

    def set_risk_threshold(self, level: str, value: float):
        """Imposta threshold per livello rischio"""
        if level in self.risk_thresholds:
            self.risk_thresholds[level] = max(0.0, min(1.0, value))

    def get_risk_history(self, count: int = 20) -> List[Dict]:
        """API per ottenere storico rischi"""
        return self.risk_assessments[-count:]

    def get_status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "assessment_count": self.assessment_count,
            "blocked_count": self.blocked_count,
            "approved_count": len(self.approved_actions),
            "active_ethical_bounds": sum(self.ethical_bounds.values()),
            "last_assessment": self.last_assessment.isoformat(),
        }
