from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.lung_cancer_predictor import LungCancerRiskPredictor
from core.compliance import ComplianceEngine
from core.audit_logger import SecureAuditLogger

prediction_routes = Blueprint('prediction', __name__)

class PredictionController:
    def __init__(
        self, 
        risk_predictor: LungCancerRiskPredictor,
        compliance_engine: ComplianceEngine,
        audit_logger: SecureAuditLogger
    ):
        self.risk_predictor = risk_predictor
        self.compliance_engine = compliance_engine
        self.audit_logger = audit_logger
    
    @prediction_routes.route('/predict', methods=['POST'])
    @jwt_required()
    def predict_lung_cancer_risk(self):
        """
        Secure endpoint for lung cancer risk prediction
        
        :return: Privacy-preserved prediction with explainability
        """
        # Authenticate current user
        current_user = get_jwt_identity()
        
        # Validate access permissions
        if not self.compliance_engine.validate_data_access(
            user_id=current_user, 
            purpose='risk_prediction'
        ):
            # Log unauthorized access attempt
            self.audit_logger.log_event(
                event_type='unauthorized_access',
                user_role='unknown',
                data_access_details={
                    'user_id': current_user,
                    'attempted_action': 'risk_prediction'
                }
            )
            
            return jsonify({
                'error': 'Insufficient permissions',
                'status': 403
            }), 403
        
        # Process prediction request
        try:
            patient_features = request.json.get('features')
            
            # Predict with privacy protections
            prediction = self.risk_predictor.predict_with_privacy(
                patient_features, 
                privacy_budget=0.1
            )
            
            # Log successful prediction
            self.audit_logger.log_event(
                event_type='prediction_performed',
                user_role='clinician',
                data_access_details={
                    'user_id': current_user,
                    'risk_score': float(prediction)
                }
            )
            
            return jsonify({
                'risk_score': float(prediction),
                'privacy_level': 'High'
            })
        
        except Exception as e:
            # Log error scenarios
            self.audit_logger.log_event(
                event_type='prediction_error',
                user_role='clinician',
                data_access_details={
                    'user_id': current_user,
                    'error_message': str(e)
                }
            )
            
            return jsonify({
                'error': 'Prediction failed',
                'status': 500
            }), 500